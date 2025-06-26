from app.models.market import PollingJob, RawPrice, PricePoints
from app.schemas.price import PollRequest, PollResponse
from app.services.PriceProviders.YahooFinanceProvider import (
    YahooFinanceProvider,
)
from app.services.PriceProviders.AlphaVantageProvider import (
    AlphaVantageProvider,
)
from app.services.kafka.KafkaProducer import publish_price_event
from fastapi import BackgroundTasks, HTTPException
from datetime import datetime, timezone
import uuid
import asyncio


class PriceService:
    def __init__(self, db, redis, background_tasks: BackgroundTasks):
        self.db = db
        self.redis = redis
        self.providers = {
            "alpha_vantage": AlphaVantageProvider(),
            "yahoo_finance": YahooFinanceProvider(),
        }
        self.background_tasks = background_tasks

    async def get_latest_price(self, symbol: str, provider: str):
        # Check Redis cache first
        cached_price = await self.redis.get(f"latest_price:{symbol}:{provider}")
        if cached_price:
            return cached_price

        # Fetch raw data from provider
        provider_instance = self.providers.get(provider)
        if not provider_instance:
            raise HTTPException(status_code=404, detail="Provider not found")

        raw_data = await asyncio.to_thread(
            provider_instance.fetch_raw_data, symbol
        )
        price_data = await asyncio.to_thread(
            provider_instance.extract_price, raw_data
        )

        # Store raw data in database
        db_raw_data = RawPrice(
            id=uuid.uuid4(),
            symbol=symbol,
            price=price_data.get("price"),
            source=provider,
            raw_data=raw_data,
        )

        self.db.add(db_raw_data)
        await self.db.commit()
        await self.db.refresh(db_raw_data)

        # Create and store price point in database
        db_price_point = PricePoints(
            id=uuid.uuid4(),
            symbol=symbol,
            price=price_data.get("price"),
            provider=provider,
            timestamp=datetime.now(timezone.utc),
            raw_response_id=str(db_raw_data.id),
        )

        self.db.add(db_price_point)
        await self.db.commit()
        await self.db.refresh(db_price_point)

        # Prepare response data
        response_data = {
            "symbol": symbol,
            "price": price_data.get("price"),
            "provider": provider,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        price_event = {
            "symbol": symbol,
            "price": price_data.get("price"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": provider,
            "raw_response_id": str(db_raw_data.id),
        }

        self.background_tasks.add_task(publish_price_event, price_event)

        # Store in Redis cache
        await self.redis.set(f"latest_price:{symbol}:{provider}", response_data)

        return response_data

    async def start_polling_job(self, req: PollRequest) -> PollResponse:
        job_id = f"poll_{uuid.uuid4().hex[:8]}"
        if req.provider not in self.providers:
            raise HTTPException(404, detail="Provider does not exist.")
        job = PollingJob(
            id=job_id,
            symbols=req.symbols,
            interval=req.interval,
            provider=req.provider,
            status="accepted",
        )
        self.db.add(job)
        await self.db.commit()
        return PollResponse(
            job_id=job_id,
            status="accepted",
            config={"symbols": req.symbols, "interval": req.interval},
        )
