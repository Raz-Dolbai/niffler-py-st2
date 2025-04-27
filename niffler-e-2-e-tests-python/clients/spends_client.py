import requests
import allure
from models.config import Envs
from models.spend import SpendAdd
from models.category import CategoryAdd
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response

from utils.sessions import BaseSession


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        # Первый вариант крепить аттачи ко всем запросам SpendsClient
        # self.session.hooks["response"].append(self.attach_response)

    # Первый вариант крепить аттачи ко всем запросам SpendsClient
    # @staticmethod
    # def attach_response(response: Response, *args, **kwargs):
    #     attachment_name = response.request.method + " " + response.request.url
    #     allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    @allure.step("HTTP: add category")
    def add_category(self, name: str) -> CategoryAdd:
        response = self.session.post("/api/categories/add", json={"name": name})
        return CategoryAdd.model_validate(response.json())

    @allure.step("HTTP: get category")
    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get("/api/categories/all")
        return [CategoryAdd.model_validate(item) for item in response.json()]

    @allure.step("HTTP: add spend")
    def add_spend(self, spend: SpendAdd) -> SpendAdd:
        response = self.session.post("/api/spends/add", json=spend.model_dump())
        return SpendAdd.model_validate(response.json())

    @allure.step("HTTP: delete spend")
    def remove_spends(self, ids: list[str]):
        """Удаление трат без возврата ответа, но если нужно проверить
        саму ручку удаления - то надо добавить возврат response"""
        self.session.delete("/api/spends/remove", params={"ids": ids})

    @allure.step("HTTP: update spend")
    def update_spends(self, body: dict):
        response = self.session.patch("/api/spends/edit", json=body)
        return response

    @allure.step("HTTP: get spends")
    def get_spends(self) -> list[SpendAdd]:
        response = self.session.get("/api/spends/all")
        return [SpendAdd.model_validate(item) for item in response.json()]

    @allure.step("HTTP: update category")
    def update_categories(self, body: dict):
        response = self.session.patch("/api/categories/update", json=body)
        return response.json()
