"""Business management router avec flag_modified + upgrade sécurisé.

Corrections Némésis:
- flag_modified pour mutations JSON
- is_active check
- Upgrade nécessite validation paiement (stub sécurisé)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import attributes
from pydantic import BaseModel

from app.db.database import get_db
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.schemas.auth import BusinessResponse, BusinessUpdate

router = APIRouter()


class UpgradeRequest(BaseModel):
    tier: str


class UsageResponse(BaseModel):
    calls_used: int
    calls_limit: int
    customers_count: int
    appointments_count: int
    tier: str


class BillingHistoryItem(BaseModel):
    date: str
    amount: float
    description: str
    status: str


@router.get("/", response_model=BusinessResponse)
async def get_profile(business: Business = Depends(get_current_business)):
    return BusinessResponse.model_validate(business)


@router.put("/", response_model=BusinessResponse)
async def update_profile(
    data: BusinessUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if data.name is not None:
        business.name = data.name
    if data.phone is not None:
        business.phone = data.phone
    if data.settings is not None:
        business.settings = data.settings
        attributes.flag_modified(business, "settings")
    await db.commit()
    await db.refresh(business)
    return BusinessResponse.model_validate(business)


@router.get("/features")
async def get_features(business: Business = Depends(get_current_business)):
    return {
        "tier": business.tier,
        "features": business.features,
        "limits": business.limits,
    }


@router.post("/upgrade")
async def upgrade_subscription(
    data: UpgradeRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    """Upgrade nécessite une vérification de paiement on-chain réelle."""
    valid_tiers = ["basic", "professional", "enterprise"]
    if data.tier not in valid_tiers:
        raise HTTPException(status_code=400, detail=f"Tier invalide. Choisissez: {valid_tiers}")

    # ARCH-09: Upgrade nécessite paiement vérifié
    # TODO: Appeler le vrai vérificateur Web3 on-chain
    raise HTTPException(
        status_code=501,
        detail="Paiement non intégré — contactez le support pour un upgrade",
    )


@router.get("/usage", response_model=UsageResponse)
async def get_usage(
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    calls_count = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id))
    customers_count = await db.execute(select(func.count(Customer.id)).where(Customer.business_id == business.id))
    appointments_count = await db.execute(select(func.count(Appointment.id)).where(Appointment.business_id == business.id))
    limits = business.limits or {}
    return UsageResponse(
        calls_used=calls_count.scalar(),
        calls_limit=limits.get("max_calls", 500),
        customers_count=customers_count.scalar(),
        appointments_count=appointments_count.scalar(),
        tier=business.tier,
    )


@router.get("/billing")
async def get_billing(business: Business = Depends(get_current_business)):
    return {
        "business_id": business.id,
        "tier": business.tier,
        "history": [
            BillingHistoryItem(date="2026-06-01", amount=500.0, description="Basic tier monthly", status="paid"),
        ],
    }
