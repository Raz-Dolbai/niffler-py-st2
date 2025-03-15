import time
from typing import Sequence
from sqlalchemy import create_engine, Engine, text
from sqlmodel import Session, select

from models.spend import Category


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_users_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statements = select(Category).where(Category.username == username)
            return session.exec(statements).all()

    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    def clean_category_db(self):
        with Session(self.engine) as session:
            session.execute(text('DELETE FROM CATEGORY;'))
            session.commit()

    def clean_spend_db(self):
        with Session(self.engine) as session:
            session.execute(text('DELETE FROM SPEND;'))
            session.execute(text('DELETE FROM CATEGORY;'))
            session.commit()
