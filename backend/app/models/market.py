import uuid
from sqlalchemy import Column, String, DateTime, Date, Numeric, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_definition_id = Column(String(36), ForeignKey("asset_definitions.id", ondelete="CASCADE"), nullable=False, unique=True)
    symbol = Column(String(50), nullable=False)
    price = Column(Numeric(18, 6), nullable=False)
    currency = Column(String(3), default="TWD")
    price_date = Column(Date, nullable=False)
    source_status = Column(String(20), default="VERIFIED")
    source_used = Column(String(50))
    source_detail = Column(JSONB)
    validation_level = Column(String(20))
    execution_snapshot_id = Column(String(36))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_definition_id = Column(String(36), ForeignKey("asset_definitions.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String(50), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    open = Column(Numeric(18, 6))
    high = Column(Numeric(18, 6))
    low = Column(Numeric(18, 6))
    close = Column(Numeric(18, 6), nullable=False)
    volume = Column(BigInteger)
    currency = Column(String(3), default="TWD")
    source = Column(String(50), nullable=False)
    validation_status = Column(String(20), default="LEVEL_1")
    execution_snapshot_id = Column(String(36))
    created_at = Column(DateTime, server_default=func.now())