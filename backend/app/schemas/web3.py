from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal
    currency: str = "USDC"
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    status: str
    amount: Decimal
    currency: str
    wallet_address: str
    tx_hash: Optional[str]

class PaymentVerifyRequest(BaseModel):
    tx_hash: str
