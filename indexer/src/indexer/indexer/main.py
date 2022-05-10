import logging
import os

from indexer.vehicles import db as v_db, models

from .settings import Settings

from .models import Indexer
from .stream.processors import DetectAlert, PersistToDB, PublishAlert
from .stream.listener import StreamListener


def start():
    logging.getLogger().setLevel(logging.WARNING)
    logging.info("iniciando el indexer y los processors")

    settings = Settings()

    listener = StreamListener(settings.kafka_broker_url, settings.detections_topic)
    detect_alert = DetectAlert(settings.suspicious_vehicle)

    db = v_db.DB(settings.vehicles_db_connection)
    vm = models.VehiclesManager(db)
    persist_to_db = PersistToDB(vm)

    publish_to_api = PublishAlert(settings.kafka_broker_url, settings.alerts_topic)

    indexer = Indexer(listener, [detect_alert, persist_to_db, publish_to_api])
    indexer.start()


if __name__ == '__main__':
    start()
