import pytest
from utils.helpers import generate_user


@pytest.mark.ui
@pytest.mark.regression
class TestCheckout:

    def test_full_purchase_flow(self, inventory_page, cart_page):
        """User can add an item, checkout, and complete a purchase."""
        user = generate_user()

        inventory_page.add_item_to_cart(0)
        cart_page.open_cart()
        assert cart_page.get_cart_item_count() == 1

        cart_page.proceed_to_checkout()
        cart_page.fill_checkout_info(user["first_name"], user["last_name"], user["zip_code"])
        cart_page.finish_order()

        confirmation = cart_page.get_confirmation_message()
        assert "thank you" in confirmation.lower()

    def test_checkout_requires_first_name(self, inventory_page, cart_page):
        """Checkout fails when first name is missing."""
        inventory_page.add_item_to_cart(0)
        cart_page.open_cart()
        cart_page.proceed_to_checkout()
        cart_page.fill_checkout_info("", "Doe", "12345")
        error = cart_page.page.inner_text("[data-test='error']")
        assert "first name" in error.lower()

    def test_checkout_requires_last_name(self, inventory_page, cart_page):
        """Checkout fails when last name is missing."""
        inventory_page.add_item_to_cart(0)
        cart_page.open_cart()
        cart_page.proceed_to_checkout()
        cart_page.fill_checkout_info("John", "", "12345")
        error = cart_page.page.inner_text("[data-test='error']")
        assert "last name" in error.lower()

    def test_checkout_requires_zip(self, inventory_page, cart_page):
        """Checkout fails when zip code is missing."""
        inventory_page.add_item_to_cart(0)
        cart_page.open_cart()
        cart_page.proceed_to_checkout()
        cart_page.fill_checkout_info("John", "Doe", "")
        error = cart_page.page.inner_text("[data-test='error']")
        assert "postal" in error.lower() or "zip" in error.lower()
