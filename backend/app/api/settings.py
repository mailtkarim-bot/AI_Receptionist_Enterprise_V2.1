"""Settings router avec validation Pydantic + anti-SSRF.

Corrections Némésis:
- Validation d'URL webhook (anti-SSRF)
- httpx async (ne bloque pas l'event loop)
- flag_modified pour mutations JSON
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, Set
from urllib.parse import urlparse

import httpx
from sqlalchemy.orm import attributes
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.tier_manager import get_current_business
from app.models.business import Business
from app.db.database import get_db

router = APIRouter()

_BLOCKED_HOSTS: Set[str] = {
    "localhost", "127.0.0.1", "0.0.0.0", "::1",
    "169.254.169.254",
    "metadata.google.internal",
    "db", "redis", "api", "frontend", "nginx",
}


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


def _validate_webhook_url(url: str) -> str:
    """Valide l'URL avant requête externe (anti-SSRF)."""
    try:
        parsed = urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="URL invalide")
    if parsed.scheme not in ("https", "http"):
        raise HTTPException(status_code=400, detail="Schéma non autorisé")
    if parsed.scheme == "http":
        raise HTTPException(status_code=400, detail="HTTP non autorisé. Utilisez HTTPS.")
    hostname = parsed.hostname or ""
    if hostname in _BLOCKED_HOSTS or hostname.endswith(".internal"):
        raise HTTPException(status_code=400, detail="URL interne non autorisée")
    return url


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
    business.settings["general"].update(data.model_dump(exclude_unset=True))
    attributes.flag_modified(business, "settings")
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
    business.settings["voice"].update(data.model_dump(exclude_unset=True))
    attributes.flag_modified(business, "settings")
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
    business.settings["calendar"].update(data.model_dump(exclude_unset=True))
    attributes.flag_modified(business, "settings")
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
    business.settings["notifications"].update(data.model_dump(exclude_unset=True))
    attributes.flag_modified(business, "settings")
    await db.commit()
    return {"success": True, "notifications": business.settings["notifications"]}


@router.post("/test-webhook")
async def test_webhook(business: Business = Depends(get_current_business)):
    webhook_url = business.settings.get("notifications", {}).get("webhook_url")
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
