import uuid
from sqlalchemy import Column, String, DateTime, Date, Integer, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(String(36), ForeignKey("financial_models.id", ondelete="SET NULL"))
    category = Column(String(20), nullable=False)
    subcategory = Column(String(30))
    policy_name = Column(String(200), nullable=False)
    insurer_name = Column(String(100))
    policy_number = Column(String(100))
    coverage_amount = Column(Numeric(18, 2), nullable=False)
    annual_premium = Column(Numeric(18, 2))
    payment_period_years = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    covered_body_parts = Column(JSONB)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36))

class InsuranceProduct(Base):
    __tablename__ = "insurance_products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_code = Column(String(100), nullable=False, unique=True)
    product_name = Column(String(200), nullable=False)
    insurer_name = Column(String(100), nullable=False)
    category = Column(String(20), nullable=False)
    subcategory = Column(String(30))
    coverage_type = Column(String(50))
    covered_body_parts = Column(JSONB)
    coverage_amount = Column(Numeric(18, 2))
    annual_premium = Column(Numeric(18, 2))
    is_active = Column(Boolean, default=True)
    listed_at = Column(Date)
    delisted_at = Column(Date)
    source = Column(String(50))
    source_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class InsuranceProductsHistory(Base):
    __tablename__ = "insurance_products_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("insurance_products.id", ondelete="CASCADE"), nullable=False)
    change_type = Column(String(20), nullable=False)
    change_detail = Column(JSONB)
    changed_at = Column(DateTime, server_default=func.now())
    source = Column(String(50))

class BodyPartMapping(Base):
    __tablename__ = "body_part_mapping"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    part_code = Column(String(30), nullable=False, unique=True)
    part_name = Column(String(100), nullable=False)
    category = Column(String(20), nullable=False)
    description = Column(Text)
    related_diseases = Column(JSONB)
    required_coverage = Column(Numeric(18, 2))
    ui_config = Column(JSONB)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class InsuranceGapSnapshot(Base):
    __tablename__ = "insurance_gap_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    part_code = Column(String(30), ForeignKey("body_part_mapping.part_code"), nullable=False)
    existing_coverage = Column(Numeric(18, 2), default=0)
    required_coverage = Column(Numeric(18, 2), nullable=False)
    coverage_ratio = Column(Numeric(6, 4), nullable=False)
    state = Column(String(10), nullable=False)
    calculation_detail = Column(JSONB)
    execution_snapshot_id = Column(String(36))
    created_at = Column(DateTime, server_default=func.now())