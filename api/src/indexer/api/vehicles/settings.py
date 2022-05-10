from pydantic import BaseSettings


class Settings(BaseSettings):
    vehicles_db_connection: str
    alerts_topic: str
    kafka_broker_url: str
