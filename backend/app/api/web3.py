"""Web3 payments with real on-chain verification."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from app.db.database import get_db
from app.models.payment import Payment
from app.models.business import Business
from app.services.tier_manager import get_current_business, check_feature_access
from app.schemas.web3 import PaymentResponse, PaymentVerifyRequest
from app.core.config import get_settings
from web3 import Web3

router = APIRouter()


class InvoiceCreate(BaseModel):
    amount: Decimal
    description: Optional[str] = None


@router.get("/wallet")
async def get_wallet(business: Business = Depends(get_current_business)):
    check_feature_access(business, "web3")
    settings = get_settings()
    return {
        "business_id": business.id,
        "wallet_address": settings.PLATFORM_WALLET_ADDRESS,
        "network": settings.BLOCKCHAIN_NETWORK,
        "usdc_contract": settings.USDC_CONTRACT_ADDRESS,
    }


@router.post("/invoice", response_model=PaymentResponse, status_code=201)
async def create_invoice(
    data: InvoiceCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    check_feature_access(business, "web3")
    settings = get_settings()
    payment = Payment(
        business_id=business.id,
        amount=data.amount,
        currency="USDC",
        status="pending",
        wallet_address=settings.PLATFORM_WALLET_ADDRESS,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return PaymentResponse(
        id=payment.id,
        status=payment.status,
        amount=payment.amount,
        currency=payment.currency,
        wallet_address=payment.wallet_address,
        tx_hash=None,
    )


@router.get("/invoices")
async def list_invoices(
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    check_feature_access(business, "web3")
    result = await db.execute(
        select(Payment)
        .where(Payment.business_id == business.id)
        .order_by(desc(Payment.created_at))
        .offset(skip)
        .limit(min(limit, 100))
    )
    return result.scalars().all()


@router.post("/verify")
async def verify_payment(
    data: PaymentVerifyRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    check_feature_access(business, "web3")
    settings = get_settings()

    if not settings.WEB3_RPC_URL:
        raise HTTPException(status_code=500, detail="Web3 RPC not configured")

    w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL, request_kwargs={"timeout": 10}))
    if not w3.is_connected():
        raise HTTPException(status_code=503, detail="Blockchain RPC unavailable")

    try:
        tx = w3.eth.get_transaction(data.tx_hash)
    except Exception:
        raise HTTPException(status_code=400, detail="Transaction not found")

    if tx.get("to", "").lower() != settings.PLATFORM_WALLET_ADDRESS.lower():
        raise HTTPException(status_code=400, detail="Invalid recipient")

    receipt = w3.eth.get_transaction_receipt(data.tx_hash)
    if receipt.status != 1:
        raise HTTPException(status_code=400, detail="Transaction failed")

    result = await db.execute(
        select(Payment).where(Payment.business_id == business.id, Payment.status == "pending")
    )
    payment = result.scalars().first()
    if payment:
        payment.status = "confirmed"
        payment.tx_hash = data.tx_hash
        await db.commit()

    return {
        "success": True,
        "tx_hash": data.tx_hash,
        "status": "confirmed",
        "block": receipt.blockNumber,
    }
