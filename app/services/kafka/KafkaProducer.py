from confluent_kafka import Producer
import json
from app.core.logging import logger as logging
from app.core.config import settings

producer = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def publish_price_event(event: dict):
    try:
        producer.produce(
            settings.KAFKA_PRICE_TOPIC,
            value=json.dumps(event).encode("utf-8"),
            callback=delivery_report,
        )
        logging.debug("Published event successfully ::DEBUG::")
        producer.poll(0)
    except Exception as e:
        logging.error(f"Kafka publish error: {e}")
