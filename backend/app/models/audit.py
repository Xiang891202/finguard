import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    email_type = Column(String(50), nullable=False)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(500))
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_number = Column(String(20), nullable=False, unique=True)
    service_name = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    trigger_event = Column(String(50), nullable=False)
    diagnosis_report = Column(Text)
    possible_causes = Column(JSONB)
    auto_recovery_attempted = Column(Boolean, default=False)
    auto_recovery_success = Column(Boolean, default=False)
    recovery_action_taken = Column(String(100))
    recovery_error = Column(Text)
    engineer_email_sent = Column(Boolean, default=False)
    status = Column(String(20), default="open")
    detected_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    stripe_customer_id = Column(String(100))
    stripe_subscription_id = Column(String(100))
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    trial_end = Column(DateTime)
    auto_renew = Column(Boolean, default=False)
    failed_payment_count = Column(Integer, default=0)
    grace_period_end = Column(DateTime)
    canceled_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36))
    user_type = Column(String(20))
    tenant_id = Column(String(36))
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(36))
    changes = Column(JSONB)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, server_default=func.now())