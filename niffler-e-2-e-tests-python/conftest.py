import os
import allure
import pytest
from pytest import Item, FixtureDef, FixtureRequest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient
import time
from databases.spend_db import SpendDb
from databases.auth_db import AuthDb
from models.auth import Auth
from models.config import Envs
from faker import Faker
from models.spend import SpendAdd
from models.register_model import RegisterModel
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from tests.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spending_url=os.getenv("SPENDING_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        spend_db_url=os.getenv("SPENDS_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD"),
        login_url=os.getenv("LOGIN_URL"),
        register_url=os.getenv("REGISTER_URL")

    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


@pytest.fixture(scope="function")
def fake_user() -> Auth:
    fake = Faker()
    user = Auth(username=fake.first_name(), password=fake.password())
    return user


@pytest.fixture(scope="session")
def auth(envs):
    page = LoginPage()
    username, password = envs.test_username, envs.test_password
    browser.open(envs.frontend_url)
    page.login(username, password)
    # получаем токен из Local Storage
    time.sleep(1)
    id_token = browser.driver.execute_script("return window.localStorage.getItem('id_token');")
    assert id_token is not None
    allure.attach(id_token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return id_token


@pytest.fixture(params=[])
def auth_credential(envs, fake_user, request) -> tuple:
    get_param = request.param
    if get_param:
        username, password = envs.test_username, envs.test_password
    else:
        username, password = fake_user.username, fake_user.password
    yield username, password


@pytest.fixture(scope="session")
def register_credential(auth_db) -> RegisterModel:
    fake = Faker()
    model = RegisterModel(username=fake.user_name(),
                          password=fake.password(),
                          second_password=fake.password())
    yield model
    auth_db.clean_users_db()


@pytest.fixture(scope="session")
def register():
    pass


# Создание API и DB клиентов
@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="session")
def auth_db(envs) -> AuthDb:
    return AuthDb(envs.auth_db_url)


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


@pytest.fixture()
def spend_db_clean(spend_db):
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
    register_page = pytest.mark.usefixtures("register_page")


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
def register_page(envs):
    browser.open(envs.register_url)


@pytest.fixture()
def spending_page(auth, envs):
    browser.open(envs.spending_url)


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


def allure_reporter(config) -> AllureReporter:
    listener: AllureListener = next(
        filter(
            lambda plugin: (isinstance(plugin, AllureListener)),
            dict(config.pluginmanager.list_name_plugin()).values(),
        ),
        None,
    )
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    reporter = allure_reporter(item.config)
    test = reporter.get_test(None)
    test.labels = list(filter(lambda x: x.name not in ("tag"), test.labels))
