# Case Study: Debugging a Broken CI Pipeline

A record of a real debugging session on this repo's GitHub Actions pipeline — kept as a
reference for interviews and for my own future self. The pipeline had been failing silently
for weeks, and the fix turned out to be three separate, layered problems, not one.

---

## Symptom

The scheduled CI workflow (`SDET Test Suite`) had failed on every run for at least a week.
`pytest` never got a chance to report a single test result — every run died before that point.

---

## Investigation

**1. Read the job/step breakdown, not just "pass/fail."**
GitHub Actions reports pass/fail per *step*, not just per run. Pulling the step list for the
failing run immediately narrowed the search:

```
Install dependencies         success
Install Playwright browsers  failure   <-- here
Run smoke tests               skipped
Run full test suite           skipped
```

Everything downstream of the failure was `skipped`, not `failed` — a useful distinction.
`skipped` means "never got a chance to run"; treat the first non-`success` step as the actual
point of failure, not the last one in the list.

**2. Check what changed vs. what's pinned.**
`requirements.txt` pinned `playwright==1.44.0`. That version predates Playwright's support for
Ubuntu 24.04 ("Noble"), which is what GitHub's `ubuntu-latest` runner had migrated to. The
`--with-deps` flag on `playwright install` shells out to `apt-get` using a hardcoded
supported-OS table baked into that Playwright version — on an OS it doesn't recognize, it
fails immediately, before ever touching the network.

I confirmed this *without* needing the raw CI logs (see below) by checking that the actual
browser binary download URL was reachable (`curl -I` on the CDN link returned `200`) — which
ruled out "browser build got removed from the CDN" and pointed at the OS-support step instead.

> **Lesson:** a pinned dependency version isn't just "the version I tested with" — it's a bet
> that the version keeps working on infrastructure you don't control (runner images, OS
> releases) that changes out from under you on its own schedule. Prefer `>=` for tooling like
> browser drivers unless you have a specific reason to pin exactly.

**3. Don't assume you have log access — verify it.**
`gh` wasn't installed locally, and GitHub's REST API requires an authenticated token to
download raw job logs (`.../actions/jobs/{id}/logs`), *even for public repositories*. The
check-run annotations API gave a partial picture (which step failed, exit code) but not the
actual stdout. When the API is blocked, the run's page in a logged-in browser session still
has full access — a good fallback when you don't have `gh` or a token handy.

---

## Root cause #1: pinned Playwright version vs. runner OS

**Fix:** bump `requirements.txt`:
```diff
- playwright==1.44.0
- pytest-playwright==0.5.0
+ playwright>=1.45.0
+ pytest-playwright>=0.5.1
```

This got the browser installed — but the very next push still failed. New symptom, same
investigation loop.

---

## Root cause #2: the workflow was silently disabled

The push after the `requirements.txt` fix produced **no new run at all**. Not a failure —
nothing. GitHub Actions auto-disables a workflow's schedule (and, less obviously, blocks
*all* its triggers, including `push`) after 60 days without repository activity. The workflow
file itself was untouched and looked fine; the disablement lives in GitHub's UI state, not in
the YAML.

**Fix:** click "Enable workflow" on the workflow's Actions page. Since GitHub doesn't
retroactively run a disabled workflow for pushes that happened while it was off, triggering a
fresh run afterward required a new commit (an empty `git commit --allow-empty` is enough).

> **Lesson:** "no failure" and "no run" look identical from a distance (both show as "nothing
> happened since my push"). Always check that a run was *created* for your commit before
> assuming the absence of a red X means something is broken elsewhere.

---

## Root cause #3: a real race condition, exposed once the above got fixed

With the environment fixed, tests finally executed — and three failed, deterministically,
every time:

```
tests/ui/test_inventory.py::TestInventory::test_inventory_loads          FAILED
tests/ui/test_inventory.py::TestInventory::test_inventory_has_six_items  FAILED
tests/ui/test_checkout.py::TestCheckout::test_full_purchase_flow         FAILED
```

All three failed with a count/visibility check returning `0`/`False` where a value was
expected. The pattern that mattered: **every other UI test passed**, and every other UI test's
first action after page setup was a `.click()` or `.select_option()` — actions that Playwright
auto-waits on until the target element is actionable. The three failures called
`is_visible()` and `.count()` as their *first* action — both of which check the DOM exactly
once, synchronously, with **no polling and no timeout**, unlike almost everything else in
Playwright's API.

Root cause: the `logged_in_page` fixture and `CartPage.open_cart()` returned control
immediately after a click that triggers client-side navigation, before the destination page's
content had actually rendered. On a fast local machine this window never got hit; on the CI
runner's timing it did, every single time — deterministic, not flaky, because the runner's
timing profile was fixed.

**Fix attempt #1 (wrong):** wait for the URL to change:
```python
page.wait_for_url("**/inventory.html")
```
Still failed, identically. This taught me something specific about the app under test: it's a
client-rendered SPA where the route/URL updates *before* the async fetch-and-render of page
content finishes. Waiting on the URL doesn't wait on the DOM.

**Fix attempt #2 (correct):** wait for the actual content marker instead of the URL:
```python
page.wait_for_selector(InventoryPage.INVENTORY_CONTAINER)   # in the login fixture
self.page.wait_for_selector(self.CART_ITEMS)                 # in CartPage.open_cart()
```
This passed, consistently, in CI.

> **Lesson:** Playwright's locator-based actions (`click`, `fill`, `select_option`) auto-wait;
> its direct page queries (`is_visible`, `.count()`, `inner_text` used as a check) do **not**.
> Never call the non-waiting APIs as the *first* thing you do after an action that triggers
> navigation or async rendering — always synchronize on real content first. And when a fix
> doesn't work, don't just retry it harder — the failure was still identical byte-for-byte,
> which meant the hypothesis was wrong, not that the fix needed a bigger hammer.

---

## Takeaways for SDET work generally

- **A CI failure is a chain, not a single cause.** This one had three unrelated root causes
  stacked on top of each other. Fixing #1 didn't just reveal #2 — it revealed a totally
  different class of problem (#3) that had presumably been dormant/masked the entire time.
- **`skipped` ≠ `failed`.** Read what actually ran before diagnosing why something else didn't.
- **Reproduce locally before trusting a fix, but know when you can't.** The race condition in
  root cause #3 didn't reproduce on a fast local machine — that's expected for timing bugs, not
  a reason to skip investigation. Reason from the code and Playwright's documented waiting
  semantics instead of only from a local pass/fail.
- **Verify a fix against the actual target, not a proxy.** Local test runs are a fast feedback
  loop, but "fixes GitHub CI" was the actual acceptance criterion here — every fix attempt was
  pushed and watched through to a real run result before being called done.
- **When a fix doesn't move the needle, the failure output is the next clue.** Identical
  failure text after a change means the change didn't touch the actual mechanism — go back to
  the hypothesis, not the code.
