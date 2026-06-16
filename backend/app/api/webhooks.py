"""Complete webhook router with HMAC-SHA256 verification.

Handles: Vapi, Twilio SMS, Twilio Voice, WhatsApp, SendGrid
"""

import hmac
import hashlib
import time
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel

from app.core.config import get_settings

router = APIRouter()


def verify_hmac_signature(payload: bytes, signature: str, secret: str, max_age_seconds: int = 300, timestamp_header: Optional[str] = None) -> bool:
    if not signature or not secret:
        return False
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return False
    if timestamp_header:
        try:
            timestamp = int(timestamp_header)
            if abs(int(time.time()) - timestamp) > max_age_seconds:
                return False
        except (ValueError, TypeError):
            return False
    return True


def extract_signature(headers: dict, header_name: str) -> Optional[str]:
    sig = headers.get(header_name, "")
    if sig.startswith("sha256="):
        sig = sig[7:]
    elif sig.startswith("v0="):
        sig = sig[3:]
    return sig if sig else None


class VapiWebhookPayload(BaseModel):
    event: str
    call_id: Optional[str] = None
    assistant_id: Optional[str] = None
    customer_phone: Optional[str] = None
    status: Optional[str] = None
    duration_seconds: Optional[int] = None
    recording_url: Optional[str] = None
    transcript: Optional[list] = None


@router.post("/vapi")
async def vapi_webhook(request: Request):
    settings = get_settings()
    body = await request.body()
    signature = extract_signature(dict(request.headers), "X-Vapi-Signature")
    if not verify_hmac_signature(body, signature, settings.VAPI_WEBHOOK_SECRET, timestamp_header=request.headers.get("X-Vapi-Timestamp")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook signature")
    payload = await request.json()
    return {"success": True, "event": payload.get("event"), "call_id": payload.get("call_id")}


@router.post("/twilio/sms")
async def twilio_sms_webhook(request: Request):
    settings = get_settings()
    body = await request.body()
    signature = extract_signature(dict(request.headers), "X-Twilio-Signature")
    if not verify_hmac_signature(body, signature, settings.TWILIO_AUTH_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Twilio signature")
    form = await request.form()
    return {"success": True, "message_sid": form.get("MessageSid")}


@router.post("/twilio/voice")
async def twilio_voice_webhook(request: Request):
    settings = get_settings()
    body = await request.body()
    signature = extract_signature(dict(request.headers), "X-Twilio-Signature")
    if not verify_hmac_signature(body, signature, settings.TWILIO_AUTH_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Twilio signature")
    form = await request.form()
    return {"success": True, "call_sid": form.get("CallSid")}


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    settings = get_settings()
    body = await request.body()
    signature = extract_signature(dict(request.headers), "X-Hub-Signature-256")
    app_secret = settings.WHATSAPP_APP_SECRET or settings.WHATSAPP_ACCESS_TOKEN
    if not verify_hmac_signature(body, signature, app_secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid WhatsApp signature")
    return {"success": True}


@router.post("/sendgrid")
async def sendgrid_webhook(request: Request):
    settings = get_settings()
    body = await request.body()
    signature = extract_signature(dict(request.headers), "X-Twilio-Email-Event-Webhook-Signature")
    secret = settings.SENDGRID_WEBHOOK_SECRET or settings.SENDGRID_API_KEY
    if not verify_hmac_signature(body, signature, secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid SendGrid signature")
    return {"success": True}
