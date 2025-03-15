import pytest
from conftest import Pages

from tests.ui.pages.register_page import RegisterPage


@Pages.register_page
def test_register_with_valid_data(register_credential, register_page_object: RegisterPage):
    register_page_object.register_user(register_credential.username,
                                       register_credential.password,
                                       register_credential.password)
    register_page_object.success_text_after_register()


@Pages.register_page
def test_register_with_passwords_not_equal(register_credential, register_page_object: RegisterPage):
    register_page_object.register_user(register_credential.username,
                                       register_credential.password,
                                       register_credential.second_password)
    register_page_object.password_not_equal()


@Pages.register_page
@pytest.mark.parametrize("username", ["12", "fZwuvGnyKQjRpXAiLmYOCsHtbDeTPqleUodkNBnVIcJSMFaWqEz"])
def test_register_with_not_valid_username(username, register_credential, register_page_object: RegisterPage):
    register_page_object.register_user(username,
                                       register_credential.password,
                                       register_credential.password)
    register_page_object.username_not_valid()


@Pages.register_page
@pytest.mark.parametrize("password", ["12", "fZwuvGnyKQjRp"])
def test_register_with_not_valid_password(password, register_credential, register_page_object: RegisterPage):
    register_page_object.register_user(register_credential.username,
                                       password,
                                       password)
    register_page_object.password_not_valid()
