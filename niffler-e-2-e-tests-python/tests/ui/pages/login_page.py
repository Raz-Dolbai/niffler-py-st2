from selene import browser, have, by
from tests.ui.locators import LoginLocators
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"

    def fill_username(self, username: str):
        browser.element(LoginLocators.USERNAME).set_value(username)

    def fill_password(self, password: str):
        browser.element(LoginLocators.PASSWORD).set_value(password)

    def click_log_in(self):
        browser.element(LoginLocators.LOGIN).click()

    def click_create_new_account(self):
        pass

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_log_in()

    def invalid_auth_credential_text(self):
        assert browser.element(LoginLocators.ERROR_MESSAGE).should(
            have.text(self.expected_invalid_auth_credential_text))

    def invalid_auth_credential_url(self):
        assert browser.should(have.url_containing("/login?error"))

    def success_auth_url(self):
        assert browser.should(have.url_containing("/main"))
