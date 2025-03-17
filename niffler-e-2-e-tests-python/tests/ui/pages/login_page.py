from selene import browser, have, by
from tests.ui.locators import LoginLocators
from tests.ui.pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"

    @allure.step("Fill username")
    def fill_username(self, username: str):
        browser.element(LoginLocators.USERNAME).set_value(username)

    @allure.step("Fill password")
    def fill_password(self, password: str):
        browser.element(LoginLocators.PASSWORD).set_value(password)

    @allure.step("CLick Log In")
    def click_log_in(self):
        browser.element(LoginLocators.LOGIN).click()

    def click_create_new_account(self):
        pass

    @allure.step("Log In")
    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_log_in()

    @allure.step("Check: Authorization failed text")
    def invalid_auth_credential_text(self):
        assert browser.element(LoginLocators.ERROR_MESSAGE).should(
            have.text(self.expected_invalid_auth_credential_text))

    @allure.step("Check: Authorization failed url")
    def invalid_auth_credential_url(self):
        assert browser.should(have.url_containing("/login?error"))

    @allure.step("Check: Authorization success url")
    def success_auth_url(self):
        assert browser.should(have.url_containing("/main"))
