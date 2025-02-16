import os
import pytest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient
import time
from models.auth import Auth
from faker import Faker
from http import HTTPStatus

from models.spend import SpendRequestModel, CategoryRequest, SpendResponseModel
from models.categories import CategoriesModel


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs):
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def spending_url(envs):
    return os.getenv("SPENDING_URL")


@pytest.fixture(scope="function")
def profile_url(envs):
    return os.getenv("PROFILE_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="session")
def fake_user() -> Auth:
    fake = Faker()
    user = Auth(username=fake.first_name(), password=fake.password())
    return user


@pytest.fixture(scope="session")
def auth(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    # получаем токен из Session Storage
    time.sleep(3)
    id_token = browser.driver.execute_script("return window.localStorage.getItem('id_token');")
    assert id_token is not None
    return id_token


@pytest.fixture(scope="session")
def auth_with_diff_credential(frontend_url, fake_user, request, app_user):
    browser.open(frontend_url)
    get_param = request.param
    if get_param:
        username, password = app_user
    else:
        username, password = fake_user.username, fake_user.password
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_category()
    if category_name not in [category["name"] for category in current_categories]:
        spends_client = spends_client.add_category(category_name)
    return spends_client  # category_name


@pytest.fixture(scope="session")
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spend(request.param)
    yield spend
    try:
        spends_client.remove_spends(spend["id"])
    except Exception:
        pass


@pytest.fixture()
def spends_update(spends, spends_client):
    response = spends_client.update_spends(SpendRequestModel(id=spends["id"],
                                                             amount=200.51,
                                                             description='QA-GURU Python ADVANCED 3',
                                                             category=CategoryRequest(
                                                                 **{'name': 'school'}).model_dump(),
                                                             currency="RUB"
                                                             ).model_dump())
    return response


@pytest.fixture()
def spends_remove(spends, spends_client):
    response = spends_client.remove_spends([spends["id"]])
    return response


@pytest.fixture()
def categories_update(category, spends_client):
    faker = Faker()
    response = spends_client.update_categories({"name": faker.text(10),
                                                "id": category["id"]})
    yield response
    try:
        spends_client.update_categories({"id": category["id"], "archived": True, "name": response["name"]})
    except Exception:
        pass


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    auth_with_not_valid_user = pytest.mark.parametrize("auth_with_diff_credential", [False], indirect=True)
    auth_with_valid_user = pytest.mark.parametrize("auth_with_diff_credential", [True], indirect=True)


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.open(frontend_url)


@pytest.fixture()
def profile_page(auth, profile_url):
    browser.open(profile_url)
