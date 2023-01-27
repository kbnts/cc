import json

from django.conf import settings
from kafka import KafkaProducer

from .singleton import Singleton


class KafkaPublisher(metaclass=Singleton):
    _producer: KafkaProducer = None

    def __init__(self, url=settings.KAFKA_URL) -> None:
        self._producer = KafkaProducer(bootstrap_servers=url)

    def publish(self, topic, data) -> None:
        self._producer.send(topic, json.dumps(data).encode("utf-8"))


class ItemPublisher:
    def __init__(self, client) -> None:
        self.client = client

    def publish(self, topic, data) -> None:
        self.client.publish(topic, data)
