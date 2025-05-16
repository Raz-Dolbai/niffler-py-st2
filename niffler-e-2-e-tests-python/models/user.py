from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Field


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    surname: Optional[str] = None
    fullname: Optional[str] = None
    currency: Optional[str] = "RUB"
    photo: Optional[str] = None
    photoSmall: Optional[str] = None
    friendshipStatus: Optional[str] = "INVITE_SENT"


class UserName(BaseModel):
    username: str


class UserDB(SQLModel, table=True):
    metadata = MetaData()
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str = "RUB"
    firstname: str
    surname: str
    currency: str
    photo: str | None = None
    photo_small: str | None = None
    full_name: str
    __table_args__ = {"extend_existing": True}
