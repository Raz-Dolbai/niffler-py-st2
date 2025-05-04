from typing import List

import requests
import allure
from models.config import Envs
from models.user import User
from http import HTTPStatus

from utils.sessions import BaseSession


class UsersHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @allure.step("HTTP: update user")
    def update_user(self, user_model: User) -> User:
        response = self.session.post("/api/users/update", json=user_model.model_dump())
        return User.model_validate(response.json())

    @allure.step("HTTP: get current user")
    def get_current_user(self) -> User:
        response = self.session.get("/api/users/current")
        return User.model_validate(response.json())

    @allure.step("HTTP: get users")
    def get_users(self, params: dict = None) -> List[User]:
        response = self.session.get("/api/spends/add", params=params)
        return [User.model_validate(item) for item in response.json()]
