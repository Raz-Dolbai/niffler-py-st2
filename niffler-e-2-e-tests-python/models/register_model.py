from pydantic import BaseModel


class RegisterModel(BaseModel):
    username: str
    password: str
    second_password: str
