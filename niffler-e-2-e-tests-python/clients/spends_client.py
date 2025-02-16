from urllib.parse import urljoin

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

    def add_category(self, name: str):
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={"name": name})
        response.raise_for_status()
        return response.json()

    def get_category(self):
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def add_spend(self, body):
        response = self.session.post(urljoin(self.base_url, "/api/spends/add"), json=body)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[int]):
        response = self.session.delete(urljoin(self.base_url, "/api/spends/remove"), params={"ids": ids})
        response.raise_for_status()

    def update_spends(self, body: dict):
        response = self.session.patch(urljoin(self.base_url, "/api/spends/edit"), json=body)
        response.raise_for_status()
        return response

    def get_spend(self, spend_id: str):
        pass

    def update_categories(self, body: dict):
        response = self.session.patch(urljoin(self.base_url, "/api/categories/update"), json=body)
        print(body)
        response.raise_for_status()
        return response.json()

