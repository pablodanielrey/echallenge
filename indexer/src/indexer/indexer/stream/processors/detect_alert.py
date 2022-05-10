
from kafka.consumer.fetcher import ConsumerRecord

from ..processor import StreamProcessor, Record

class DetectAlert(StreamProcessor):
    """
        Detecta si el stream contiene un evento para el cual se debe generar una alerta
    """
    def __init__(self, category: str):
        self.category = category

    def process_event(self, detection: Record) -> bool:
        alert: bool = self.category == detection.value["Category"]
        # if alert:
        #     logging.warn(f"Se detecto una alerta {detection.timestamp} - {detection.value}")
        return alert