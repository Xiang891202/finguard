import uuid
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from app.db.base import Base

class FinancialModel(Base):
    __tablename__ = "financial_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    base_currency = Column(String(3), default="TWD")
    emergency_fund_months = Column(Integer, default=6)
    is_default = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36))

class Vault(Base):
    __tablename__ = "vaults"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(String(36), ForeignKey("financial_models.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    vault_type = Column(String(20), nullable=False)
    currency = Column(String(3), default="TWD")
    amount = Column(Numeric(18, 2), default=0)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36))

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(String(36), ForeignKey("financial_models.id", ondelete="CASCADE"), nullable=False)
    asset_definition_id = Column(String(36), ForeignKey("asset_definitions.id"), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    average_cost = Column(Numeric(18, 4))
    currency = Column(String(3), default="TWD")
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36))

class Liability(Base):
    __tablename__ = "liabilities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(String(36), ForeignKey("financial_models.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    liability_type = Column(String(20), nullable=False)
    total_amount = Column(Numeric(18, 2), nullable=False)
    remaining_amount = Column(Numeric(18, 2), nullable=False)
    interest_rate = Column(Numeric(5, 4))
    monthly_payment = Column(Numeric(18, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    currency = Column(String(3), default="TWD")
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36))