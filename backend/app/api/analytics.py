from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.business import Business
from app.models.call import Call
from app.models.customer import Customer
from app.models.appointment import Appointment
from app.models.campaign import Campaign
from app.services.tier_manager import get_current_business
from app.schemas.analytics import DashboardSummary, CallAnalytics, SentimentReport, RevenueAnalytics

router = APIRouter()

@router.get("/dashboard", response_model=DashboardSummary)
async def dashboard_summary(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    calls = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id))
    customers = await db.execute(select(func.count(Customer.id)).where(Customer.business_id == business.id))
    appointments = await db.execute(select(func.count(Appointment.id)).where(Appointment.business_id == business.id))
    campaigns = await db.execute(select(func.count(Campaign.id)).where(Campaign.business_id == business.id, Campaign.status == "active"))
    return DashboardSummary(total_calls=calls.scalar(), total_customers=customers.scalar(), total_appointments=appointments.scalar(), active_campaigns=campaigns.scalar(), revenue_usd=0.0)

@router.get("/calls", response_model=CallAnalytics)
async def call_analytics(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    total = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id))
    inbound = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id, Call.direction == "inbound"))
    outbound = await db.execute(select(func.count(Call.id)).where(Call.business_id == business.id, Call.direction == "outbound"))
    return CallAnalytics(total_calls=total.scalar(), inbound_calls=inbound.scalar(), outbound_calls=outbound.scalar(), avg_duration=0.0, success_rate=0.0)

@router.get("/trends")
async def usage_trends(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return {"business_id": business.id, "trends": []}

@router.get("/sentiment", response_model=SentimentReport)
async def sentiment_report(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return SentimentReport(positive=0, neutral=0, negative=0, avg_score=0.0)

@router.get("/revenue", response_model=RevenueAnalytics)
async def revenue_analytics(business: Business = Depends(get_current_business), db: AsyncSession = Depends(get_db)):
    return RevenueAnalytics(total_revenue=0.0, by_tier={}, by_month={})
