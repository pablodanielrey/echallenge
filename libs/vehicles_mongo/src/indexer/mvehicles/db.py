
import pymongo


class DB:

    def __init__(self, db_conn: str):
        self.client = pymongo.MongoClient(db_conn, uuidRepresentation='standard')
        self.generate_db()

    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass

    def generate_db(self):
        self.db = self.client.vehicles
        self.detections = self.db.detections
        self.detections.create_index([("id", pymongo.ASCENDING)], unique=True)
        self.detections.create_index([("make", pymongo.ASCENDING)], unique=False)

    def drop_db(self):
        self.client.drop_database("vehicles")

