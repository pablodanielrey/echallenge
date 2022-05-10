import uuid
from typing import Any
from pydantic import BaseModel


class Detection(BaseModel):

    id: uuid.UUID
    timestamp: int
    year: int
    make: str
    model: str
    category: str


class CountByMake(BaseModel):

    make: str
    count: int


def from_dict(cls: type[BaseModel], data: dict[str, Any]) -> BaseModel:
    """
        Método utilitario para parsear dics a estas entidades
        uso este método debido a que los dicts vienen con distinto case las keys.
        y tambien no quiero tirar un error en caso de que el dict traiga mas keys que las que necesito.
        El case de las claves no es importante ya que se lleva todo a lower. (year == Year)
    """
    filtered_dict = {k.lower(): v for (k, v) in data.items() if k.lower() in cls.__fields__.keys()}
    if "id" not in filtered_dict:
        filtered_dict["id"] = uuid.uuid4()
    return cls(**filtered_dict)
