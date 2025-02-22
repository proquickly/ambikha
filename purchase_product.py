"""As a cuustomer I want to purchase a product. feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('purchase_product.feature', 'I can search for a and purchase a single product.')
def test_i_can_search_for_a_and_purchase_a_single_product():
    """I can search for a and purchase a single product.."""


@given('I am on the home page')
def goto_home():
    """I am on the home page."""
    raise NotImplementedError


@when('I select the purchase option')
def select_purchase():
    """I select the purchase option."""
    raise NotImplementedError


@then('I am taken to a search screen')
def goto_product_search():
    """I am taken to a search screen."""
    raise NotImplementedError


@then('I can search to find the product I want')
def search_for_product():
    """I can search to find the product I want."""
    raise NotImplementedError

@then('I can add that product to me Cart')
def add_product_to_cart_():
    """I can add that product to me Cart."""
    raise NotImplementedError


@then('then order the product')
def order_product():
    """then order the product."""
    raise NotImplementedError

