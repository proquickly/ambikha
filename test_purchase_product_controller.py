import pytest
from pytest_bdd import scenarios, given, when, then

# Import the functions to be tested
from purchase_product import (
    goto_home,
    select_purchase,
    goto_product_search,
    search_for_product,
    add_product_to_cart_,
    order_product
)

# Define the feature file to be used for the tests
scenarios('purchase_product.feature')

@given('I am on the home page')
def test_goto_home():
    with pytest.raises(NotImplementedError):
        goto_home()

@when('I select the purchase option')
def test_select_purchase():
    with pytest.raises(NotImplementedError):
        select_purchase()

@then('I am taken to a search screen')
def test_goto_product_search():
    with pytest.raises(NotImplementedError):
        goto_product_search()

@then('I can search to find the product I want')
def test_search_for_product():
    with pytest.raises(NotImplementedError):
        search_for_product()

@then('I can add that product to me Cart')
def test_add_product_to_cart_():
    with pytest.raises(NotImplementedError):
        add_product_to_cart_()

@then('then order the product')
def test_order_product():
    with pytest.raises(NotImplementedError):
        order_product()