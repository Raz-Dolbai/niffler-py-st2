from selene import browser, have, by
from tests.ui.locators import ProfileLocators
from tests.ui.pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"
        self.title_profile = "Profile"
        self.title_categories = "Categories"
        self.update_category_text = "TEST_CATEGORY"

    def profile_title_text_exist(self):
        browser.element(ProfileLocators.PROFILE_TITLE).should(
            have.text(self.title_profile))
        browser.element(ProfileLocators.CATEGORIES_TITLE).should(
            have.text(self.title_categories))

    def add_category(self, category: str):
        browser.element(ProfileLocators.CATEGORIES_INPUT).set_value(category).press_enter()

    def should_have_category(self, text: str):
        browser.element(ProfileLocators.CATEGORIES_DIV).should(
            have.text(text))

    def click_edit_category(self, name_category: str):
        browser.element(by.text(name_category)).click()

    def clear_category(self):
        browser.element(ProfileLocators.CATEGORY_UPDATE).clear()

    def update_category(self):
        browser.element(ProfileLocators.CATEGORY_UPDATE).set_value(self.update_category_text).press_enter()
