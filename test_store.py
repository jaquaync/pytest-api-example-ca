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
def create_order():
    existing_pet_id = 2
    new_order = {
        "pet_id": existing_pet_id
    }
    response = api_helpers.post_api_data("/store/order", new_order)
    print("Order creation response:", response.text)
    assert response.status_code == 201
    return response.json()


# Updating the order with a new pet_id
def test_patch_order_by_id(create_order):
    updated_data = {
        "pet_id": 1
    }

    order_id = create_order["id"]
    response = api_helpers.patch_api_data(f"/store/order/{order_id}", updated_data)
    print("Patch response:", response.text)

    # Validate status code
    assert response.status_code == 200

    # Validate response structure
    response_json = response.json()
    validate(instance=response_json.get("order"), schema=schemas.order)
    validate(instance=response_json.get("pet"), schema=schemas.pet)

    # Validate response message
    expected_message = "Order and pet status updated successfully"
    assert_that(response_json.get("message"), is_(expected_message))

    # Assert updated values
    assert_that(response_json["order"]["pet_id"], is_(1))
    assert_that(response_json["pet"]["status"], is_("sold"))


def test_patch_with_invalid_pet_id():
    # Attempt patch with non-existent pet_id
    fake_order_id = "fake pet"
    patch_data = {
        "pet_id": 999
    }

    response = api_helpers.patch_api_data(f"/store/order/{fake_order_id}", patch_data)
    print("Invalid patch response:", response.text)

    # Validate failure code (adjust depending on API behavior)
    assert response.status_code in [400, 404]
    assert_that(response.text, contains_string("not found"))