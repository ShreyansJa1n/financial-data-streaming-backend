from fastapi import APIRouter

from app.services.YahooFinanceProvider import YahooFinanceProvider
from app.services.AlphaVantageProvider import AlphaVantageProvider

router = APIRouter()

providers = {
    "alpha_vantage": AlphaVantageProvider(),
    "yahoo_finance": YahooFinanceProvider()
    
}

@router.get("/")
def get_latest_price(symbol: str, provider: str = "alpha_vantage"):
    provider_instance = providers.get(provider)
    if not provider_instance:
        return {"error": "Provider not found"}, 404

    raw_data = provider_instance.fetch_raw_data(symbol)
    price_data = provider_instance.extract_price(raw_data)

    return {
        "symbol": symbol,
        "price": price_data.get("price"),
        "timestamp": price_data.get("timestamp"),
        "provider": provider,
    }
