import uuid
from sqlalchemy import Column, String, DateTime, Date, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class ForecastInput(Base):
    __tablename__ = "forecast_inputs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    user_snapshot = Column(JSONB, nullable=False)
    data_quality = Column(String(20), default="GOOD")
    market_snapshot_refs = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())

class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(String(36), ForeignKey("financial_models.id", ondelete="CASCADE"), nullable=False)
    model_version = Column(String(20), nullable=False)
    input_snapshot_id = Column(String(36), ForeignKey("forecast_inputs.id"), nullable=False)
    simulation_count = Column(Integer, nullable=False)
    horizon_months = Column(Integer, nullable=False)
    status = Column(String(20), default="completed")
    execution_snapshot_id = Column(String(36))
    generated_at = Column(DateTime, server_default=func.now())

class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String(36), ForeignKey("forecast_runs.id", ondelete="CASCADE"), nullable=False)
    metric = Column(String(50), nullable=False)
    value = Column(Numeric(10, 6), nullable=False)
    confidence_interval_low = Column(Numeric(10, 6))
    confidence_interval_high = Column(Numeric(10, 6))
    execution_snapshot_id = Column(String(36))
    created_at = Column(DateTime, server_default=func.now())