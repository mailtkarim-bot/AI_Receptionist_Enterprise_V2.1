from sqlalchemy import Column, String, DateTime, JSON, Numeric, Boolean
from app.db.database import Base
from datetime import datetime, timezone
import uuid

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, nullable=False, index=True)
    invoice_id = Column(String)
    amount = Column(Numeric(20, 8))
    currency = Column(String, default="USDC")
    status = Column(String, default="pending")
    tx_hash = Column(String)
    wallet_address = Column(String)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    confirmed_at = Column(DateTime)
