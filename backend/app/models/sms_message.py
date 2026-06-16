from sqlalchemy import Column, String, DateTime, JSON
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class SMSMessage(Base):
    __tablename__ = "sms_messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, index=True)
    direction = Column(String, default="inbound")
    phone_number = Column(String)
    content = Column(String)
    status = Column(String, default="received")
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
