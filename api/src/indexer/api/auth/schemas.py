
from pydantic import BaseModel, Field


class Credentials(BaseModel):
    username: str
    password: str

class User(BaseModel):
    name: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


class UserWithCredentials(User):
    credentials: Credentials

    def flatten_dict(self):
        d = self.dict()
        d.update(d['credentials'])
        del d['credentials']
        return d


class UserId(BaseModel):
    id: str = Field(None, description="user's id")