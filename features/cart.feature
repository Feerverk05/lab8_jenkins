@ui @cart
Feature: Shopping Cart
  As a logged-in customer
  I want to add products to the cart
  So that I can buy them later

  Scenario: Add a backpack to the cart
    Given I am logged in as "standard_user" with password "secret_sauce"
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show 1
    When I open the cart
    Then the cart should contain "Sauce Labs Backpack"
