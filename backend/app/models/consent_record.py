from sqlalchemy import Column, String, DateTime, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class ConsentRecord(Base):
    """Enregistrement GDPR persisté en base — NE JAMAIS SUPPRIMER."""
    __tablename__ = "consent_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    caller_phone_hash = Column(String, nullable=False, index=True)
    business_id = Column(String, nullable=False, index=True)
    channel = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    consent_given = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

class BreachLog(Base):
    """Log de breach GDPR (Art. 33) — persistance légale obligatoire."""
    __tablename__ = "breach_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)
    detected_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    notified_at = Column(DateTime)
