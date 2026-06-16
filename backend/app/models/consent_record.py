from sqlalchemy import Column, String, DateTime, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class ConsentRecord(Base):
    """Enregistrement GDPR persistant — NE JAMAIS SUPPRIMER."""
    __tablename__ = "consent_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    caller_phone_hash = Column(String, nullable=False, index=True)
    business_id = Column(String, nullable=False, index=True)
    channel = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    consent_given = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
