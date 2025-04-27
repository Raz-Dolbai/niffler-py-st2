from clients.spends_client import SpendsHttpClient
from models.enums import Category
import allure


def test_add_category(spends_client: SpendsHttpClient, category_db_clean):
    spends_client.add_category(name=Category.SCHOOL)
    category = spends_client.get_categories()
    with allure.step(f"Категория {Category.SCHOOL} добавлена"):
        assert Category.SCHOOL == category[0].name
