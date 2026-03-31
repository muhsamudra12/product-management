import requests
from behave import given

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    # 1. Delete old data
    rest_endpoint = f"{context.base_url}/products"
    context.driver.get(rest_endpoint)
    
    # 2. Get data from the table in the feature file and post it to the API
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'].lower() in ['true', '1', 't'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == 201