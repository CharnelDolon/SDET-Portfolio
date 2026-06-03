from playwright.sync_api import Page


class BasePage:
    """All page objects inherit from this. Holds the page instance
    and common utilities like navigation and screenshot helpers."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str = ""):
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str):
        self.page.screenshot(path=f"reports/{name}.png")
