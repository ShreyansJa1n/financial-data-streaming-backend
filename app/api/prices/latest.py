from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.services.YahooFinanceProvider import YahooFinanceProvider
from app.services.AlphaVantageProvider import AlphaVantageProvider
from app.services.Database import get_db
from app.schemas.LatestPrice import LatestPrice
from app import models

router = APIRouter()

providers = {
    "alpha_vantage": AlphaVantageProvider(),
    "yahoo_finance": YahooFinanceProvider(),
}


@router.get(
    "/",
    response_model=LatestPrice,
    tags=["prices"],
    summary="Get latest price for a symbol",
)
async def get_latest_price(\
    symbol: str, provider: str = "alpha_vantage", request: Request = None, db: Session = Depends(get_db)
):
    provider_instance = providers.get(provider)
    if not provider_instance:
        return {"error": "Provider not found"}, 404

    # Check Redis cache first
    cached_price = await request.app.state.redis_service.get(
        f"latest_price:{symbol}:{provider}"
    )
    if cached_price:
        
        return LatestPrice(
            symbol=cached_price["symbol"],
            price=cached_price["price"],
            provider=cached_price["provider"],
            timestamp=cached_price["timestamp"],
        )
        
    

    raw_data = provider_instance.fetch_raw_data(symbol)
    price_data = provider_instance.extract_price(raw_data)
        
    db_raw_data = models.RawPrice(
        symbol=symbol,
        price=price_data.get("price"),
        source=provider,
        raw_data=raw_data,
    )

    db.add(db_raw_data)
    db.commit()
    db.refresh(db_raw_data)
    
    returned_data = LatestPrice(
        symbol=symbol,
        price=price_data.get("price"),
        provider=provider,
        timestamp=price_data.get("timestamp"),
    )
    
    db_price_point = models.PricePoints(
        symbol=symbol,
        price=price_data.get("price"),
        source=provider,
        timestamp=returned_data.timestamp,
    )
    db.add(db_price_point)
    db.commit()
    db.refresh(db_price_point)

    await request.app.state.redis_service.set(
        f"latest_price:{symbol}:{provider}",
        {
            "symbol": symbol,
            "price": price_data.get("price"),
            "provider": provider,
            "timestamp": returned_data.timestamp,
        },
        expire=60,
    )
    
    return returned_data
