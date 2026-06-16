"""Settings router with Pydantic validation.

Endpoints:
- GET / → all settings
- PATCH /general → general settings
- PATCH /voice → voice AI settings
- PATCH /calendar → calendar settings
- PATCH /notifications → notification settings
- POST /test-webhook → test webhook connectivity
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.tier_manager import get_current_business
from app.models.business import Business
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class GeneralSettingsUpdate(BaseModel):
    language: Optional[str] = None
    timezone: Optional[str] = None
    business_hours: Optional[Dict[str, Any]] = None


class VoiceSettingsUpdate(BaseModel):
    voice_id: Optional[str] = None
    greeting_message: Optional[str] = None
    fallback_message: Optional[str] = None
    max_call_duration: Optional[int] = None


class CalendarSettingsUpdate(BaseModel):
    default_calendar_id: Optional[str] = None
    buffer_minutes: Optional[int] = None
    working_hours: Optional[Dict[str, Any]] = None


class NotificationSettingsUpdate(BaseModel):
    email_alerts: Optional[bool] = None
    sms_alerts: Optional[bool] = None
    webhook_url: Optional[str] = None
    alert_events: Optional[list] = None


@router.get("/")
async def get_all_settings(business: Business = Depends(get_current_business)):
    return {
        "business_id": business.id,
        "general": business.settings.get("general", {}),
        "voice": business.settings.get("voice", {}),
        "calendar": business.settings.get("calendar", {}),
        "notifications": business.settings.get("notifications", {}),
    }


@router.patch("/general")
async def update_general_settings(
    data: GeneralSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if "general" not in business.settings:
        business.settings["general"] = {}
    update_data = data.model_dump(exclude_unset=True)
    business.settings["general"].update(update_data)
    await db.commit()
    return {"success": True, "general": business.settings["general"]}


@router.patch("/voice")
async def update_voice_settings(
    data: VoiceSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if "voice" not in business.settings:
        business.settings["voice"] = {}
    update_data = data.model_dump(exclude_unset=True)
    business.settings["voice"].update(update_data)
    await db.commit()
    return {"success": True, "voice": business.settings["voice"]}


@router.patch("/calendar")
async def update_calendar_settings(
    data: CalendarSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if "calendar" not in business.settings:
        business.settings["calendar"] = {}
    update_data = data.model_dump(exclude_unset=True)
    business.settings["calendar"].update(update_data)
    await db.commit()
    return {"success": True, "calendar": business.settings["calendar"]}


@router.patch("/notifications")
async def update_notification_settings(
    data: NotificationSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if "notifications" not in business.settings:
        business.settings["notifications"] = {}
    update_data = data.model_dump(exclude_unset=True)
    business.settings["notifications"].update(update_data)
    await db.commit()
    return {"success": True, "notifications": business.settings["notifications"]}


@router.post("/test-webhook")
async def test_webhook(
    business: Business = Depends(get_current_business),
):
    import requests
    webhook_url = business.settings.get("notifications", {}).get("webhook_url")
    if not webhook_url:
        raise HTTPException(status_code=400, detail="No webhook URL configured")
    try:
        response = requests.post(webhook_url, json={"event": "test", "business_id": business.id}, timeout=5)
        return {"success": True, "status_code": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook test failed: {str(e)}")
