"""Page Object сторінки входу Swag Labs."""
from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Сторінка входу."""

    URL = BASE_URL

    # Локатори — атрибути класу, тести їх не дублюють
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.XPATH, "//input[@data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input#login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username):
        self.type(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def do_login(self, username, password):
        """Повний сценарій входу: ім'я → пароль → кнопка Login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_text(self):
        return self.get_text(self.ERROR_MESSAGE)
