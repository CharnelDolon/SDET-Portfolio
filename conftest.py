import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import BASE_URL, STANDARD_USER, PASSWORD


# ── Browser / page fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def logged_in_page(page):
    """Returns a page already logged in as standard_user."""
    login = LoginPage(page)
    login.navigate()
    login.login(STANDARD_USER, PASSWORD)
    page.wait_for_selector(InventoryPage.INVENTORY_CONTAINER)
    return page


# ── Page Object fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(logged_in_page):
    return InventoryPage(logged_in_page)


@pytest.fixture
def cart_page(logged_in_page):
    return CartPage(logged_in_page)
