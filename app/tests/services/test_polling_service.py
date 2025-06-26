import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.PollingService import PollingService


@pytest.mark.asyncio
async def test_call_own_endpoint_success(monkeypatch):
    polling = PollingService()
    mock_response = MagicMock()
    mock_response.status_code = 200
    with patch("httpx.AsyncClient.get", AsyncMock(return_value=mock_response)):
        result = await polling._call_own_endpoint("AAPL", "alpha_vantage")
        assert result is True


@pytest.mark.asyncio
async def test_call_own_endpoint_failure(monkeypatch):
    polling = PollingService()
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch("httpx.AsyncClient.get", AsyncMock(return_value=mock_response)):
        result = await polling._call_own_endpoint("AAPL", "alpha_vantage")
        assert result is False
