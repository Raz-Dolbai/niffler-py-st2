import time
import allure
import pytest
from allure_commons.types import AttachmentType
from faker import Faker
from selene import browser
from clients.oauth_client import OAuthClient
from models.auth import Auth
from models.config import Envs
from models.register_model import RegisterModel
from tests.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def auth_api_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password)


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


@pytest.fixture(scope="function")
def fake_user() -> Auth:
    fake = Faker()
    user = Auth(username=fake.first_name(), password=fake.password(special_chars=False))
    return user
