
import json
import logging
from typing import Callable

from kafka import KafkaConsumer, KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import NoBrokersAvailable
from db.src.indexer.db.detections import VehiclesManager

from indexer.db import DB, detections

from .exceptions import ProcessingException


def deserializer(data: bytes) -> object:
    """
    la genero como función pero esto se puede modelar
    mejor, tener clases compartidas entre el producer y el indexer, etc.
    por ahora asumo que solo la especificación es que llega un json
    """
    return json.loads(data)


def serializer(data: object) -> bytes:
    """
    la genero como función pero esto se puede modelar
    mejor, tener clases compartidas entre el producer y el indexer, etc.
    por ahora asumo que el requerimiento es solo json
    """
    return json.dumps(data, ensure_ascii=False).encode()


class StreamProcessor:

    def start(self):
        pass

    def process_event(self, detection: ConsumerRecord) -> bool:
        return True


class DetectAlert(StreamProcessor):
    """
        Detecta si el stream contiene un evento para el cual se debe generar una alerta
    """
    def __init__(self, category: str):
        self.category = category

    def process_event(self, detection: ConsumerRecord) -> bool:
        alert: bool = self.category == detection.value["Category"]
        # if alert:
        #     logging.warn(f"Se detecto una alerta {detection.timestamp} - {detection.value}")
        return alert


class PersistToDB(StreamProcessor):

    def __init__(self, vm: detections.VehiclesManager):
        self.vm = vm

    def process_event(self, detection_event: ConsumerRecord) -> bool:
        # logging.warn(f"agregando la detección {detection.value} a la base")
        # detection = {"timestamp": detection_event.timestamp, **detection_event.value}
        self.vm.add_detection(timestamp=detection_event.timestamp, **detection_event.value)
        return True


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
        self.producer: KafkaProducer = None

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

    def process_event(self, detection: ConsumerRecord):
        logging.warn(f"Publicando una alerta timestamp: {detection.timestamp} vehiculo: {detection.value}")
        self.producer.send(self.alerts_topic, detection.value)
        return True


class StreamListener:

    def __init__(self,
                 broker_url: str,
                 detections_topic: str,
                 deserializer: Callable[[bytes], object] = deserializer):

        self.stream_processors: list[StreamProcessor] = []
        self.broker_url = broker_url
        self.detections_topic = detections_topic
        self.deserializer = deserializer
        self.consumer: KafkaConsumer = None

    def start(self):
        broker_online = False
        while not broker_online:
            try:
                if not self.consumer:
                    self.consumer = KafkaConsumer(
                        self.detections_topic,
                        group_id="indexer",
                        bootstrap_servers=self.broker_url,
                        value_deserializer=self.deserializer
                    )
                broker_online = True
            except NoBrokersAvailable:
                # podría exportar a prometheus
                logging.warn("No se encuentra el broker")

    def add_procesors(self, processors: list[StreamProcessor]):
        self.stream_processors.extend(processors)

    def process_loop(self):
        for detection in self.consumer:
            # logging.info(f"detección: {detection}")
            # save the detections to db
            for processor in self.stream_processors:
                try:
                    if not processor.process_event(detection):
                        """ si el procesador retorna False entonces no se continua con los demas """
                        break
                except ProcessingException as e:
                    """ 
                        loggeo la exception y dejo de procesar este evento
                        si existe un error en un procesamiento del stream no se continua con los siguientes
                    """
                    logging.exception(e)
                    break


class Indexer:

    def __init__(self,
                 stream_listener: StreamListener,
                 stream_processors: list[StreamProcessor]):

        self.stream_processors = stream_processors
        self.stream_listener = stream_listener
        self.stream_listener.add_procesors(stream_processors)

    def start(self):
        for sp in self.stream_processors:
            sp.start()
        self.stream_listener.start()
        self.stream_listener.process_loop()

