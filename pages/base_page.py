"""Базовий клас для всіх сторінок: спільні дії з явними очікуваннями."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Спільні дії для всіх сторінок."""

    TIMEOUT = 10  # секунд очікування елемента

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def find(self, locator):
        """Чекає, поки елемент стане видимим, і повертає його."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text
