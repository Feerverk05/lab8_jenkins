"""Page Object сторінки кошика (cart.html)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """Сторінка кошика."""

    TITLE = (By.CSS_SELECTOR, "span.title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_item_names(self):
        return [item.text for item in self.find_all(self.ITEM_NAMES)]
