from sqlalchemy import Column, String, DateTime, JSON, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    name = Column(String)
    role = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
