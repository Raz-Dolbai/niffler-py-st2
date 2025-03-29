import time
from typing import Sequence
from sqlalchemy import create_engine, Engine, text, event
from sqlmodel import Session, select
from allure_commons.types import AttachmentType
from models.spend import Category, Spend
import allure


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

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

    @allure.step("DB: select spend by id")
    def select_spend_by_id(self, spend_id: str):
        with Session(self.engine) as session:
            statements = select(Spend).where(Spend.id == spend_id)
            return session.exec(statements).first()

    @allure.step("DB: select category by name")
    def select_category_by_name(self, name: str):
        with Session(self.engine) as session:
            statements = select(Category).where(Category.name == name)
            return session.exec(statements).first()

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
