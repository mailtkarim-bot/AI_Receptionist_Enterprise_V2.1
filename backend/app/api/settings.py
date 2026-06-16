"""Settings router — SSRF fix, flag_modified JSON."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel
from urllib.parse import urlparse
import httpx

from app.db.database import get_db
from app.models.business import Business
from app.services.tier_manager import get_current_business
from sqlalchemy.orm import attributes

router = APIRouter()

_BLOCKED_HOSTS = {
    "localhost", "127.0.0.1", "0.0.0.0", "::1",
    "169.254.169.254",
    "metadata.google.internal",
    "db", "redis", "api", "frontend", "nginx",
}


def _validate_webhook_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="URL invalide")
    if parsed.scheme not in ("https",):
        raise HTTPException(status_code=400, detail="HTTPS requis")
    hostname = parsed.hostname or ""
    if hostname in _BLOCKED_HOSTS or hostname.endswith(".internal") or hostname.endswith(".local"):
        raise HTTPException(status_code=400, detail="URL interne non autorisée")
    return url


class GeneralSettingsUpdate(BaseModel):
    timezone: Optional[str] = None
    language: Optional[str] = None


class VoiceSettingsUpdate(BaseModel):
    assistant_id: Optional[str] = None
    voice_id: Optional[str] = None


class CalendarSettingsUpdate(BaseModel):
    google_calendar_id: Optional[str] = None
    sync_enabled: Optional[bool] = None


class NotificationSettingsUpdate(BaseModel):
    webhook_url: Optional[str] = None
    email_alerts: Optional[bool] = None


@router.get("/")
async def get_settings_all(business: Business = Depends(get_current_business)):
    return business.settings or {}


@router.patch("/general")
async def update_general(
    data: GeneralSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    settings = business.settings or {}
    settings["general"] = {**(settings.get("general") or {}), **data.model_dump(exclude_unset=True)}
    business.settings = settings
    attributes.flag_modified(business, "settings")
    await db.commit()
    return {"success": True, "general": settings["general"]}


@router.patch("/voice")
async def update_voice(
    data: VoiceSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    settings = business.settings or {}
    settings["voice"] = {**(settings.get("voice") or {}), **data.model_dump(exclude_unset=True)}
    business.settings = settings
    attributes.flag_modified(business, "settings")
    await db.commit()
    return {"success": True, "voice": settings["voice"]}


@router.patch("/calendar")
async def update_calendar(
    data: CalendarSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    settings = business.settings or {}
    settings["calendar"] = {**(settings.get("calendar") or {}), **data.model_dump(exclude_unset=True)}
    business.settings = settings
    attributes.flag_modified(business, "settings")
    await db.commit()
    return {"success": True, "calendar": settings["calendar"]}


@router.patch("/notifications")
async def update_notifications(
    data: NotificationSettingsUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    settings = business.settings or {}
    settings["notifications"] = {**(settings.get("notifications") or {}), **data.model_dump(exclude_unset=True)}
    business.settings = settings
    attributes.flag_modified(business, "settings")
    await db.commit()
    return {"success": True, "notifications": settings["notifications"]}


@router.post("/test-webhook")
async def test_webhook(business: Business = Depends(get_current_business)):
    webhook_url = (business.settings or {}).get("notifications", {}).get("webhook_url")
    if not webhook_url:
        raise HTTPException(status_code=400, detail="Aucune URL webhook configurée")
    validated_url = _validate_webhook_url(webhook_url)
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(
                validated_url,
                json={"event": "test", "business_id": str(business.id)},
                headers={"Content-Type": "application/json"},
            )
            return {"success": True, "status_code": response.status_code}
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Webhook timeout (5s)")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"Erreur de connexion: {str(e)}")
