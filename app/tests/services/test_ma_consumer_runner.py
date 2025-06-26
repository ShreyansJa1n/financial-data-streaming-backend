import pytest
from unittest.mock import AsyncMock
from app.services.kafka.ma_consumer_runner import PriceEventConsumer


@pytest.mark.asyncio
async def test_process_price_event(monkeypatch):
    consumer = PriceEventConsumer()
    db = AsyncMock()
    event = {"symbol": "AAPL", "price": 100, "timestamp": "2025-06-25T12:00:00Z"}
    db.execute.return_value.fetchall = AsyncMock(
        return_value=[(100,), (101,), (102,), (103,)]
    )
    await consumer._process_price_event(db, event)
    db.add.assert_called()
    db.commit.assert_awaited()
