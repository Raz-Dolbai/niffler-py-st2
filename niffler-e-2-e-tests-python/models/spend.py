from typing import Optional, Literal
from datetime import datetime, timezone

from pydantic import BaseModel, StrictFloat, Field


class CategoryResponse(BaseModel):
    id: str
    name: str
    username: str
    archived: bool


class SpendResponseModel(BaseModel):
    id: str
    spendDate: str
    category: CategoryResponse
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: StrictFloat
    description: str
    username: str


class CategoryRequest(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: bool | None = None


class SpendRequestModel(BaseModel):
    id: str | None = None
    spendDate: str = Field(default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]+"Z")
    category: CategoryRequest
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: float
    description: str
    username: str | None = None
