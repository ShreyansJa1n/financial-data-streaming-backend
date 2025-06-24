from confluent_kafka import Consumer
from app.core.config import settings


class KafkaConsumerService:
    def __init__(self, topics: list):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'auto.offset.reset': 'earliest',
            'group.id': 'fastapi-kafka-consumer',
        })
        self.consumer.subscribe(topics)

    def consume_messages(self, callback, timeout=1.0, max_messages=100):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))
            callback(msg.value().decode('utf-8'))

    def close(self):
        self.consumer.close()