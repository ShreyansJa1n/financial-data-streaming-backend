from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/latest")
def get_latest_price():
    return {
        "symbol": "AAPL",
        "price": 150.25,
        "timestamp": "2024-03-20T10:30:00Z",
        "provider": "alpha_vantage",
    }
