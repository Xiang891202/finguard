import uuid
from sqlalchemy import Column, String, DateTime, Date, Integer, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class UserHealthProfile(Base):
    __tablename__ = "user_health_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    family_history = Column(JSONB)
    has_genetic_test = Column(Boolean, default=False)
    consent_genetic = Column(Boolean, default=False)
    consent_genetic_at = Column(DateTime)
    completion_rate = Column(Numeric(5, 2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class GeneticMarker(Base):
    __tablename__ = "genetic_markers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    marker_code = Column(String(50), nullable=False, unique=True)
    marker_name = Column(String(100), nullable=False)
    related_diseases = Column(JSONB, nullable=False)
    related_body_parts = Column(JSONB)
    risk_level_high = Column(Numeric(4, 2), default=2.0)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class UserGeneticTest(Base):
    __tablename__ = "user_genetic_tests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    marker_id = Column(String(36), ForeignKey("genetic_markers.id"), nullable=False)
    result = Column(String(20), nullable=False)
    raw_data_encrypted = Column(Text)
    risk_level_computed = Column(Numeric(4, 2))
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class MedicalCostReference(Base):
    __tablename__ = "medical_cost_references"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    disease_code = Column(String(50), nullable=False, unique=True)
    disease_name = Column(String(200), nullable=False)
    related_body_part = Column(String(30), ForeignKey("body_part_mapping.part_code"))
    cost_min = Column(Numeric(18, 2), nullable=False)
    cost_max = Column(Numeric(18, 2), nullable=False)
    cost_avg = Column(Numeric(18, 2))
    currency = Column(String(3), default="TWD")
    source = Column(String(100))
    effective_date = Column(Date)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class DiseaseRiskMapping(Base):
    __tablename__ = "disease_risk_mapping"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    body_part_code = Column(String(30), ForeignKey("body_part_mapping.part_code"), nullable=False)
    disease_code = Column(String(50), nullable=False)
    age_risk_multiplier = Column(JSONB)
    gender_risk_multiplier = Column(JSONB)
    family_history_multiplier = Column(Numeric(4, 2), default=1.5)
    genetic_multiplier = Column(Numeric(4, 2), default=1.5)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())