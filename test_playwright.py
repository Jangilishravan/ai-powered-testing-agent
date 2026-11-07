from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.saucedemo.com/")

    # Enter invalid login details
    page.locator("#user-name").fill("wrong_user")
    page.locator("#password").fill("wrong_password")

    page.get_by_role("button", name="Login").click()

    # Verify the error message
    error_message = page.locator("[data-test='error']").inner_text()

    assert "Username and password do not match" in error_message

    print("TEST PASSED: Invalid login correctly rejected!")

    browser.close()
