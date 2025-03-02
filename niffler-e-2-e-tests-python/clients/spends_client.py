from urllib.parse import urljoin
from models.spend import SpendAdd, CategoryAdd

import requests


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def add_category(self, name: str) -> CategoryAdd:
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={"name": name})
        response.raise_for_status()
        return CategoryAdd.model_validate(response.json())

    def get_category(self) -> list[CategoryAdd]:
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return [CategoryAdd.model_validate(item) for item in response.json()]

    def add_spend(self, spend: SpendAdd) -> SpendAdd:
        response = self.session.post(urljoin(self.base_url, "/api/spends/add"), json=spend.model_dump())
        response.raise_for_status()
        return SpendAdd.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        response = self.session.delete(urljoin(self.base_url, "/api/spends/remove"), params={"ids": ids})
        response.raise_for_status()

    def update_spends(self, body: dict):
        response = self.session.patch(urljoin(self.base_url, "/api/spends/edit"), json=body)
        response.raise_for_status()
        return response

    def get_spends(self) -> list[SpendAdd]:
        url = urljoin(self.base_url, "api/spends/all")
        response = self.session.get(url)
        response.raise_for_status()
        return [SpendAdd.model_validate(item) for item in response.json()]

    def update_categories(self, body: dict):
        response = self.session.patch(urljoin(self.base_url, "/api/categories/update"), json=body)
        print(body)
        response.raise_for_status()
        return response.json()
