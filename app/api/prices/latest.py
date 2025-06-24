from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.services.Database import get_db
from app.schemas.price import LatestPrice
from app.services.PriceService import PriceService

router = APIRouter()

@router.get(
    "/",
    response_model=LatestPrice,
    tags=["prices"],
    summary="Get latest price for a symbol",
)
async def get_latest_price(\
    symbol: str, provider: str = "alpha_vantage", request: Request = None, db: Session = Depends(get_db)
) -> Optional[LatestPrice]:
    price_service = PriceService(db=get_db(), redis=request.app.state.redis_service)
    response = await price_service.get_latest_price(symbol=symbol, provider=provider)
    
    if not response:
        return {"error": "Price not found"}, 404
    
    return response