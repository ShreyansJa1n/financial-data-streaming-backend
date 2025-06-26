from fastapi import APIRouter, status, Depends, Request, BackgroundTasks
from app.schemas.price import PollResponse, PollRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.Database import get_async_db
from app.services.PriceService import PriceService

router = APIRouter()


@router.post(
    "/", response_model=PollResponse, status_code=status.HTTP_202_ACCEPTED
)
async def poll_prices(
    req: PollRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
    request: Request = None,
):
    service = PriceService(
        db=db,
        redis=request.app.state.redis_service,
        background_tasks=background_tasks,
    )
    job = await service.start_polling_job(req)
    return job
