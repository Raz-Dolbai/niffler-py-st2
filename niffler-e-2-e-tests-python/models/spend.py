from typing import Literal
from datetime import datetime
from pydantic import BaseModel

from sqlmodel import Field, SQLModel

from models.category import CategoryAdd


class Spend(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str


class SpendAdd(BaseModel):
    id: str | None = None
    spendDate: str
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: float
    description: str
    category: CategoryAdd
