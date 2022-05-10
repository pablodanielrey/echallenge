from pydantic import BaseSettings


class Settings(BaseSettings):
    vehicles_db_connection: str
    kafka_broker_url: str
    alerts_topic: str
    detections_topic: str
    suspicious_vehicle: str