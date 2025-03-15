from tests.ui.locators import RegisterLocators
from selene import browser, have

from tests.ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self):
        self.expected_success_register_text = "Congratulations! You've registered!"
        self.expected_password_not_equal_text = "Passwords should be equal"
        self.expected_not_valid_user_data_text = "Allowed username length should be from 3 to 50 characters"
        self.expected_not_valid_password_text = "Allowed password length should be from 3 to 12 characters"

    def fill_username(self, username: str):
        browser.element(RegisterLocators.USERNAME).set_value(username)

    def fill_password(self, password: str):
        browser.element(RegisterLocators.PASSWORD).set_value(password)

    def fill_submit_password(self, password: str):
        browser.element(RegisterLocators.SUBMIT_PASSWORD).set_value(password)

    def click_sign_up(self):
        browser.element(RegisterLocators.SIGN_UP_BUTTON).click()

    def success_text_after_register(self):
        assert browser.element(RegisterLocators.SUCCESS_TEXT).should(
            have.text(self.expected_success_register_text))

    def password_not_equal(self):
        assert browser.element(RegisterLocators.ERROR).should(have.text(self.expected_password_not_equal_text))

    def username_not_valid(self):
        assert browser.element(RegisterLocators.ERROR).should(have.text(self.expected_not_valid_user_data_text))

    def password_not_valid(self):
        assert browser.element(RegisterLocators.ERROR).should(have.text(self.expected_not_valid_password_text))

    def register_user(self, username: str, password: str, submit_password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.fill_submit_password(submit_password)
        self.click_sign_up()
