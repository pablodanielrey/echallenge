from typing import Optional
import uuid

from bson.son import SON
from . import db, entities


class VehiclesManager:

    def __init__(self, db: db.DB):
        self.db = db

    def detections(self, skip: Optional[int] = None, limit: Optional[int] = None):
        f = self.db.detections.find().sort("id")
        if skip:
            f = f.skip(skip)
        if limit:
            f = f.limit(limit)
        
        return [self.db.from_dict(entities.Detection, v) for v in f]

    def add_detection(self, **kw):
        detection = db.DB.from_dict(entities.Detection, kw)
        iid = self.db.detections.insert_one(detection.dict()).inserted_id
        return iid

    def vehicles_by_make(self):
        pipeline = [
            {"$group": {"_id": "$make", "count": {"$sum": 1}}},
            {"$sort": SON([("_id", -1)])},
            {"$project": {"_id": 0, "make": "$_id", "count": "$count"}}
        ]
        data = [self.db.from_dict(entities.CountByMake, m) for m in self.db.detections.aggregate(pipeline)]
        return data
