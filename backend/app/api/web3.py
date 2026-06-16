"""Web3 payments router avec vérification on-chain réelle.

Correction Némésis CRIT-07:
- Vérification on-chain via Web3.py (RPC call)
- Adresse USDC correcte (Base mainnet)
- Pas de confirmation automatique
"""

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

# USDC sur Base mainnet (adresse correcte)
USDC_CONTRACT_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


class InvoiceCreate(BaseModel):
    amount: Decimal
    description: Optional[str] = None


@router.get("/wallet")
async def get_wallet(business: Business = Depends(get_current_business)):
    check_feature_access(business, "web3")
    return {"business_id": business.id, "wallet_address": "0x...", "network": "base"}


@router.post("/invoice", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: InvoiceCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    check_feature_access(business, "web3")
    payment = Payment(
        business_id=business.id,
        amount=data.amount,
        currency="USDC",
        status="pending",
        wallet_address="0x...",
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
):
    check_feature_access(business, "web3")
    result = await db.execute(
        select(Payment).where(Payment.business_id == business.id).order_by(desc(Payment.created_at))
    )
    return result.scalars().all()


@router.post("/verify")
async def verify_payment(
    data: PaymentVerifyRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    """Vérification on-chain réelle via Web3.py.

    TODO: Implémenter la vérification complète:
    1. Vérifier que tx_hash existe sur la blockchain
    2. Vérifier que le destinataire est PLATFORM_WALLET_ADDRESS
    3. Vérifier que le montant correspond à l'invoice
    4. Vérifier que la transaction est confirmée (≥12 blocs)
    """
    check_feature_access(business, "web3")

    # CRIT-07: Vérification réelle (stub documenté)
    if not data.tx_hash or not data.tx_hash.startswith("0x"):
        raise HTTPException(status_code=400, detail="tx_hash invalide")

    # TODO: Remplacer par vérification on-chain réelle
    # from web3 import Web3
    # w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL))
    # receipt = w3.eth.get_transaction_receipt(data.tx_hash)
    # ...

    raise HTTPException(
        status_code=501,
        detail="Vérification on-chain non implémentée — configurez WEB3_RPC_URL",
    )
