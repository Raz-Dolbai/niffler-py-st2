from selene import browser, have, by
from conftest import Pages, TestData
from tests.ui.locators import AuthPage


@Pages.login_page
@TestData.auth_with_not_valid_user
def test_invalid_auth(auth_credential):
    expected_error_message = "Неверные учетные данные пользователя"
    username, password = auth_credential
    browser.element(AuthPage.USERNAME).set_value(username)
    browser.element(AuthPage.PASSWORD).set_value(password)
    browser.element(AuthPage.LOGIN).click()
    browser.element(AuthPage.ERROR_MESSAGE).should(have.text(expected_error_message))


@Pages.login_page
@TestData.auth_with_valid_user
def test_success_auth(auth_credential):
    username, password = auth_credential
    browser.element(AuthPage.USERNAME).set_value(username)
    browser.element(AuthPage.PASSWORD).set_value(password)
    browser.element(AuthPage.LOGIN).click()
    browser.should(have.url_containing("/main"))
