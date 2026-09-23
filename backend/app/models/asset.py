import uuid
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base


class AssetClass(Base):
    __tablename__ = "asset_classes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    handler_class = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AssetDefinition(Base):
    __tablename__ = "asset_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_class_id = Column(String(36), ForeignKey("asset_classes.id"), nullable=False)
    symbol = Column(String(50), nullable=False)
    display_name = Column(String(100), nullable=False)
    currency = Column(String(3), default="TWD")
    source_config = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())