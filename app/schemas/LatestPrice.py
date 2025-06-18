from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class LatestPrice(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    provider: str
    
    class Config:
        from_attributes = True