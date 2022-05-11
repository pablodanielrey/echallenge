from abc import ABC, abstractmethod

from kafka.consumer.fetcher import ConsumerRecord


Record = ConsumerRecord

class StreamProcessor(ABC):
    """
    Procesa el stream de eventos de kafka.
    Patrón Chain of Reponsibility
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def process_event(self, detection: Record) -> bool:
        return True
