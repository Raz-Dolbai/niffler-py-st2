import base64
import os
import allure
import pytest
from pytest import Item, FixtureDef, FixtureRequest
from dotenv import load_dotenv

from clients.user_client import UsersHttpClient
from models.category import CategoryAdd
from models.config import Envs
from models.spend import SpendAdd
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener

from models.user import User

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


@pytest.fixture(scope="session")
def envs() -> Envs:
    # todo разбить на 2 dotenv серверные и клиентские и сделать 2 фикстуры
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
        register_url=os.getenv("REGISTER_URL"),
        auth_url=os.getenv("AUTH_URL"),
        kafka_address=os.getenv("KAFKA_ADDRESS")

    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


# @pytest.fixture(scope="session")
# def spends_client(envs, auth) -> SpendsHttpClient:
#     return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client, spend_db) -> CategoryAdd:
    category_name = request.param
    category = spends_client.add_category(CategoryAdd(name=category_name))
    yield category
    spend_db.delete_category(category.id)


@pytest.fixture()
def category_db_clean(spend_db):
    yield
    spend_db.clean_category_db()


@pytest.fixture()
def current_user(user_client: UsersHttpClient) -> User:
    current_user = user_client.get_current_user()
    return User.model_validate(current_user)


@pytest.fixture()
def image_to_base64():
    """Конвертирует изображение в строку base64.
    Returns:
        Строку base64, представляющую изображение, или None, если файл не найден.
    """
    try:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_file_dir, "static", "astronaut.png")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return "data:image/png;base64,{}".format(encoded_string)
    except FileNotFoundError:
        return ""


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
    main_page_oauth = pytest.mark.usefixtures("main_page_oauth")
    profile_page_oauth = pytest.mark.usefixtures("profile_page_oauth")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param.description)
    auth_with_not_valid_user = pytest.mark.parametrize("auth_credential", [False], indirect=True)
    auth_with_valid_user = pytest.mark.parametrize("auth_credential", [True], indirect=True)


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
