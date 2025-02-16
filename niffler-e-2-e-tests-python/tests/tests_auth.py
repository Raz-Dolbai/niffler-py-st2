import pytest
from selene import browser, have, by
from conftest import Pages


@Pages.auth_with_not_valid_user
def test_invalid_auth(auth_with_diff_credential):
    expected_error_message = "Неверные учетные данные пользователя"
    browser.element('.form__error').should(have.text(expected_error_message))


@Pages.auth_with_valid_user
def test_success_auth(auth_with_diff_credential):
    browser.should(have.url_containing("/main"))
