from sqlalchemy import Column, String, DateTime, JSON, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    name = Column(String)
    phone = Column(String, index=True)
    email = Column(String)
    tags = Column(JSON, default=list)
    preferences = Column(JSON, default=dict)
    embedding = Column(JSON)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
