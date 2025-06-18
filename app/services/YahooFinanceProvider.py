from typing import Dict, Any
from app.services.ProviderInterface import ProviderInterface
from app.core.config import settings
import yfinance as yf

class YahooFinanceProvider(ProviderInterface):
    def fetch_raw_data(self, symbol: str) -> Dict[str, Any]:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1m")
        return hist.to_dict()
    
    def extract_price(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        close_prices = raw_data['Close']
        latest_timestamp = max(close_prices.keys())
        return {
            "price": close_prices[latest_timestamp],
            "timestamp": latest_timestamp,
        }