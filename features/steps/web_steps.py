from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------------
@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

# ------------------------------------------------------------------
# INTERACTION FORM
# ------------------------------------------------------------------
@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@when('I select "{text_string}" from the "{dropdown_name}" dropdown')
def step_impl(context, text_string, dropdown_name):
    element_id = dropdown_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    select = Select(element)
    select.select_by_visible_text(text_string)

# ------------------------------------------------------------------
# Button & Action
# ------------------------------------------------------------------
@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    button_id = button_name.lower().replace(" ", "-") + "-btn"
    element = WebDriverWait(context.driver, 5).until(
        EC.element_to_be_clickable((By.ID, button_id))
    )
    element.click()

@when('I press the "{button_name}" button for "{product_name}"')
def step_impl(context, button_name, product_name):
    """
    Search for a row based on Product Name (2nd column),
then press the (Edit/Delete) button on that row.
    """
    xpath = f"//tr[td[2][contains(.,'{product_name}')]]//button[contains(.,'{button_name}')]"
    element = WebDriverWait(context.driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

# ------------------------------------------------------------------
# ASERSI (Checking)
# ------------------------------------------------------------------
@then('I should see "{message}" in the results')
def step_impl(context, message):
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    results = context.driver.find_element(By.ID, "search_results")
    assert message in results.text

@then('I should not see "{message}" in the results')
def step_impl(context, message):
    """Used to ensure the product has been deleted from the table."""
    results = context.driver.find_element(By.ID, "search_results")
    assert message not in results.text

@then('I should see the message "{message}"')
def step_impl(context, message):
    element = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash_message"))
    )
    assert message in element.text

@then('I should see the "{element_name}" is "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    
    if element.tag_name == 'select':
        actual_value = Select(element).first_selected_option.text
    else:
        actual_value = element.get_attribute('value')
    
    # Normalization to handle 'True' vs 'true'
    assert str(actual_value).strip().lower() == str(text_string).strip().lower()