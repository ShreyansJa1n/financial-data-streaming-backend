from sqlalchemy import (
    Column,
    String,
    UUID,
    DateTime,
    ForeignKey,
    Float,
    JSON,
    Integer,
    Index,
)
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Base class for declarative models
Base = declarative_base()


class RawPrice(Base):
    __tablename__ = "raw_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    source = Column(String(50), nullable=False)
    raw_data = Column(JSON, nullable=True)


class PricePoints(Base):
    __tablename__ = "price_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), index=True
    )
    provider = Column(String, nullable=False)
    raw_response_id = Column(UUID(as_uuid=True), ForeignKey("raw_prices.id"))


class SymbolAverage(Base):
    __tablename__ = "symbol_averages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    average = Column(Float, nullable=False)
    window = Column(Integer, default=5)
    timestamp = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), index=True
    )


class PollingJob(Base):
    __tablename__ = "polling_jobs"
    id = Column(String, primary_key=True)
    symbols = Column(JSON, nullable=False)
    interval = Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    status = Column(String, default="accepted")
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )


Index(
    "ix_price_points_symbol_timestamp",
    PricePoints.symbol,
    PricePoints.timestamp,
)
Index(
    "ix_symbol_averages_symbol_timestamp",
    SymbolAverage.symbol,
    SymbolAverage.timestamp,
)
