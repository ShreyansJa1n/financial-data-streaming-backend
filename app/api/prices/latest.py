from fastapi import APIRouter, Request

from app.services.YahooFinanceProvider import YahooFinanceProvider
from app.services.AlphaVantageProvider import AlphaVantageProvider
from app.services.Database import get_db

router = APIRouter()

providers = {
    "alpha_vantage": AlphaVantageProvider(),
    "yahoo_finance": YahooFinanceProvider()
    
}

@router.get("/")
async def get_latest_price(symbol: str, provider: str = "alpha_vantage", request: Request = None):
    provider_instance = providers.get(provider)
    if not provider_instance:
        return {"error": "Provider not found"}, 404

    # Check Redis cache first
    cached_price = await request.app.state.redis_service.get(f"latest_price:{symbol}:{provider}")
    if cached_price:
        print(f"Cache hit for {symbol} from {provider}")
        return cached_price

    raw_data = provider_instance.fetch_raw_data(symbol)
    price_data = provider_instance.extract_price(raw_data)

    returned_data = {
        "symbol": symbol,
        "price": price_data.get("price"),
        "timestamp": price_data.get("timestamp"),
        "provider": provider,
    }

    await request.app.state.redis_service.set(f"latest_price:{symbol}:{provider}", returned_data, expire=60)
    return returned_data
