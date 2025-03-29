from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool = Field(default=False)


class Spend(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str


class CategoryAdd(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: bool | None = None


class SpendAdd(BaseModel):
    id: str | None = None
    spendDate: str
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: float
    description: str
    category: CategoryAdd
