import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.PriceService import PriceService

@pytest.mark.asyncio
async def test_get_latest_price_returns_cached(monkeypatch):
    db = MagicMock()
    redis = AsyncMock()
    redis.get.return_value = {"symbol": "AAPL", "price": 100, "provider": "alpha_vantage"}
    background_tasks = MagicMock()
    service = PriceService(db, redis, background_tasks)
    result = await service.get_latest_price("AAPL", "alpha_vantage")
    assert result["symbol"] == "AAPL"
    redis.get.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_latest_price_provider_not_found():
    db = MagicMock()
    redis = AsyncMock()
    redis.get.return_value = None
    background_tasks = MagicMock()
    service = PriceService(db, redis, background_tasks)
    with pytest.raises(Exception):
        await service.get_latest_price("AAPL", "unknown_provider")