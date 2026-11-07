from logger_config import logger
import os
import pytest
import json

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


# Load test data from JSON
with open("test_data/login_data.json", "r") as file:
    test_data = json.load(file)
def capture_screenshot(page, test_name):

    os.makedirs("screenshots", exist_ok=True)

    screenshot_path = os.path.abspath(
        f"screenshots/{test_name}.png"
    )

    page.screenshot(
        path=screenshot_path,
        full_page=True
    )

    print(f"Screenshot saved at: {screenshot_path}")


@pytest.fixture(scope="function")
def browser_page():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        yield page

        browser.close()


@pytest.mark.parametrize("data", test_data, ids=[
    test["id"] for test in test_data
])
def test_login(browser_page, data):

    login = LoginPage(browser_page)

    logger.info(f"Starting test: {data['id']}")

    try:
        # Step 1: Open website
        login.open()
        logger.info("Website opened successfully")

        # Step 2: Enter username
        login.enter_username(data["username"])
        logger.info("Username entered")

        # Step 3: Enter password
        login.enter_password(data["password"])
        logger.info("Password entered")

        # Step 4: Click login
        login.click_login()
        logger.info("Login button clicked")

        # Step 5: Validate result
        if data["expected"] == "success":

            assert browser_page.locator(
                ".title"
            ).inner_text() == "Products"

        else:

            error = login.get_error_message()

            if data["username"] == "" and data["password"] == "":
                assert error == "Epic sadface: Username is required"

            else:
                assert error == (
                    "Epic sadface: Username and password "
                    "do not match any user in this service"
                )

        logger.info(f"Test passed: {data['id']}")
        print(f"Test completed: {data['id']}")

    except Exception:
        logger.exception(f"Test failed: {data['id']}")
        capture_screenshot(browser_page, data["id"])
        raise
    