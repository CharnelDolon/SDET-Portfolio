import pytest
from utils.config import STANDARD_USER, LOCKED_USER, PASSWORD


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:

    def test_valid_login(self, login_page, page):
        """Standard user can log in successfully."""
        login_page.navigate()
        login_page.login(STANDARD_USER, PASSWORD)
        assert "inventory" in page.url

    def test_locked_out_user(self, login_page):
        """Locked out user sees an error message."""
        login_page.navigate()
        login_page.login(LOCKED_USER, PASSWORD)
        assert login_page.is_error_visible()
        assert "locked out" in login_page.get_error_message().lower()

    def test_wrong_password(self, login_page):
        """Wrong password shows an error."""
        login_page.navigate()
        login_page.login(STANDARD_USER, "wrong_password")
        assert login_page.is_error_visible()

    def test_empty_username(self, login_page):
        """Empty username shows a validation error."""
        login_page.navigate()
        login_page.login("", PASSWORD)
        assert login_page.is_error_visible()
        assert "username" in login_page.get_error_message().lower()

    def test_empty_password(self, login_page):
        """Empty password shows a validation error."""
        login_page.navigate()
        login_page.login(STANDARD_USER, "")
        assert login_page.is_error_visible()
        assert "password" in login_page.get_error_message().lower()

    def test_logout(self, inventory_page):
        """Logged-in user can log out and is redirected to login page."""
        inventory_page.logout()
        assert inventory_page.page.url.endswith("/")
