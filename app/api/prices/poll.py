from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.post("/poll", status_code=202)
def create_poll(poll: dict):
    print(poll)
    return {
        "job_id": "poll_123",
        "status": "accepted",
        "config": {"symbols": ["AAPL", "MSFT"], "interval": 60},
    }
