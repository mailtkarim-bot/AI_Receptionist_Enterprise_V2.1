from sqlalchemy import Column, String, DateTime, JSON, Integer, Float
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Call(Base):
    __tablename__ = "calls"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, index=True)
    direction = Column(String, default="inbound")
    status = Column(String, default="pending")
    phone_number = Column(String)
    duration = Column(Integer)
    transcript = Column(JSON)
    recording_url = Column(String)
    notes = Column(JSON, default=list)
    sentiment = Column(String)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime)
