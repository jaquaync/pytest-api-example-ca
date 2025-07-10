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


@pytest.fixture
# create a pet
def new_pet():
    unique_id = uuid.uuid4().int >> 96
    pet_data = {
        "id": unique_id,
        "name": f"Mochi-{unique_id}",
        "type": "dog",
        "status": "available"
    }
    # run the request to create the pet and get the response code
    response = api_helpers.post_api_data("/pets/", pet_data)
    assert response.status_code == 201
    return pet_data


@pytest.fixture
# create an order
def new_order(new_pet):
    order_data = {
        "pet_id": new_pet["id"]
    }
    # run the request to create the order and get the response code
    response = api_helpers.post_api_data("/store/order", order_data)
    assert response.status_code == 201
    return response.json()


# patch the order
def test_patch_order_by_id(new_order):
    validate(instance=new_order, schema=schemas.order)
    order_id = new_order["id"]
    # run the patch request and get the response code
    updated_status = {"status": "sold"}
    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", updated_status)
    assert patch_response.status_code == 200
    # verify the response message
    response_json = patch_response.json()
    assert_that(response_json["message"], contains_string("Order and pet status updated successfully"))
