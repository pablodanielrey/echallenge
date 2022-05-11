from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserToken(BaseModel):
    name: str
    lastname: str
    email: str

    class Config:
        orm_mode = True