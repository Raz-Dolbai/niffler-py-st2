import pytest

from clients.spends_client import SpendsHttpClient
from databases.auth_db import AuthDb
from databases.spend_db import SpendDb
from models.config import Envs


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def auth_db(envs: Envs) -> AuthDb:
    return AuthDb(envs)


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_api_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_api_token)
