from typing import Optional

from pydantic import BaseModel, ConfigDict, StrictInt
from sqlmodel import SQLModel, Field


class CategoryAdd(BaseModel):
    id: Optional[str] = None
    name: str | None = None
    username: Optional[str] = None
    archived: Optional[bool] = False


class Category(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool = Field(default=False)


class CategoryError(BaseModel):
    type: str
    title: str
    status: StrictInt
    detail: str
    instance: str

    model_config = ConfigDict(extra="forbid")
