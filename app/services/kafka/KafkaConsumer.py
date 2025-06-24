"""
Kafka consumer for moving average calculation.
"""
from confluent_kafka import Consumer
import json
import logging
from app.core.config import get_settings
from app.models.market import PricePoint, SymbolAverage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime

settings = get_settings()

consumer = Consumer({
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'ma-consumer',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([settings.KAFKA_PRICE_TOPIC])

async def process_price_event(db: AsyncSession, event: dict):
    symbol = event['symbol']
    price = event['price']
    timestamp = event['timestamp']
    # Fetch last 4 prices (plus this one = 5)
    result = await db.execute(
        select(PricePoint.price).where(PricePoint.symbol == symbol).order_by(desc(PricePoint.timestamp)).limit(4)
    )
    prices = [row[0] for row in result.fetchall()]
    prices = [price] + prices
    if len(prices) == 5:
        avg = sum(prices) / 5
        avg_obj = SymbolAverage(
            symbol=symbol,
            average=avg,
            window=5,
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        )
        db.add(avg_obj)
        await db.commit()

# Consumer loop (to be run in a background task)
def consume_loop(db: AsyncSession):
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue
            event = json.loads(msg.value().decode('utf-8'))
            # Should be run in async context
            # await process_price_event(db, event)
    except Exception as e:
        logging.error(f"Kafka consumer error: {e}")
    finally:
        consumer.close()
