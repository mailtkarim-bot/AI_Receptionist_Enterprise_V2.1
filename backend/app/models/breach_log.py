from sqlalchemy import Column, String, DateTime
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class BreachLog(Base):
    """Log de breach GDPR (Art. 33) — persistance légale obligatoire."""
    __tablename__ = "breach_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)
    detected_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    notified_at = Column(DateTime)
