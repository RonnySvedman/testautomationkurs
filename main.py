import requests
import pytest
import time


# DEMOVERSION....
def test_create_pet_in_petstore_version_one():
    json_dict = {"id": 0, "category": {"id": 0, "name": "Bambi"}, "name": "dog", "photoUrls": [],
                 "tags": [{"id": 0, "name": "poodle"}], "status": "available"}
    # Creates a POST request to the URL, with a JSON as body
    # Response is saved to variable response and is an object of type Response
    response = requests.post("https://petstore.swagger.io/v2/pet", json=json_dict)
    # Response object has different methods which you can use to get different stuff.
    response.headers.values()  # Dictionary of HTTP headers with keys and their values
    print(response.headers.get("Date"))
    print(response.status_code)  # This prints the HTTP status code of the response

"""
def test_simple_json_string_ugly():
    url = "https://petstore.swagger.io/v2/pet"

    json_dict = {"id": 0, "category": {"id": 0, "name": "Bambi"}, "name": "dog", "photoUrls": [], "tags": [
        {"id": 0, "name": "poodle"}], "status": "available"}
    expected_media_type = "application/json"
    response = requests.post(url, json=json_dict)
    assert response.status_code == 200
    header_content_type = response.headers.get("content-type")
    assert header_content_type == expected_media_type
    assert response.headers["Content-Type"] == "application/json"  # One line to test Content-Type
    response_body = response.json()  # This will create a dict from the body, which was a JSON string
    print(response_body)
"""

# Here asserts should be on response_body, the important data


# This is a helper function to create
def create_pet_in_petstore(id: int):
    """This will create a pet in Petstore"""
    url = "https://petstore.swagger.io/v2/pet"
    json_dict = {"id": 0, "category": {"id": 0, "name": "FizzBuzz"}, "name": "BuzzFizz", "photoUrls": [],
                 "tags": [{"id": 0, "name": "poodle"}], "status": "available"}
    json_dict.update({"id": id})  # Update id in our Pet, to make it different
    response = requests.post(url, json=json_dict)
    return response  # returns the whole response


def test_create_pet_in_petstore_version2():
    response = create_pet_in_petstore(13374711)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()  # a dict of the whole body
    assert response_body["id"] == 13374711


def test_create_pet_from_petstore():
    # arrange
    pet_id = 133747114219
    the_pet = create_pet_in_petstore(pet_id)
    url = (f"https://petstore.swagger.io/v2/pet/{pet_id}")

    # Act
    response = requests.get(url)
    # assert
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == the_pet.json()


# This is a helper function to update a pet

def update_pet_category_name_in_petstore(id: int, name: str):
    url = "https://petstore.swagger.io/v2/pet"
    json_dict = requests.get(url + "/" + str(id)).json()
    json_dict.get("category").update({"name": name})
    response = requests.put(url, json=json_dict)
    return response  # returns the whole response


def test_update_pet_in_petstore():
    pet_id = 133747111914
    create_pet_in_petstore(pet_id)  # "NAME fIZZbUZZ"
    url = "https://petstore.swagger.io/v2/pet"
    updated_pet = update_pet_category_name_in_petstore(pet_id, "barbaz")
    time.sleep(5)
    pet_now_in_database = requests.get(url + "/" + str(pet_id))
    assert updated_pet.status_code == 200
    assert pet_now_in_database.status_code == 200
    assert updated_pet.headers["Content-Type"] == "application/json"
    assert pet_now_in_database.headers["Content-Type"] == "application/json"
    assert pet_now_in_database.json() == updated_pet.json()


# bygga en fixture som skara en pet, yieldar ett id och sedan deletar den igen?


# def test_get_testpersonnummer_from_skatteverket()

def test_delete_pet_from_petstore():
    pet_id = 133747112022
    create_pet_in_petstore(pet_id)
    url = "https://petstore.swagger.io/v2/pet/"+str(pet_id)
    response=requests.delete(url)
    time.sleep(5)
    assert response.status_code==200
    assert response.json()["message"] == str(pet_id)
    assert requests.get(url + "/" + str(pet_id)).status_code == 404

