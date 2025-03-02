import time
from selene import browser, have, by
from conftest import Pages, TestData
from tests.ui.locators import ProfilePage
from faker import Faker

fake = Faker()
TEST_CATEGORY = fake.text(10)


@Pages.profile_page
def test_title_in_page():
    browser.element(ProfilePage.PROFILE_TITLE).should(
        have.text('Profile'))
    browser.element(ProfilePage.CATEGORIES_TITLE).should(
        have.text('Categories'))


@Pages.profile_page
def test_add_categories(category_db_clean):
    browser.element(ProfilePage.CATEGORIES_INPUT).set_value("investments").press_enter()
    browser.element(ProfilePage.CATEGORIES_DIV).should(
        have.text('investments'))


@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_update_categories(category):
    name_category = category
    time.sleep(5)
    browser.element(by.text(name_category)).click()
    browser.element(ProfilePage.CATEGORY_UPDATE).clear()
    browser.element(ProfilePage.CATEGORY_UPDATE).set_value("TEST_CATEGORY").press_enter()
    time.sleep(5)
    browser.element(ProfilePage.CATEGORIES_DIV).should(
        have.text('TEST_CATEGORY'))
