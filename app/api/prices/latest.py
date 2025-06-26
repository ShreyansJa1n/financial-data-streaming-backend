from typing import Optional
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.Database import get_async_db
from app.schemas.price import PriceResponse
from app.services.PriceService import PriceService

router = APIRouter()


@router.get(
    "/",
    response_model=PriceResponse,
    tags=["prices"],
    summary="Get latest price for a symbol",
)
async def get_latest_price(
    symbol: str,
    background_tasks: BackgroundTasks,
    provider: str = "alpha_vantage",
    request: Request = None,
    db: AsyncSession = Depends(get_async_db),
) -> Optional[PriceResponse]:
    price_service = PriceService(
        db=db,
        redis=request.app.state.redis_service,
        background_tasks=background_tasks,
    )
    response = await price_service.get_latest_price(
        symbol=symbol, provider=provider
    )

    if not response:
        return {"error": "Price not found"}, 404

    return response
