from typing import Any
from pydantic import BaseModel


class SingleResultApiResponse(BaseModel):
    data: Any


class MultipleResultApiResponse(BaseModel):
    data: list[Any]
    size: int

    # @validator('size')
    # def calculate_size(cls, value, values, config, field):
    #     if 'data' in values:
    #         return len(values['data'])
    #     return 0


class PaginatedApiResponse(MultipleResultApiResponse):
    skip: int
    limit: int
