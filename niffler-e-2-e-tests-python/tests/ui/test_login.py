from conftest import Pages, TestData
import pytest
from tests.ui.pages.login_page import LoginPage

pytestmark = [pytest.mark.allure_label("Login", label_type="epic")]


@Pages.login_page
@TestData.auth_with_not_valid_user
def test_invalid_auth(auth_credential, login_page_object: LoginPage):
    username, password = auth_credential
    login_page_object.login(username, password)
    login_page_object.should_be_expected_text_after_invalid_auth()
    login_page_object.should_be_expected_url_after_invalid_auth()


@Pages.login_page
@TestData.auth_with_valid_user
def test_success_auth(auth_credential, login_page_object: LoginPage):
    username, password = auth_credential
    login_page_object.login(username, password)
    login_page_object.should_be_expected_url_after_success_auth()


@Pages.login_page
def test_go_to_register_page_after_click_create_new_account(login_page_object: LoginPage):
    login_page_object.click_create_new_account()
    login_page_object.should_be_register_page()
