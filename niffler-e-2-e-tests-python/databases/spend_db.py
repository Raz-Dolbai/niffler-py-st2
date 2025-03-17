import time
from typing import Sequence
from sqlalchemy import create_engine, Engine, text
from sqlmodel import Session, select

from models.spend import Category
import allure


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    @allure.step("DB: get user categories")
    def get_users_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statements = select(Category).where(Category.username == username)
            return session.exec(statements).all()

    @allure.step("DB: delete category by id")
    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    @allure.step("DB: clear category table")
    def clean_category_db(self):
        with Session(self.engine) as session:
            session.execute(text('DELETE FROM CATEGORY;'))
            session.commit()

    @allure.step("DB: clear spend/category tables")
    def clean_spend_db(self):
        with Session(self.engine) as session:
            session.execute(text('DELETE FROM SPEND;'))
            session.execute(text('DELETE FROM CATEGORY;'))
            session.commit()
