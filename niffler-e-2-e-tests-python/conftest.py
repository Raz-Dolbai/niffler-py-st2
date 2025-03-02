import os
import pytest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient
import time
from databases.spend_db import SpendDb
from models.auth import Auth
from models.config import Envs
from faker import Faker
from models.spend import SpendAdd
from tests.ui.locators import AuthPage


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spending_url=os.getenv("SPENDING_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        spend_db_url=os.getenv("SPENDS_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD"),
        login_url=os.getenv("LOGIN_URL")

    )


@pytest.fixture(scope="function")
def fake_user() -> Auth:
    fake = Faker()
    user = Auth(username=fake.first_name(), password=fake.password())
    return user


@pytest.fixture(scope="session")
def auth(envs):
    username, password = envs.test_username, envs.test_password
    browser.open(envs.frontend_url)
    browser.element(AuthPage.USERNAME).set_value(username)
    browser.element(AuthPage.PASSWORD).set_value(password)
    browser.element(AuthPage.LOGIN).click()
    # получаем токен из Local Storage
    time.sleep(1)
    id_token = browser.driver.execute_script("return window.localStorage.getItem('id_token');")
    assert id_token is not None
    return id_token


@pytest.fixture(params=[])
def auth_credential(envs, fake_user, request) -> tuple:
    get_param = request.param
    if get_param:
        username, password = envs.test_username, envs.test_password
    else:
        username, password = fake_user.username, fake_user.password
    yield username, password


# Создание API и DB клиентов
@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="session")
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client, spend_db) -> str:
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture()
def category_db_clean(spend_db):
    yield
    spend_db.clean_category_db()


@pytest.fixture(params=[])
def spends(request, spends_client) -> SpendAdd:
    spend = spends_client.add_spend(request.param)
    yield spend
    all_spends = spends_client.get_spends()
    if spend.id in [item.id for item in all_spends]:
        spends_client.remove_spends([spend.id])


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    login_page = pytest.mark.usefixtures("login_page")
    spending_page = pytest.mark.usefixtures("spending_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param.description)
    auth_with_not_valid_user = pytest.mark.parametrize("auth_credential", [False], indirect=True)
    auth_with_valid_user = pytest.mark.parametrize("auth_credential", [True], indirect=True)


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.frontend_url)


@pytest.fixture()
def profile_page(auth, envs):
    browser.open(envs.profile_url)


@pytest.fixture()
def login_page(envs):
    browser.open(envs.login_url)


@pytest.fixture()
def spending_page(auth, envs):
    browser.open(envs.spending_url)
