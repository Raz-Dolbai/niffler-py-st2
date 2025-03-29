import pytest
from tests.ui.pages.spending_page import SpendingPage
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.register_page import RegisterPage
from tests.ui.pages.profile_page import ProfilePage


@pytest.fixture()
def spending_page_object() -> SpendingPage:
    return SpendingPage()


@pytest.fixture()
def login_page_object() -> LoginPage:
    return LoginPage()


@pytest.fixture()
def register_page_object() -> RegisterPage:
    return RegisterPage()


@pytest.fixture()
def profile_page_object() -> ProfilePage:
    return ProfilePage()
