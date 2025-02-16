from pydantic import BaseModel, StrictFloat, Field


class CategoriesModel(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: str | None = None
