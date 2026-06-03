from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):

    URL = BASE_URL

    # Locators
    USERNAME_INPUT  = "#user-name"
    PASSWORD_INPUT  = "#password"
    LOGIN_BUTTON    = "#login-button"
    ERROR_MESSAGE   = "[data-test='error']"

    def navigate(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.page.inner_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.page.is_visible(self.ERROR_MESSAGE)
