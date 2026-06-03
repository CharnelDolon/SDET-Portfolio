import pytest


@pytest.mark.ui
@pytest.mark.regression
class TestInventory:

    def test_inventory_loads(self, inventory_page):
        """Inventory page loads with items visible."""
        assert inventory_page.is_loaded()

    def test_inventory_has_six_items(self, inventory_page):
        """Exactly 6 products are displayed."""
        assert inventory_page.get_item_count() == 6

    def test_add_single_item_to_cart(self, inventory_page):
        """Adding one item updates the cart badge to 1."""
        inventory_page.add_item_to_cart(0)
        assert inventory_page.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, inventory_page):
        """Adding 3 items updates the cart badge to 3."""
        for i in range(3):
            inventory_page.add_item_to_cart(i)
        assert inventory_page.get_cart_count() == 3

    def test_sort_by_price_low_to_high(self, inventory_page):
        """Sorting low-to-high returns prices in ascending order."""
        inventory_page.sort_by("lohi")
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_by_price_high_to_low(self, inventory_page):
        """Sorting high-to-low returns prices in descending order."""
        inventory_page.sort_by("hilo")
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices, reverse=True)

    def test_sort_by_name_a_to_z(self, inventory_page):
        """Sorting A→Z returns names in alphabetical order."""
        inventory_page.sort_by("az")
        names = inventory_page.get_item_names()
        assert names == sorted(names)

    def test_all_items_have_positive_price(self, inventory_page):
        """All product prices are greater than zero."""
        prices = inventory_page.get_item_prices()
        assert all(p > 0 for p in prices)
