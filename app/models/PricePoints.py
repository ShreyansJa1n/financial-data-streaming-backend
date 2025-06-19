from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from app.services.Database import Base

class PricePoints(Base):
    __tablename__ = 'price_points'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    price = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)
    timestamp = Column(String(50), nullable=False, index=True)