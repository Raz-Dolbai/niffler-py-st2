from selene import browser, have, by
from tests.ui.locators import ProfileLocators
from tests.ui.pages.base_page import BasePage
import allure


class ProfilePage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"
        self.title_profile = "Profile"
        self.title_categories = "Categories"
        self.update_category_text = "TEST_CATEGORY"

    @allure.step("Check: title exist")
    def profile_title_text_exist(self):
        assert browser.element(ProfileLocators.PROFILE_TITLE).should(
            have.text(self.title_profile))
        assert browser.element(ProfileLocators.CATEGORIES_TITLE).should(
            have.text(self.title_categories))

    @allure.step("Add category")
    def add_category(self, category: str):
        browser.element(ProfileLocators.CATEGORIES_INPUT).set_value(category).press_enter()

    @allure.step("Check: category name on page")
    def should_have_category(self, text: str):
        assert browser.element(ProfileLocators.CATEGORIES_DIV).should(
            have.text(text))

    @allure.step("Click Edit category")
    def click_edit_category(self, name_category: str):
        browser.element(by.text(name_category)).click()

    @allure.step("Clear category placeholder")
    def clear_category(self):
        browser.element(ProfileLocators.CATEGORY_UPDATE).clear()

    @allure.step("Update category")
    def update_category(self):
        browser.element(ProfileLocators.CATEGORY_UPDATE).set_value(self.update_category_text).press_enter()
