from fastapi import APIRouter
from app.api.prices.latest import router as latest_router
from app.api.prices.poll import router as poll_router

prices_router = APIRouter()
prices_router.include_router(latest_router, prefix="/latest", tags=["prices"])
prices_router.include_router(poll_router, prefix="/poll", tags=["prices"])