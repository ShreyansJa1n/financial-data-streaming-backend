from fastapi import FastAPI, APIRouter
from app.api.prices.latest import latest_router

api_router = APIRouter()
api_router.include_router(latest_router, prefix="/prices", tags=["prices"])
