import pytest

from clients.spends_client import SpendsHttpClient
from clients.user_client import UsersHttpClient
from clients.kafka_client import KafkaClient
from clients.oauth_client import OAuthClient
from databases.auth_db import AuthDb
from databases.spend_db import SpendDb
from databases.userdata_db import UserdataDb
from models.config import Envs


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def auth_db(envs: Envs) -> AuthDb:
    return AuthDb(envs)


@pytest.fixture(scope="session")
def userdata_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_api_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_api_token)


@pytest.fixture(scope="session")
def user_client(envs: Envs, auth_api_token) -> UsersHttpClient:
    return UsersHttpClient(envs, auth_api_token)


@pytest.fixture(scope="session")
def kafka_client(envs: Envs) -> KafkaClient:
    with KafkaClient(envs) as k:
        yield k


@pytest.fixture(scope="session")
def auth_client(envs: Envs) -> OAuthClient:
    return OAuthClient(envs)
