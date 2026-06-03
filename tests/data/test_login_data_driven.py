import pytest
from utils.config import PASSWORD


# Each tuple: (username, expected_outcome)
LOGIN_SCENARIOS = [
    ("standard_user",      "success"),
    ("locked_out_user",    "locked"),
    ("problem_user",       "success"),
    ("performance_glitch_user", "success"),
    ("",                   "error"),
    ("invalid_user",       "error"),
]


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("username,expected", LOGIN_SCENARIOS)
def test_login_scenarios(login_page, username, expected):
    """Data-driven test covering all Saucedemo user types."""
    login_page.navigate()
    login_page.login(username, PASSWORD)

    if expected == "success":
        assert "inventory" in login_page.page.url, \
            f"Expected inventory page for user '{username}'"

    elif expected == "locked":
        assert login_page.is_error_visible()
        assert "locked out" in login_page.get_error_message().lower()

    elif expected == "error":
        assert login_page.is_error_visible(), \
            f"Expected error for user '{username}'"
