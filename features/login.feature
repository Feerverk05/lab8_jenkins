@ui @login
Feature: User Login
  As a registered user of the Swag Labs store
  I want to log in to the application
  So that I can see the inventory and buy products

  Background:
    Given I open the Swag Labs login page

  @smoke
  Scenario: Successful login with standard user
    When I enter username "standard_user" and password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page
    And I should see 6 products

  @negative
  Scenario Outline: Login is rejected for invalid credentials
    When I enter username "<username>" and password "<password>"
    And I click the login button
    Then I should see the error message "<error>"
    And I should stay on the login page

    Examples:
      | username        | password       | error                                                       |
      | locked_out_user | secret_sauce   | Sorry, this user has been locked out.                       |
      | standard_user   | wrong_password | Username and password do not match any user in this service |
      | unknown_user    | secret_sauce   | Username and password do not match any user in this service |
