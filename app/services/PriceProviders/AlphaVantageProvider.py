from datetime import datetime
from typing import Any, Dict
import requests
from app.core.config import settings
from app.services.PriceProviders.ProviderInterface import ProviderInterface


class AlphaVantageProvider(ProviderInterface):
    def fetch_raw_data(self, symbol: str) -> Dict[str, Any]:
        # Just return the raw API response
        return requests.get(
            f"""https://www.alphavantage.co/query?function=
            GLOBAL_QUOTE&symbol={symbol}&
            apikey={settings.ALPHA_VANTAGE_API_KEY}"""
        ).json()

    def extract_price(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        quote = raw_data["Global Quote"]
        return {
            "price": float(quote["05. price"]),
            "timestamp": datetime.now(),
        }
