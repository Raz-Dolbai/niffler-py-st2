import pytest
from selene import browser


@pytest.fixture()
def register_page(envs):
    browser.open(envs.register_url)


@pytest.fixture()
def login_page(envs):
    browser.open(envs.login_url)


@pytest.fixture()
def spending_page(auth, envs):
    browser.open(envs.spending_url)


@pytest.fixture()
def main_page_oauth(auth_api_token, envs):
    # retrieved_token = browser.execute_script("return localStorage.getItem('id_token');")
    # assert retrieved_token == auth_api_token, f"Expected {auth_api_token}, but got {retrieved_token}"
    browser.open(envs.frontend_url)
    browser.execute_script(f"localStorage.setItem('id_token', '{auth_api_token}')")
    browser.open(envs.frontend_url)


@pytest.fixture()
def profile_page_oauth(auth_api_token, envs):
    browser.open(envs.profile_url)
    browser.execute_script(f"localStorage.setItem('id_token', '{auth_api_token}')")
    # browser.driver.execute_script(f"localStorage.setItem('id_token', '{auth_api_token}')")
    browser.open(envs.profile_url)


@pytest.fixture()
def profile_page(auth, envs):
    browser.open(envs.profile_url)


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.frontend_url)
