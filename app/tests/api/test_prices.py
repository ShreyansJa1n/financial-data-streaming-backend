import pytest
from httpx import AsyncClient, ASGITransport 
from app.main import app


@pytest.mark.asyncio
async def test_get_latest_price_endpoint(monkeypatch):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/prices/latest/",
            params={"symbol": "AAPL", "provider": "alpha_vantage"},
        )
        assert response.status_code in (200, 404)  # Depending on test DB state
