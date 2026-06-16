from sqlalchemy import Column, String, DateTime, JSON, Integer
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String)
    status = Column(String, default="draft")
    target_audience = Column(JSON)
    message_template = Column(String)
    schedule = Column(JSON)
    stats = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
