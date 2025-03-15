from conftest import Pages, TestData


@Pages.login_page
@TestData.auth_with_not_valid_user
def test_invalid_auth(auth_credential, login_page_object):
    username, password = auth_credential
    login_page_object.login(username, password)
    login_page_object.invalid_auth_credential_text()
    login_page_object.invalid_auth_credential_url()


@Pages.login_page
@TestData.auth_with_valid_user
def test_success_auth(auth_credential, login_page_object):
    username, password = auth_credential
    login_page_object.login(username, password)
    login_page_object.success_auth_url()
