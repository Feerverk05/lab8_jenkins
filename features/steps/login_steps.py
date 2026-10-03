"""Кроки сценаріїв входу. Логіка роботи зі сторінками — у класах Page Object (pages/)."""
# behave створює декоратори given/when/then динамічно, тому pylint помилково
# вважає їх відсутніми або невикликними (хибнопозитивні no-name-in-module, not-callable)
# pylint: disable=no-name-in-module,not-callable
from behave import given, then, when

from config import BASE_URL
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@given("I open the Swag Labs login page")
def open_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    assert BASE_URL.rstrip("/") in context.driver.current_url


@given('I am logged in as "{user}" with password "{pwd}"')
def logged_in(context, user, pwd):
    open_login_page(context)
    context.login_page.do_login(user, pwd)
    context.inventory_page = InventoryPage(context.driver).wait_until_opened()


@when('I enter username "{user}" and password "{pwd}"')
def enter_credentials(context, user, pwd):
    context.login_page.enter_username(user)
    context.login_page.enter_password(pwd)


@when("I click the login button")
def click_login(context):
    context.login_page.click_login()


@then("I should be redirected to the inventory page")
def verify_redirect(context):
    context.inventory_page = InventoryPage(context.driver).wait_until_opened()
    assert context.driver.current_url.endswith("/inventory.html")
    title = context.inventory_page.get_title_text()
    assert title == "Products", f'Очікувався заголовок "Products", отримано "{title}"'


@then("I should see {count:d} products")
def verify_products_count(context, count):
    actual = context.inventory_page.get_items_count()
    assert actual == count, f"Очікувалось товарів: {count}, знайдено: {actual}"


@then('I should see the error message "{message}"')
def verify_error(context, message):
    error = context.login_page.get_error_text()
    assert message in error, f'Очікувалось повідомлення "{message}", отримано "{error}"'


@then("I should stay on the login page")
def verify_still_on_login(context):
    assert "inventory.html" not in context.driver.current_url
    assert context.driver.find_element(*LoginPage.LOGIN_BUTTON).is_displayed()
