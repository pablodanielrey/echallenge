import logging
import json
from typing import Callable, Optional

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from ..processor import StreamProcessor, Record


def serializer(data: object) -> bytes:
    """
    la genero como función pero esto se puede modelar
    mejor, tener clases compartidas entre el producer y el indexer, etc.
    por ahora asumo que el requerimiento es solo json
    """
    return json.dumps(data, ensure_ascii=False).encode()


class PublishAlert(StreamProcessor):
    """
        Publica el evento en un topic del broker
    """
    def __init__(self,
                 broker_url: str,
                 alerts_topic: str,
                 serializer: Callable[[object], bytes] = serializer):
 
        super().__init__()
        self.broker_url = broker_url
        self.alerts_topic = alerts_topic
        self.serializer = serializer
        self.producer: Optional[KafkaProducer] = None

    def start(self):
        broker_online = False
        while not broker_online:
            try:
                if not self.producer:
                    self.producer = KafkaProducer(
                        bootstrap_servers=self.broker_url,
                        value_serializer=self.serializer,
                    )
                broker_online = True
            except NoBrokersAvailable:
                # podría exportar a prometheus
                logging.warn("No se encuentra el broker")

    def process_event(self, detection: Record):
        logging.warn(f"Publicando una alerta timestamp: {detection.timestamp} vehiculo: {detection.value}")
        self.producer.send(self.alerts_topic, detection.value)
        return True
