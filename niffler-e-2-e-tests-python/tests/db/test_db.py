from conftest import TestData, Pages
from databases.spend_db import SpendDb
from models.config import Envs
from models.spend import SpendAdd
from models.category import CategoryAdd

TEST_CATEGORY = "TestCategory"


class TestDB:

    @Pages.main_page
    @TestData.category(TEST_CATEGORY)
    def test_category_in_db_after_add(self, category, spend_db: SpendDb, envs: Envs):
        category_db = spend_db.select_category_by_name(category)
        assert category_db is not None, "Category with name TestCategory not found in db"
        assert category_db.name == category, f"Expected TestCategory, got {category_db.name}"
        assert not category_db.archived, f"Expected False, got {category_db.archived}"
        assert category_db.username == envs.test_username, f"Expected {Envs.test_username}, got {category_db.username}"

    @Pages.main_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(
        amount=108.51,
        description="QA-GURU Python ADVANCED 2",
        currency="RUB",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2025-03-10T18:39:27.955Z"))
    def test_spend_in_db_after_add(self, category, spends: SpendAdd, spend_db: SpendDb, envs: Envs):
        spend_db = spend_db.select_spend_by_id(spends.id)
        assert spend_db is not None, f"Spend with id {spends.id} not found in db"
        assert spend_db.description == spends.description, f"Expected description {spends.id}, got {spend_db.id}"
        assert spend_db.currency == spends.currency, f"Expected currency {spends.currency}, got {spend_db.currency}"
        assert spend_db.username == envs.test_username, f"Expected {Envs.test_username}, got {spend_db.username}"
