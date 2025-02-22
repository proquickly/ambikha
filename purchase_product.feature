Feature: As a cuustomer I want to purchase a product.

  Scenario: I can search for a and purchase a single product.
    Given I am on the home page
    When I select the purchase option
    Then I am taken to a search screen
    And I can search to find the product I want
    And I can add that product to me Cart
    And then order the product

