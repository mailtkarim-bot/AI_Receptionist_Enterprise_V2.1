"""Business management router with Pydantic validation.

Endpoints:
- GET / → profile
- PUT / → update profile (validated schema)
- GET /features → enabled features
- POST /upgrade → subscription upgrade
- GET /usage → usage statistics
- GET /billing → billing history
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.models.business import Business
from app.models.call import Call
from app.models.customer import Customer
from app.models.appointment import Appointment
from app.services.tier_manager import get_current_business
from app.schemas.auth import BusinessResponse, BusinessUpdate
from pydantic import BaseModel

router = APIRouter()


class UpgradeRequest(BaseModel):
    tier: str  # basic, professional, enterprise


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
    valid_tiers = ["basic", "professional", "enterprise"]
    if data.tier not in valid_tiers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid tier. Choose from: {valid_tiers}")
    business.tier = data.tier
    # Update features and limits based on tier
    tier_features = {
        "basic": ["voice", "sms", "scheduling"],
        "professional": ["voice", "sms", "whatsapp", "scheduling", "emergency", "memory", "sentiment", "campaigns", "spam"],
        "enterprise": ["voice", "sms", "whatsapp", "email", "scheduling", "emergency", "memory", "sentiment", "campaigns", "spam", "web3", "voice_cloning", "nft_receipts"],
    }
    tier_limits = {
        "basic": {"max_calls": 500, "max_calendars": 1},
        "professional": {"max_calls": 2000, "max_calendars": 3},
        "enterprise": {"max_calls": 10000, "max_calendars": 10},
    }
    business.features = tier_features.get(data.tier, [])
    business.limits = tier_limits.get(data.tier, {})
    await db.commit()
    await db.refresh(business)
    return {"success": True, "tier": business.tier, "features": business.features}


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
    # TODO: Integrate with Stripe/PayPal for real billing history
    return {
        "business_id": business.id,
        "tier": business.tier,
        "history": [
            BillingHistoryItem(date="2026-06-01", amount=500.0, description="Basic tier monthly", status="paid"),
        ],
    }
