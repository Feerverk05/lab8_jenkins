"""Page Object сторінки товарів (inventory.html)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


def _slug(product_name):
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (так сайт формує id кнопок)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage(BasePage):
    """Сторінка зі списком товарів, що відкривається після входу."""

    TITLE = (By.CSS_SELECTOR, "span.title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CSS_SELECTOR, "span.shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")

    def wait_until_opened(self):
        self.wait.until(EC.url_contains("/inventory.html"))
        return self

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_items_count(self):
        return len(self.find_all(self.INVENTORY_ITEMS))

    def add_product_to_cart(self, product_name):
        """Натискає Add to cart і чекає, поки кнопка зміниться на Remove."""
        self.click((By.ID, f"add-to-cart-{_slug(product_name)}"))
        self.find((By.ID, f"remove-{_slug(product_name)}"))

    def add_backpack_to_cart(self):
        self.add_product_to_cart("Sauce Labs Backpack")

    def get_cart_count(self):
        """Число на значку кошика; 0, якщо значка немає (кошик порожній)."""
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.click(self.CART_LINK)
        self.wait.until(EC.url_contains("/cart.html"))
