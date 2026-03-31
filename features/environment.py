import os
from selenium import webdriver

# Application address
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

def before_all(context):
    """ Executed once before all tests """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # So that the browser does not appear (runs in the background)
    options.add_argument("--no-sandbox")
    context.driver = webdriver.Chrome(options=options)
    context.base_url = BASE_URL

def after_all(context):
    """ Executed after all tests """
    context.driver.quit()