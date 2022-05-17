import uuid
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    username: str
    password: str

class CredentialsOut(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    lastname: str
    email: Optional[str]

    credentials: list[CredentialsOut]

    class Config:
        orm_mode = True


class UsersListOut(BaseModel):
    skip: int
    limit: int
    size: int
    users: list[UserOut]


class UserIdOut(BaseModel):
    id: uuid.UUID = Field(None, description="user's id")


class AdminOut(UserIdOut):
    username: str
    password: str