from typing import Any
from pydantic import BaseModel, Field, EmailStr



class CredentialsOut(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    name: str
    lastname: str
    email: str
    credentials: list[CredentialsOut]

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    skip: int
    limit: int
    size: int
    users: list[UserOut]


class UserIn(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    username: str
    password: str

class UserId(BaseModel):
    id: str = Field(None, description="user's id")
