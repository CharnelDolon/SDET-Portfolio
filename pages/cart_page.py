from pages.base_page import BasePage


class CartPage(BasePage):

    CART_ICON       = ".shopping_cart_link"
    CART_ITEMS      = ".cart_item"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    REMOVE_BUTTONS  = "[data-test^='remove']"
    FIRST_NAME      = "[data-test='firstName']"
    LAST_NAME       = "[data-test='lastName']"
    ZIP_CODE        = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    FINISH_BUTTON   = "[data-test='finish']"
    COMPLETE_HEADER = ".complete-header"

    def open_cart(self):
        self.page.click(self.CART_ICON)
        self.page.wait_for_url("**/cart.html")

    def get_cart_item_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()

    def proceed_to_checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)

    def fill_checkout_info(self, first: str, last: str, zip_code: str):
        self.page.fill(self.FIRST_NAME, first)
        self.page.fill(self.LAST_NAME, last)
        self.page.fill(self.ZIP_CODE, zip_code)
        self.page.click(self.CONTINUE_BUTTON)

    def finish_order(self):
        self.page.click(self.FINISH_BUTTON)

    def get_confirmation_message(self) -> str:
        return self.page.inner_text(self.COMPLETE_HEADER)
