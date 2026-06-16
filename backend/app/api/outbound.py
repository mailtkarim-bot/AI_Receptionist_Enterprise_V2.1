"""Outbound campaigns router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.campaign import Campaign
from app.models.business import Business
from app.services.tier_manager import get_current_business

router = APIRouter()


class CampaignCreate(BaseModel):
    name: str
    type: str = Field(..., pattern=r"^(call|sms|email)$")
    target_count: int = 0


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


@router.get("/")
async def list_campaigns(
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.business_id == business.id).order_by(desc(Campaign.created_at))
    )
    return result.scalars().all()


@router.post("/", status_code=201)
async def create_campaign(
    data: CampaignCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    campaign = Campaign(
        business_id=business.id,
        name=data.name,
        type=data.type,
        status="draft",
        target_count=data.target_count,
    )
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.business_id == business.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/{campaign_id}/launch")
async def launch_campaign(
    campaign_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.business_id == business.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.status = "active"
    await db.commit()
    return {"success": True, "campaign_id": campaign_id, "status": "active"}


@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.business_id == business.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.status = "paused"
    await db.commit()
    return {"success": True, "campaign_id": campaign_id, "status": "paused"}


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.business_id == business.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    await db.delete(campaign)
    await db.commit()
    return {"success": True, "message": "Campaign deleted"}
