from pages.base_page import BasePage


class InventoryPage(BasePage):

    URL = "/inventory.html"

    # Locators
    INVENTORY_CONTAINER = ".inventory_list"
    INVENTORY_ITEMS     = ".inventory_item"
    ITEM_NAMES          = ".inventory_item_name"
    ITEM_PRICES         = ".inventory_item_price"
    ADD_TO_CART_BUTTONS = "[data-test^='add-to-cart']"
    CART_BADGE          = ".shopping_cart_badge"
    SORT_DROPDOWN       = "[data-test='product-sort-container']"
    BURGER_MENU         = "#react-burger-menu-btn"
    LOGOUT_LINK         = "#logout_sidebar_link"

    def is_loaded(self) -> bool:
        return self.page.is_visible(self.INVENTORY_CONTAINER)

    def get_item_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEMS).count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICES).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def add_item_to_cart(self, index: int = 0):
        self.page.locator(self.ADD_TO_CART_BUTTONS).nth(index).click()

    def get_cart_count(self) -> int:
        if self.page.is_visible(self.CART_BADGE):
            return int(self.page.inner_text(self.CART_BADGE))
        return 0

    def sort_by(self, option: str):
        """option values: 'az', 'za', 'lohi', 'hilo'"""
        self.page.select_option(self.SORT_DROPDOWN, option)

    def logout(self):
        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)
