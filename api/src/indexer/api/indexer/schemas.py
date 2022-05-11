from typing import Any
from pydantic import BaseModel


class SingleResultApiResponse(BaseModel):
    data: Any


class MultipleResultApiResponse(BaseModel):
    data: list[Any]
    size: int


class PaginatedApiResponse(MultipleResultApiResponse):
    skip: int
    limit: int
