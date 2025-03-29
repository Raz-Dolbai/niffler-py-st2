from selene import browser, have
from tests.ui.pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"
        self.username_field = "input[name=username]"
        self.password_field = "input[name=password]"
        self.login_button = "button[type=submit]"
        self.error_message = ".form__error"
        self.create_new_account_button = ".form__register"

    @allure.step("Fill username")
    def fill_username(self, username: str):
        browser.element(self.username_field).set_value(username)

    @allure.step("Fill password")
    def fill_password(self, password: str):
        browser.element(self.password_field).set_value(password)

    @allure.step("CLick Log In")
    def click_log_in(self):
        browser.element(self.login_button).click()

    def click_create_new_account(self):
        browser.element(self.create_new_account_button).click()

    @allure.step("Log In")
    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_log_in()

    @allure.step("Check: Authorization failed text")
    def should_be_expected_text_after_invalid_auth(self):
        assert browser.element(self.error_message).should(
            have.text(self.expected_invalid_auth_credential_text))

    @allure.step("Check: Authorization failed url")
    def should_be_expected_url_after_invalid_auth(self):
        assert browser.should(have.url_containing("/login?error"))

    @allure.step("Check: Authorization success url")
    def should_be_expected_url_after_success_auth(self):
        assert browser.should(have.url_containing("/main"))

    @allure.step("Check: Go to register page after click Create New Account Button")
    def should_be_register_page(self):
        assert browser.should(have.url_containing("/register"))
