from sqlalchemy import Column, String, DateTime, JSON, Integer, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Business(Base):
    __tablename__ = "businesses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String)
    tier = Column(String, default="basic")
    features = Column(JSON, default=list)
    limits = Column(JSON, default=dict)
    settings = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)  # ARCH-07: permet de suspendre/bannir
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
