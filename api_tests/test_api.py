
import requests
import logging
from logger_config import logger


# 1. GET API TEST
def test_get_user():
    url = "https://jsonplaceholder.typicode.com/users/1"

    logger.info("Starting GET API test")

    response = requests.get(url)

    logger.info(f"GET status code: {response.status_code}")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Leanne Graham"

    logger.info("GET API test passed")


# 2. POST API TEST
def test_create_user():
    url = "https://jsonplaceholder.typicode.com/users"

    user_data = {
        "name": "Shravan",
        "username": "Sunny",
        "email": "sunny@example.com"
    }

    logger.info("Starting POST API test")

    response = requests.post(url, json=user_data)

    logger.info(f"POST status code: {response.status_code}")

    assert response.status_code == 201
    assert response.json()["name"] == "Shravan"
    assert response.json()["username"] == "Sunny"

    logger.info("POST API test passed")


# 3. PATCH API TEST
def test_update_user():
    url = "https://jsonplaceholder.typicode.com/users/1"

    updated_data = {
        "email": "shravan@example.com"
    }

    logger.info("Starting PATCH API test")

    response = requests.patch(url, json=updated_data)

    logger.info(f"PATCH status code: {response.status_code}")

    assert response.status_code == 200
    assert response.json()["email"] == "shravan@example.com"

    logger.info("PATCH API test passed")


# 4. DELETE API TEST
def test_delete_user():
    url = "https://jsonplaceholder.typicode.com/users/1"

    logger.info("Starting DELETE API test")

    response = requests.delete(url)

    logger.info(f"DELETE status code: {response.status_code}")

    assert response.status_code == 200

    logger.info("DELETE API test passed")


# 5. NEGATIVE GET API TEST
def test_get_invalid_user():
    url = "https://jsonplaceholder.typicode.com/users/9999"

    logger.info("Starting negative GET API test")

    response = requests.get(url)

    logger.info(f"Negative GET status code: {response.status_code}")

    assert response.status_code == 404

    logger.info("Negative GET API test passed")

# 6. PUT API TEST
def test_replace_user():
    url = "https://jsonplaceholder.typicode.com/users/1"

    updated_data = {
        "id": 1,
        "name": "Shravan Kumar",
        "username": "Sunny",
        "email": "shravan@example.com"
    }

    logger.info("Starting PUT API test")

    response = requests.put(url, json=updated_data)

    logger.info(f"PUT status code: {response.status_code}")

    assert response.status_code == 200
    assert response.json()["name"] == "Shravan Kumar"
    assert response.json()["email"] == "shravan@example.com"

    logger.info("PUT API test passed")

# 7. API RESPONSE TIME TEST

def test_api_response_time():

    url = "https://jsonplaceholder.typicode.com/users/1"

    logger.info("Starting API response time test")

    response = requests.get(url)

    response_time = response.elapsed.total_seconds()

    print("API Response Time:", response_time, "seconds")

    logger.info(f"API response time: {response_time} seconds")

    assert response.status_code == 200

    assert response_time < 2

    logger.info("API response time test passed")

# 8. API HEADERS TEST

def test_api_headers():

    url = "https://jsonplaceholder.typicode.com/users/1"

    logger.info("Starting API headers test")

    response = requests.get(
        url,
        headers={
            "Accept": "application/json"
        }
    )

    print("Response Status:", response.status_code)
    print("Response Headers:", response.headers)

    logger.info(f"Response status: {response.status_code}")

    assert response.status_code == 200
    assert "application/json" in response.headers.get(
        "Content-Type", ""
    )

    logger.info("API headers test passed")
