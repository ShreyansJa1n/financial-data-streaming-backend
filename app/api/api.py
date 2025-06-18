from fastapi import APIRouter
from app.api.prices.prices import prices_router

api_router = APIRouter()
api_router.include_router(prices_router, prefix="/prices", tags=["prices"])
