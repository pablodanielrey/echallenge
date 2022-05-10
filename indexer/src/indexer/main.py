import logging
import os

from .settings import Settings

from .models import DetectAlert, Indexer, PersistToDB, PublishAlert, StreamListener


def start():
    logging.getLogger().setLevel(logging.WARNING)
    logging.info("iniciando el indexer y los processors")

    settings = Settings()

    listener = StreamListener(settings.kafka_broker_url, settings.detections_topic)
    detect_alert = DetectAlert(settings.suspicious_vehicle)

    db = DB(settings.vehicles_db_connection)
    vm = detections.VehiclesManager(db)
    persist_to_db = PersistToDB(vm)

    publish_to_api = PublishAlert(settings.kafka_broker_url, settings.alerts_topic)

    indexer = Indexer(listener, [detect_alert, persist_to_db, publish_to_api])
    indexer.start()


if __name__ == '__main__':
    start()
