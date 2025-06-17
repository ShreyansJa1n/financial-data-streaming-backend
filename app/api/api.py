from fastapi import FastAPI, APIRouter
from app.api.prices.latest import router as latest_router
from app.api.prices.poll import router as poll_router

api_router = APIRouter()
api_router.include_router(latest_router, prefix="/prices", tags=["prices"])
api_router.include_router(poll_router, prefix="/prices", tags=["prices"])
