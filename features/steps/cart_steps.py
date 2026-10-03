"""Кроки сценарію кошика."""
# pylint: disable=no-name-in-module,not-callable
from behave import then, when

from pages.cart_page import CartPage


@when('I add "{product}" to the cart')
def add_to_cart(context, product):
    context.inventory_page.add_product_to_cart(product)


@then("the cart badge should show {count:d}")
def verify_cart_badge(context, count):
    actual = context.inventory_page.get_cart_count()
    assert actual == count, f"На значку кошика {actual}, очікувалось {count}"


@when("I open the cart")
def open_cart(context):
    context.inventory_page.open_cart()


@then('the cart should contain "{product}"')
def verify_cart_content(context, product):
    cart_page = CartPage(context.driver)
    assert cart_page.get_title_text() == "Your Cart"
    names = cart_page.get_item_names()
    assert names == [product], f"У кошику: {names}"
