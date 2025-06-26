from pydantic import BaseModel, Field
from typing import List, Optional


class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: str
    provider: str


class PollRequest(BaseModel):
    symbols: List[str]
    interval: int = Field(..., description="Polling interval in seconds")
    provider: Optional[str] = Field(..., description="Market data provider")


class PollResponse(BaseModel):
    job_id: str
    status: str
    config: dict
