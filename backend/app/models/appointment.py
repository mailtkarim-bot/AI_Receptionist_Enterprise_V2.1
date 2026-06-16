from sqlalchemy import Column, String, DateTime, JSON
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    calendar_id = Column(String)
    status = Column(String, default="confirmed")
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
