from typing import Optional
from sqlalchemy import select, func

from . import db, entities


class VehiclesManager:

    def __init__(self, db: db.DB):
        self.db = db
        self.db.generate_db()

    def detections(self, skip: Optional[int] = None, limit: Optional[int] = None):
        stmt = select(entities.Detection)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        with self.db.session() as session:
            rs = [d for d in session.execute(stmt).all()]
        return rs

    # def add_detection(self, detection: dict[str, Any]):
    def add_detection(self, **kw):
        detection = db.DB.from_dict(entities.Detection, kw)
        with self.db.session() as session:
            session.add(detection)
            session.commit()

    def vehicles_by_make(self):
        stmt = select(entities.Detection.make, func.count(entities.Detection.id).label("count")).group_by(entities.Detection.make).order_by(entities.Detection.make)
        with self.db.session() as session:
            rs = [v for v in session.execute(stmt)]
        return rs
