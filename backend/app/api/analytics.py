"""Analytics router."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional

from app.db.database import get_db
from app.models.call import Call
from app.models.customer import Customer
from app.models.appointment import Appointment
from app.models.campaign import Campaign
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.schemas.analytics import DashboardSummary

router = APIRouter()


@router.get("/dashboard")
async def dashboard(
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    calls = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id))
    customers = await db.execute(select(func.count(Customer.id)).where(Customer.business_id == business.id))
    appointments = await db.execute(select(func.count(Appointment.id)).where(Appointment.business_id == business.id))
    campaigns = await db.execute(select(func.count(Campaign.id)).where(Campaign.business_id == business.id, Campaign.status == "active"))
    return DashboardSummary(
        total_calls=calls.scalar(),
        total_customers=customers.scalar(),
        total_appointments=appointments.scalar(),
        active_campaigns=campaigns.scalar(),
    )


@router.get("/calls")
async def call_analytics(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return {"business_id": business.id, "metrics": []}


@router.get("/trends")
async def trends(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return {"business_id": business.id, "trends": []}


@router.get("/sentiment")
async def sentiment(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return {"business_id": business.id, "sentiment": []}


@router.get("/revenue")
async def revenue(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return {"business_id": business.id, "revenue": []}
