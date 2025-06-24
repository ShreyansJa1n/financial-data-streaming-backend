from confluent_kafka import KafkaProducer
import json
from app.core.config import settings

class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        
    def _serialize_message(self, message: dict) -> bytes:
        return json.dumps(message).encode("utf-8")

    def send_message(self, topic: str, message: dict):
        try:
            serialized_message = self._serialize_message(message)
            self.producer.send(topic, value=serialized_message)
            self.producer.flush()
            print(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            print(f"Failed to send message to topic {topic}: {e}")