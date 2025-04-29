import pytest
from clients.user_client import UsersHttpClient
import allure
from models.user import User
from models.enums import Category
from http import HTTPStatus


@allure.epic("POSITIVE USERS API TESTS")
class TestsPositiveApiUsers:
    @allure.feature("Get User")
    @allure.story("Current user is correct")
    def test_get_current_user(self, user_client: UsersHttpClient):
        response = user_client.get_current_user()
        assert response.username == "Raz_2_Three"

    @allure.feature("Update user")
    @allure.story("Update fullname")
    @pytest.mark.parametrize("fullname", [Category.TEXT_2_CHARACTERS, pytest.param(Category.TEXT_100_ELEMENTS,
                                                                                   marks=pytest.mark.xfail(
                                                                                       reason="Known bug: The documentation states max 100 characters")),
                                          Category.TEXT_50_ELEMENTS])
    def test_update_user_fullname(self, fullname, current_user, user_client: UsersHttpClient):
        user_client.update_user(User(fullname=fullname, id=current_user.id))
        response = user_client.get_current_user()
        assert response.fullname == fullname

    @pytest.mark.xfail(reason="surname doesn't change")
    @allure.feature("Update user")
    @allure.story("Update surname")
    def test_update_user_surname(self, current_user, user_client: UsersHttpClient):
        user_client.update_user(User(surname="Петрович", id=current_user.id))
        response = user_client.get_current_user()
        assert response.surname == "Петрович"

    @pytest.mark.xfail(reason="firstname doesn't change")
    @allure.feature("Update user")
    @allure.story("Update firstname")
    def test_update_user_firstname(self, current_user, user_client: UsersHttpClient):
        user_client.update_user(User(firstname="Петров", id=current_user.id))
        response = user_client.get_current_user()
        assert response.firstname == "Петров"

    @allure.feature("Update user")
    @allure.story("Update photo")
    def test_update_user_photo(self, current_user, user_client: UsersHttpClient, image_to_base64):
        user_client.update_user(User(id=current_user.id, photo=image_to_base64, username="Raz_2_Three"))
        response = user_client.get_current_user()
        assert response.photo == image_to_base64
