from typing import Sequence
from sqlalchemy import create_engine, Engine, text
from sqlmodel import Session
import allure

from models.config import Envs


class AuthDb:
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine_auth_db = create_engine(envs.auth_db_url)

    @allure.step("DB: clear authority/user tables")
    def clean_users_db(self):
        with Session(self.engine_auth_db) as session:
            session.execute(text('DELETE FROM public."authority";'))
            session.execute(text('DELETE FROM public."user";'))
            session.commit()
