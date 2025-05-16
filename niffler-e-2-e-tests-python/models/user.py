from typing import Optional
from datetime import datetime
from pydantic import BaseModel


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
