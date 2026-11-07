class LoginPage:

    def __init__(self, page):
        self.page = page

        # Locators
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.get_by_role(
            "button", name="Login"
        )
        self.error_message = page.locator(
            "[data-test='error']"
        )

    def open(self):
        self.page.goto("https://www.saucedemo.com/")

    def enter_username(self, username):
        self.username.fill(username)

    def enter_password(self, password):
        self.password.fill(password)

    def click_login(self):
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.inner_text()