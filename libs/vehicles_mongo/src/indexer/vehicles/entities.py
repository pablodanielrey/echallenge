import uuid

from pydantic import BaseModel


class Detection(BaseModel):

    id: uuid.UUID
    timestamp: int
    year: int
    make: str
    model: str
    category: str


class MakeCount(BaseModel):

    make: str
    count: int