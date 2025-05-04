from conftest import Pages, TestData
from tests.ui.pages.profile_page import ProfilePage
from faker import Faker
from models.enums import Category
import pytest

fake = Faker()
TEST_CATEGORY = fake.text(10)

pytestmark = [pytest.mark.allure_label("Profile", label_type="epic")]


@Pages.profile_page
def test_title_in_page(profile_page_object: ProfilePage):
    profile_page_object.profile_title_text_exist()


@Pages.profile_page
def test_add_categories(category_db_clean, profile_page_object: ProfilePage):
    profile_page_object.add_category(Category.SCHOOL)
    profile_page_object.should_have_category(Category.SCHOOL)


@Pages.profile_page
@TestData.category(Category.SCHOOL)
def test_update_categories(category, profile_page_object: ProfilePage):
    name_category = category.name
    profile_page_object.click_edit_category(name_category)
    profile_page_object.clear_category()
    profile_page_object.update_category()
    profile_page_object.should_have_category(profile_page_object.update_category_text)
