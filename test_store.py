import random
import uuid
import pytest
from hamcrest import assert_that, contains_string, is_
from jsonschema.validators import validate
import schemas
import api_helpers

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


def test_patch_order_by_id():
    # Step 1: Create a pet
    pet_data = {
        "id": 999,
        "name": "Mochi",
        "type": "dog",
        "status": "available"
    }
    pet_response = api_helpers.post_api_data("/pets/", pet_data)
    assert pet_response.status_code == 201

    # Step 2: Place an order for the pet
    order_data = {
        "pet_id": pet_data["id"]
    }
    order_response = api_helpers.post_api_data("/store/order", order_data)
    assert order_response.status_code == 201

    # Extract the order ID from the response
    order = order_response.json()
    validate(instance=order, schema=schemas.order)
    order_id = order["id"]

    # Step 3: Patch the order with a new status
    updated_status = {"status": "sold"}
    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", updated_status)
    assert patch_response.status_code == 200

    # Validate the message
    response_json = patch_response.json()
    assert_that(response_json["message"], contains_string("Order and pet status updated successfully"))
