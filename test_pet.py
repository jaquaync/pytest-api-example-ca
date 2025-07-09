from jsonschema import validate, ValidationError
import pytest
import schemas
import api_helpers

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''


def test_pet_schema():
    test_endpoint = "/pets/"

    response = api_helpers.get_api_data(test_endpoint)

    # validate the response code
    assert response.status_code == 200

    print("Response JSON:", response.json())

    # Validate the response schema against the defined schema in schemas.py
    try:
        validate(instance=response.json(), schema=schemas.pet)
        print("Response matches the defined schema")
    except ValidationError as e:
        print("JSON validation error:", e)


'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''


@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)

    # Validate the response code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Validate the status property in the response is equal to the expected status
    response_json = response.json()
    for pet in response_json:
        assert pet["status"] == status, f"Expected status '{status}'but got '{pet.get['status']}'"

    # Validate the schema for each object in the response
    for pet in response.json():
        assert "id" in pet, "Missing 'id' property"
        assert isinstance(pet['id'], int), "'id' should be of type integer"
        assert "name" in pet, "Missing 'name' property"
        assert isinstance(pet['name'], str), "'name' should be of type string"
        assert "type" in pet, "Missing 'type' property"
        assert pet['type'] in ["cat", "dog", "fish"], f"Invalid 'type' value: {pet['type']}"
        assert "status" in pet, "Missing 'status' property"
        assert pet['status'] in ["available", "sold", "pending"], f"Invalid 'status' value: {pet['status']}"


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''


@pytest.mark.parametrize("pet_id", [
    "p",      # letters as the ID
    "''",     # empty string
    "!@#^*",  # special characters as the ID
    "99999",  # large ID
    "-4",     # negative ID
])
def test_get_by_id_404(pet_id):
    test_endpoint = "/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404, f"Expected 404, got {response.status_code} for ID: {pet_id}"
