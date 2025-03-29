from selene import browser, have, by
from tests.ui.pages.base_page import BasePage
import allure


class ProfilePage(BasePage):
    def __init__(self):
        self.expected_invalid_auth_credential_text = "Неверные учетные данные пользователя"
        self.title_profile = "Profile"
        self.title_categories = "Categories"
        self.update_category_text = "TEST_CATEGORY"
        self.PROFILE_TITLE = ".MuiTypography-root.MuiTypography-h5.css-w1t7b3"
        self.CATEGORIES_TITLE = ".MuiTypography-root.MuiTypography-h5.css-1pam1gy"
        self.CATEGORIES_INPUT = "input[name=category]"
        self.SAVE_CHANGES_BUTTON = "[id=:r5:]"
        self.CATEGORIES_DIV = ".MuiBox-root.css-1lekzkb"
        self.EDIT_CATEGORY_NAME = "#root > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.css-17u3xlq > div > div.MuiBox-root.css-0 > button:nth-child(1)"
        self.ARCHIVE_CATEGORY = "#root > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.css-17u3xlq > div > div.MuiBox-root.css-0 > button:nth-child(2)"
        self.CATEGORY_UPDATE = ".MuiBox-root.css-1kxonj9 > [name=category]"

    @allure.step("Check: title exist")
    def profile_title_text_exist(self):
        assert browser.element(self.PROFILE_TITLE).should(
            have.text(self.title_profile))
        assert browser.element(self.CATEGORIES_TITLE).should(
            have.text(self.title_categories))

    @allure.step("Add category")
    def add_category(self, category: str):
        browser.element(self.CATEGORIES_INPUT).set_value(category).press_enter()

    @allure.step("Check: category name on page")
    def should_have_category(self, text: str):
        assert browser.element(self.CATEGORIES_DIV).should(
            have.text(text))

    @allure.step("Click Edit category")
    def click_edit_category(self, name_category: str):
        browser.element(by.text(name_category)).click()

    @allure.step("Clear category placeholder")
    def clear_category(self):
        browser.element(self.CATEGORY_UPDATE).clear()

    @allure.step("Update category")
    def update_category(self):
        browser.element(self.CATEGORY_UPDATE).set_value(self.update_category_text).press_enter()
