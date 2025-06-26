"""
Kafka moving average consumer runner for background execution.
"""

import asyncio
from app.core.Database import SessionLocal
from app.core.logging import logger as logging
from confluent_kafka import Consumer
from app.core.config import settings
from app.models.market import PricePoints, SymbolAverage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timezone


class PriceEventConsumer:
    def __init__(self):
        self.running = False
        self.consumer: Consumer = Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": "ma-consumer",
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe([settings.KAFKA_PRICE_TOPIC])

    async def start_ma_consumer(self):
        """Start the moving average Kafka consumer in a background task."""

        logging.debug("Starting ma consumer")

        self.running = True
        async with SessionLocal() as db:
            while self.running:
                msg = self.consumer.poll(1.0)
                logging.debug(f"DEBUG: Testing the freq of this loop., {msg}")
                if msg is None:
                    continue
                if msg.error():
                    continue
                event = msg.value()
                try:
                    import json

                    event = json.loads(event.decode("utf-8"))
                    await self._process_price_event(db, event)
                except Exception as e:
                    logging.error(f"Error while consuming: {e}", exc_info=True)

                await asyncio.sleep(5)

    def stop_ma_consumer(self):
        """Stop the moving average Kafka consumer and close the connection."""
        self.running = False
        self.consumer.close()

    async def _process_price_event(self, db: AsyncSession, event: dict):
        symbol = event["symbol"]
        price = event["price"]
        # Fetch last 4 prices (plus this one = 5)
        result = await db.execute(
            select(PricePoints.price)
            .where(PricePoints.symbol == symbol)
            .order_by(desc(PricePoints.timestamp))
            .limit(4)
        )
        prices = [row[0] for row in result.fetchall()]
        prices = [price] + prices
        logging.debug("Received an event, processing it")
        if len(prices) == 5:
            avg = sum(prices) / 5
            avg_obj = SymbolAverage(
                symbol=symbol,
                average=avg,
                window=5,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(avg_obj)
            await db.commit()
