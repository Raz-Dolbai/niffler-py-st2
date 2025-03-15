from typing import Sequence
from sqlalchemy import create_engine, Engine, text
from sqlmodel import Session


class AuthDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine_auth_db = create_engine(db_url)

    def clean_users_db(self):
        with Session(self.engine_auth_db) as session:
            session.execute(text('DELETE FROM public."authority";'))
            session.execute(text('DELETE FROM public."user";'))
            session.commit()
