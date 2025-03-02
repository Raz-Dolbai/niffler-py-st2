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
    id: Optional[str] = Field(default=None, primary_key=True)
    spendDate: datetime
    currency: str
    amount: float
    description: str
    # category: Category = Relationship()


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






