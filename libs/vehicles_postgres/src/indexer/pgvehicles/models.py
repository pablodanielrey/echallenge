from typing import Optional
from sqlalchemy import select, func, exc

from indexer.vehicles.exceptions import IntegrityError
from indexer.vehicles.entities import Detection, CountByMake, from_dict

from . import db, entities


class VehiclesManager:

    def __init__(self, db: db.DB):
        self.db = db
        self.db.generate_db()

    def detections(self, skip: Optional[int] = None, limit: Optional[int] = None) -> list[Detection]:
        stmt = select(entities.Detection).order_by(entities.Detection.id)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        with self.db.session() as session:
            rs = [from_dict(Detection, d.__dict__) for d, in session.execute(stmt)]
        return rs

    # def add_detection(self, detection: dict[str, Any]):
    def add_detection(self, **kw) -> str:
        try:
            detection = db.DB.from_dict_to_entity(entities.Detection, kw)
            with self.db.session() as session:
                session.add(detection)
                session.commit()
                return str(detection.id)
        except exc.IntegrityError as e:
            raise IntegrityError() from e

    def vehicles_by_make(self) -> list[CountByMake]:
        stmt = select(entities.Detection.make, func.count(entities.Detection.id).label("count")).group_by(entities.Detection.make).order_by(entities.Detection.make)
        with self.db.session() as session:
            rs = [CountByMake(make=make, count=count) for (make, count) in session.execute(stmt)]
        return rs
