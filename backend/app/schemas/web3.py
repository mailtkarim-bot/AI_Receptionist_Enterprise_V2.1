from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    status: str
    amount: Decimal
    currency: str
    wallet_address: Optional[str] = None
    tx_hash: Optional[str] = None

    class Config:
        from_attributes = True

class PaymentVerifyRequest(BaseModel):
    tx_hash: str = Field(..., pattern=r"^0x[a-fA-F0-9]{64}$")
