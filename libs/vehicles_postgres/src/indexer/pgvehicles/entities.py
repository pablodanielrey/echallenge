import uuid

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from .db import Base


class Detection(Base):
    __tablename__ = 'detections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(BigInteger)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    category = Column(String)
