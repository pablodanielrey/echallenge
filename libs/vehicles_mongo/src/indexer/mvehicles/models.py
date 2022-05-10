from typing import Optional
from bson.son import SON

from pymongo.errors import DuplicateKeyError

from indexer.vehicles.entities import Detection, CountByMake, from_dict
from indexer.vehicles.exceptions import IntegrityError

from . import db


class VehiclesManager:
    """
    Implementa el procolo indexer.vehicles.models.VehiclesManager
    usando mongodb para almacenar los datos.
    """

    def __init__(self, database: db.DB):
        self.db = database

    def detections(self, skip: Optional[int] = None, limit: Optional[int] = None)  -> list[Detection]:
        f = self.db.detections.find().sort("id")
        if skip:
            f = f.skip(skip)
        if limit:
            f = f.limit(limit)
        return [from_dict(Detection, v) for v in f]

    def add_detection(self, **kw) -> str:
        try:
            detection = from_dict(Detection, kw)
            iid = self.db.detections.insert_one(detection.dict()).inserted_id
            return iid
        except DuplicateKeyError as e:
            raise IntegrityError() from e

    def vehicles_by_make(self) -> list[CountByMake]:
        pipeline = [
            {"$group": {"_id": "$make", "count": {"$sum": 1}}},
            {"$sort": SON([("_id", -1)])},
            {"$project": {"_id": 0, "make": "$_id", "count": "$count"}}
        ]
        data = [from_dict(CountByMake, m) for m in self.db.detections.aggregate(pipeline)]
        return data

