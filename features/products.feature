Feature: Product Service Administration
  As a Product Store Administrator
  I want to manage the product catalogue
  So that I can keep the inventory up to date

  Background:
    Given the following products
      | name       | category    | price | available | description |
      | Laptop     | Electronics | 800   | True      | High-end gaming laptop |
      | iPhone     | Electronics | 1000  | True      | Latest smartphone |
      | T-Shirt    | Apparel     | 20    | True      | Cotton shirt |
      | Headphones | Electronics | 150   | False     | Noise cancelling |

  Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see "Laptop" in the results
    When I press the "Edit" button for "Laptop"
    Then I should see the "Name" is "Laptop"
    And I should see the "Category" is "Electronics"

  Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    And I press the "Edit" button for "Laptop"
    And I set the "Name" to "Gaming Laptop"
    And I press the "Update" button
    Then I should see the message "Success"