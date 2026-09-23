import uuid
from sqlalchemy import Column, String, DateTime, Date, Integer, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class EngineVersion(Base):
    __tablename__ = "engine_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engine_type = Column(String(30), nullable=False)
    version = Column(String(30), nullable=False)
    config = Column(JSONB, nullable=False)
    status = Column(String(20), default="draft")
    description = Column(Text)
    created_by = Column(String(36))
    activated_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ExecutionSnapshot(Base):
    __tablename__ = "execution_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_date = Column(Date, nullable=False)
    crawler_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    normalizer_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    validator_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    matcher_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    monte_carlo_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    llm_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    status = Column(String(20), default="pending")
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)

class EngineTrace(Base):
    __tablename__ = "engine_traces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_snapshot_id = Column(String(36), ForeignKey("execution_snapshots.id", ondelete="CASCADE"))
    engine_type = Column(String(30), nullable=False)
    parent_trace_id = Column(String(36), ForeignKey("engine_traces.id"))
    step_name = Column(String(100))
    input_data = Column(JSONB)
    output_data = Column(JSONB)
    status = Column(String(20))
    duration_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class RecomputeJob(Base):
    __tablename__ = "recompute_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engine_type = Column(String(30), nullable=False)
    from_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    to_version_id = Column(String(36), ForeignKey("engine_versions.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default="pending")
    affected_records = Column(Integer, default=0)
    error_message = Column(Text)
    created_by = Column(String(36))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class LlmUsageLog(Base):
    __tablename__ = "llm_usage_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    provider = Column(String(30), nullable=False)
    request_type = Column(String(50))
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    cost_usd = Column(Numeric(10, 6), default=0)
    latency_ms = Column(Integer)
    status = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

class EngineCacheInvalidation(Base):
    __tablename__ = "engine_cache_invalidations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engine_type = Column(String(30), nullable=False)
    version_id = Column(String(36), ForeignKey("engine_versions.id"))
    published_at = Column(DateTime, server_default=func.now())
    subscriber_count = Column(Integer, default=0)