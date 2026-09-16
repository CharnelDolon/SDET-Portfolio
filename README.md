# SDET Portfolio — Saucedemo Test Framework

![CI](https://github.com/YOUR_USERNAME/sdet-portfolio/actions/workflows/tests.yml/badge.svg)

A production-style automated test framework built with **Playwright**, **pytest**, and **GitHub Actions CI**. Covers UI automation, REST API testing, and data-driven test scenarios.

---

## What's tested

| Area | Target | Tests |
|------|--------|-------|
| UI — Login | saucedemo.com | Valid login, locked user, empty fields, logout |
| UI — Inventory | saucedemo.com | Page load, item count, sorting, add to cart |
| UI — Checkout | saucedemo.com | Full purchase flow, missing field validation |
| API — CRUD | jsonplaceholder.typicode.com | GET / POST / PUT / DELETE, schema validation |
| Data-driven | saucedemo.com | All user types via parametrize |

---

## Tech stack

- **Playwright (Python)** — browser automation
- **pytest** — test runner, fixtures, parametrize
- **Page Object Model** — maintainable UI test structure
- **requests + jsonschema** — API testing and schema validation
- **GitHub Actions** — CI on every push and daily schedule
- **pytest-html** — HTML test reports with screenshots on failure

---

## Project structure

```
sdet-portfolio/
├── pages/                  # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   ├── ui/                 # Browser tests
│   ├── api/                # REST API tests
│   └── data/               # Data-driven tests
├── utils/
│   ├── config.py           # Environment variables
│   └── helpers.py          # Shared utilities / data generators
├── reports/                # Auto-generated HTML reports
├── .github/workflows/      # CI pipeline
├── conftest.py             # Shared fixtures
└── pytest.ini              # pytest config
```

---

## Getting started

```bash
# 1. Clone and install
git clone https://github.com/YOUR_USERNAME/sdet-portfolio.git
cd sdet-portfolio
pip install -r requirements.txt
playwright install chromium

# 2. Copy env file
cp .env.example .env

# 3. Run smoke tests
pytest -m smoke -v

# 4. Run full suite
pytest -v

# 5. Open the HTML report
start reports/report.html   # Windows
open reports/report.html    # Mac
```

---

## Running specific test types

```bash
pytest -m ui        # UI tests only
pytest -m api       # API tests only
pytest -m smoke     # Quick sanity check
pytest -m regression # Full regression suite
```

---

## CI pipeline

Tests run automatically on every push to `main` and `dev`, on every pull request, and on a daily schedule (weekday mornings). The HTML report is uploaded as a CI artifact after every run.

See [`docs/ci-debugging-case-study.md`](docs/ci-debugging-case-study.md) for a write-up of a real CI outage on this pipeline and how it was diagnosed and fixed.
