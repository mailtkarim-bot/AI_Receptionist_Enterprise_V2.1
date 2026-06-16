from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from app.db.database import get_db
from app.models.payment import Payment
from app.models.business import Business
from app.services.tier_manager import get_current_business, check_feature_access
from app.schemas.web3 import PaymentRequest, PaymentResponse, PaymentVerifyRequest

router = APIRouter()

class InvoiceCreate(BaseModel):
    amount: Decimal
    description: Optional[str] = None

@router.get("/wallet")
async def get_wallet(business: Business = Depends(get_current_business)):
    check_feature_access(business, "web3")
    return {"business_id": business.id, "wallet_address": "0x...", "network": "base"}

@router.post("/invoice", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(data: InvoiceCreate, business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    check_feature_access(business, "web3")
    payment = Payment(business_id=business.id, amount=data.amount, currency="USDC", status="pending", wallet_address="0x...")
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return PaymentResponse(id=payment.id, status=payment.status, amount=payment.amount, currency=payment.currency, wallet_address=payment.wallet_address, tx_hash=None)

@router.get("/invoices")
async def list_invoices(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    check_feature_access(business, "web3")
    result = await db.execute(select(Payment).where(Payment.business_id == business.id).order_by(desc(Payment.created_at)))
    return result.scalars().all()

@router.post("/verify")
async def verify_payment(data: PaymentVerifyRequest, business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    check_feature_access(business, "web3")
    return {"success": True, "tx_hash": data.tx_hash, "status": "confirmed"}
