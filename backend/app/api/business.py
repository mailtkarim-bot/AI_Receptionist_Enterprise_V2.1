"""Business management — upgrade sécurisé, is_active."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.core.config import get_settings

router = APIRouter()


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class UpgradeRequest(BaseModel):
    tier: str


@router.get("/", response_model=dict)
async def get_business(business: Business = Depends(get_current_business)):
    return {
        "id": business.id,
        "name": business.name,
        "email": business.email,
        "phone": business.phone,
        "tier": business.tier,
        "features": business.features,
        "limits": business.limits,
        "is_active": business.is_active,
    }


@router.put("/", response_model=dict)
async def update_business(
    data: BusinessUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if data.name:
        business.name = data.name
    if data.phone:
        business.phone = data.phone
    await db.commit()
    await db.refresh(business)
    return {"success": True, "business": business}


@router.get("/features")
async def get_features(business: Business = Depends(get_current_business)):
    return {"tier": business.tier, "features": business.features or [], "limits": business.limits or {}}


@router.post("/upgrade")
async def upgrade_subscription(
    data: UpgradeRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    valid_tiers = ["basic", "professional", "enterprise"]
    if data.tier not in valid_tiers:
        raise HTTPException(status_code=400, detail=f"Tier invalide. Choix: {valid_tiers}")
    # TODO: Intégrer la vérification on-chain réelle avant activation
    raise HTTPException(
        status_code=501,
        detail="Paiement non intégré — contactez le support pour un upgrade",
    )


@router.get("/usage")
async def get_usage(business: Business = Depends(get_current_business)):
    return {"business_id": business.id, "tier": business.tier, "limits": business.limits or {}}


@router.get("/billing")
async def get_billing(business: Business = Depends(get_current_business)):
    return {"business_id": business.id, "invoices": [], "payments": []}
