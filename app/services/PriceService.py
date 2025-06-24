from app import models
from app.services.PriceProviders import YahooFinanceProvider
from app.services.Database import get_db
from app.services.PriceProviders import AlphaVantageProvider
from app.services.Redis import RedisService


class PriceService:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
        self.providers = {
            "alpha_vantage": AlphaVantageProvider(),
            "yahoo_finance": YahooFinanceProvider(),
        }
        
    async def get_latest_price(self, symbol: str, provider: str):
        # Check Redis cache first
        cached_price = await self.redis.get(f"latest_price:{symbol}:{provider}")
        if cached_price:
            return cached_price
        
        # Fetch raw data from provider
        provider_instance = self.providers.get(provider)
        if not provider_instance:
            return {"error": "Provider not found"}, 404
        
        raw_data = provider_instance.fetch_raw_data(symbol)
        price_data = provider_instance.extract_price(raw_data)
        
        # Store raw data in database
        db_raw_data = models.RawPrice(
            symbol=symbol,
            price=price_data.get("price"),
            source=provider,
            raw_data=raw_data,
        )
        
        self.db.add(db_raw_data)
        self.db.commit()
        self.db.refresh(db_raw_data)
        
        # Create and store price point in database
        db_price_point = models.PricePoints(
            symbol=symbol,
            price=price_data.get("price"),
            source=provider,
            timestamp=price_data.get("timestamp"),
        )
        
        self.db.add(db_price_point)
        self.db.commit()
        self.db.refresh(db_price_point)
        
        # Prepare response data
        response_data = {
            "symbol": symbol,
            "price": price_data.get("price"),
            "provider": provider,
            "timestamp": price_data.get("timestamp"),
        }
        
        # Store in Redis cache
        await self.redis.set(f"latest_price:{symbol}:{provider}", response_data)
        
        return response_data