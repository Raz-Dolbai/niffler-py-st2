import pytest
from clients.spends_client import SpendsHttpClient
from conftest import TestData
from models.category import CategoryAdd
from models.enums import Category
import allure
from http import HTTPStatus


@allure.epic("POSITIVE CATEGORY API TESTS")
class TestsPositiveApiCategory:
    @allure.feature("Add Category")
    @allure.story("Create new category")
    def test_add_category(self, spends_client: SpendsHttpClient, category_db_clean):
        spends_client.add_category(CategoryAdd(name=Category.SCHOOL))
        category = spends_client.get_categories()
        with allure.step(f"Category {Category.SCHOOL} created"):
            assert Category.SCHOOL == category[0].name

    @allure.feature("Add Category")
    @allure.story("Create new category with valid character length")
    @pytest.mark.parametrize("category_name",
                             [Category.TEXT_2_CHARACTERS, Category.TEXT_3_CHARACTERS,
                              Category.TEXT_49_ELEMENTS,
                              Category.TEXT_50_ELEMENTS])
    def test_add_valid_categories_characters(self, category_name, spends_client: SpendsHttpClient,
                                             category_db_clean):
        spends_client.add_category(CategoryAdd(name=category_name))
        category = spends_client.get_categories()
        with allure.step(f"Category created"):
            assert category_name == category[0].name

    @allure.feature("Update Category")
    @allure.story("Update name category")
    @TestData.category(Category.SCHOOL)
    def test_update_name_category(self, spends_client: SpendsHttpClient, category):
        spends_client.update_categories(
            CategoryAdd(id=category.id, name=Category.CAR).model_dump())
        get_categories = spends_client.get_categories()
        with allure.step(f"Category name has changed"):
            assert get_categories[0].name == Category.CAR

    @allure.feature("Update Category")
    @allure.story("Moving a category to the archive")
    @TestData.category(Category.SCHOOL)
    def test_update_archived_category(self, spends_client: SpendsHttpClient, category):
        spends_client.update_categories(
            CategoryAdd(id=category.id, archived=True, name=category.name).model_dump())
        get_archived_categories = spends_client.get_categories()
        with allure.step(f"Category {Category.SCHOOL} moving to the archive"):
            assert category.name == get_archived_categories[0].name
            assert category.id == get_archived_categories[0].id
            assert get_archived_categories[0].archived


@allure.epic("NEGATIVE CATEGORY API TESTS")
class TestsNegativeApiCategory:

    @allure.feature("Add Category")
    @allure.story("Unable to create duplicate category")
    @TestData.category(Category.SCHOOL)
    def test_add_duplicate_category(self, spends_client: SpendsHttpClient, category):
        response = spends_client.add_category(
            CategoryAdd(name=Category.SCHOOL))
        with allure.step(f"There is an error message"):
            assert response.status == HTTPStatus.CONFLICT
            assert response.type == "niffler-spend: Bad request "
            assert response.detail == "Cannot save duplicates"
            assert response.instance == "/api/categories/add"

    @allure.feature("Add Category")
    @allure.story("Create new category with not valid character length")
    @pytest.mark.parametrize("category_name",
                             ["L", Category.TEXT_51_ELEMENTS])
    def test_add_not_valid_categories_characters(self, category_name, spends_client: SpendsHttpClient,
                                                 category_db_clean):
        response = spends_client.add_category(CategoryAdd(name=category_name))
        with allure.step(f"There is an error message"):
            assert response.status == HTTPStatus.BAD_REQUEST
            assert response.type == "niffler-gateway: Entity validation error"
            assert response.detail == "Allowed category length should be from 2 to 50 characters"
            assert response.instance == "/api/categories/add"
