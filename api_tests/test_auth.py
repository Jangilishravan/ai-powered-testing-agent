import requests
from logger_config import logger

def test_bearer_token():

    url = "https://httpbin.org/bearer"

    headers = {
        "Authorization": "Bearer abc123"
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)
    print("Response:", response.text)
    print("Response JSON:", response.json())
    print("Authorization:", response.request.headers.get("Authorization"))

def test_missing_token():

    url = "https://httpbin.org/bearer"

    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

def test_invalid_token():

    url = "https://httpbin.org/bearer"

    headers = {
        "Authorization": "Bearer invalid123"
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200

def test_valid_user_token():

    logger.info("Starting valid user token test")

    url = "http://127.0.0.1:5000/profile"

    headers = {
        "Authorization": "Bearer sunny123"
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    logger.info("Valid user token test passed")

def test_invalid_token_local():

    logger.info("Starting invalid token test")

    url = "http://127.0.0.1:5000/profile"

    headers = {
        "Authorization": "Bearer wrong123"
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401

    logger.info("Invalid token test passed")

def test_admin_access_denied():

    logger.info("Starting admin access denied test")

    url = "http://127.0.0.1:5000/admin"

    headers = {
        "Authorization": "Bearer sunny123"
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 403

    logger.info("Admin access denied test passed")

def test_admin_access_success():

    logger.info("Starting admin access success test")

    url = "http://127.0.0.1:5000/admin"

    headers = {
        "Authorization": "Bearer admin123"
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    logger.info("Admin access success test passed")

def test_missing_token_local():

    logger.info("Starting missing token test")

    url = "http://127.0.0.1:5000/profile"

    response = requests.get(url)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401

    logger.info("Missing token test passed")

def test_invalid_auth_format():

    logger.info("Starting invalid auth format test")

    url = "http://127.0.0.1:5000/profile"

    headers = {
        "Authorization": "Token sunny123"
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401

    logger.info("Invalid auth format test passed")

def test_unsupported_http_method():

    logger.info("Starting unsupported HTTP method test")

    url = "http://127.0.0.1:5000/profile"

    response = requests.post(url)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 405

    logger.info("Unsupported HTTP method test passed")

def test_empty_login_request():

    logger.info("Starting empty login request test")

    url = "http://127.0.0.1:5000/login"

    response = requests.post(url, json={})

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Empty login request test passed") 

def test_missing_login_credentials():

    logger.info("Starting missing login credentials test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "",
        "password": ""
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Missing login credentials test passed")  

def test_missing_password():

    logger.info("Starting missing password test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Missing password test passed")

def test_missing_username():

    logger.info("Starting missing username test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "password": "sunny123"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Missing username test passed")

def test_invalid_username_data_type():

    logger.info("Starting invalid username data type test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": 12345,
        "password": "sunny123"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Invalid username data type test passed")

def test_invalid_password_data_type():
    logger.info("Starting invalid password data type test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny",
        "password": 12345
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")
    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Invalid password data type test passed")

def test_whitespace_username():
    logger.info("Starting whitespace username test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "   ",
        "password": "sunny123"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")
    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Whitespace username test passed")

def test_whitespace_password():
    logger.info("Starting whitespace password test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny",
        "password": "   "
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")
    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    logger.info("Whitespace password test passed")

def test_valid_login_credentials():
    logger.info("Starting valid login credentials test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny",
        "password": "sunny123"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")
    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    logger.info("Valid login credentials test passed")

def test_empty_password():

    logger.info("Starting empty password test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny",
        "password": ""
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400
    assert response.json()["error"] == "Password is required"

    logger.info("Empty password test passed")


def test_invalid_username_format():

    logger.info("Starting invalid username format test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "sunny@123",
        "password": "sunny123"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400
    assert response.json()["error"] == "Username format is invalid"

    logger.info("Invalid username format test passed")

def test_sql_injection_input_rejected():

    logger.info("Starting SQL injection input test")

    url = "http://127.0.0.1:5000/login"

    payload = {
        "username": "' OR '1'='1",
        "password": "anything"
    }

    response = requests.post(url, json=payload)

    logger.info(f"Response status: {response.status_code}")

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 400

    assert response.json()["error"] == "Username format is invalid"

    logger.info("SQL injection input test passed")

    
    
