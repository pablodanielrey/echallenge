
import json
import logging
from typing import Optional, Callable

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

from .processors.exceptions import ProcessingException

from .processor import StreamProcessor

def deserializer(data: bytes) -> object:
    """
    la genero como función pero esto se puede modelar
    mejor, tener clases compartidas entre el producer y el indexer, etc.
    por ahora asumo que solo la especificación es que llega un json
    """
    return json.loads(data)


class StreamListener:

    def __init__(self,
                 broker_url: str,
                 detections_topic: str,
                 deserializer: Callable[[bytes], object] = deserializer):

        self.stream_processors: list[StreamProcessor] = []
        self.broker_url = broker_url
        self.detections_topic = detections_topic
        self.deserializer = deserializer
        self.consumer: Optional[KafkaConsumer] = None

    def start(self):
        broker_online = False
        while not broker_online:
            try:
                if not self.consumer:
                    self.consumer = KafkaConsumer(
                        self.detections_topic,
                        group_id="indexer",
                        bootstrap_servers=self.broker_url,
                        enable_auto_commit=False,
                        value_deserializer=self.deserializer
                    )
                broker_online = True
            except NoBrokersAvailable:
                # podría exportar a prometheus
                logging.warn("No se encuentra el broker")

    def add_procesors(self, processors: list[StreamProcessor]):
        self.stream_processors.extend(processors)

    def process_loop(self):
        """
        Procesa los eventos que llegan por el stream. 
        Cada procesador retorna True|False.
        True = continuar con los siguientes procesadores en la cadena.
        False = terminar de procesar el evento y pasar al siguiente.
        ProcessingException = se deja de procesar el evento y continua con los siguientes. (decisión de diseño)

        Notas: 
        se puede hacer tan robusto como se necesite el manejo de errores del procesamiento. ahora solo lo ignora
        y sigue con los siguientes.
        """
        if self.consumer:
            for detection in self.consumer:
                for processor in self.stream_processors:
                    logging.debug(f"Procesando evento con: {processor}")
                    try:
                        if not processor.process_event(detection):
                            break
                    except ProcessingException as e:
                        logging.exception(e)
                        break
                self.consumer.commit()