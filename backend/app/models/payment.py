from sqlalchemy import Column, String, DateTime, JSON, Numeric
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    amount = Column(Numeric(18, 6), nullable=False)
    currency = Column(String, default="USDC")
    status = Column(String, default="pending")
    wallet_address = Column(String)
    tx_hash = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
