from sqlalchemy import JSON, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class RawPrice(Base):
    __tablename__ = 'raw_prices'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    price = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    source = Column(String(50), nullable=False)
    raw_data = Column(JSON, nullable=True)
