from typing import Dict, Any
from app.services.PriceProviders.ProviderInterface import ProviderInterface
from app.core.config import settings
import yfinance as yf


class YahooFinanceProvider(ProviderInterface):
    def fetch_raw_data(self, symbol: str) -> Dict[str, Any]:
        ticker = yf.Ticker(symbol)
        hist = ticker.get_info()
        return hist

    def extract_price(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price": raw_data.get("currentPrice") or raw_data.get("regularMarketPrice"),
            "timestamp": raw_data.get("regularMarketTime"),
        }
