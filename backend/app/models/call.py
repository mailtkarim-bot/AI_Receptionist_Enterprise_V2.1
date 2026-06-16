from sqlalchemy import Column, String, DateTime, JSON, Integer
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Call(Base):
    __tablename__ = "calls"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, index=True)
    direction = Column(String, nullable=False)
    status = Column(String, default="initiated")
    phone_number = Column(String)
    recording_url = Column(String)
    notes = Column(JSON, default=list)
    metadata = Column(JSON, default=dict)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
