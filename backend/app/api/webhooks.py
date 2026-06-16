"""Webhook router avec vérification de signature correcte par fournisseur."""

import base64
import hashlib
import hmac
import time
from urllib.parse import urlencode
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel
from app.core.config import get_settings

router = APIRouter()
MAX_WEBHOOK_AGE_SECONDS = 300


def _verify_twilio_signature(auth_token: str, url: str, post_params: dict, signature: str) -> bool:
    if not auth_token or not signature:
        return False
    signed_string = url
    for key in sorted(post_params.keys()):
        signed_string += key + post_params[key]
    mac = hmac.new(auth_token.encode("utf-8"), signed_string.encode("utf-8"), hashlib.sha1)
    expected = base64.b64encode(mac.digest()).decode("utf-8")
    return hmac.compare_digest(expected, signature)


def _verify_hmac_sha256(secret: str, payload: bytes, signature: str, timestamp: Optional[str] = None) -> bool:
    if not secret or not signature:
        return False
    if timestamp:
        try:
            ts = int(timestamp)
            if abs(int(time.time()) - ts) > MAX_WEBHOOK_AGE_SECONDS:
                return False
        except (ValueError, TypeError):
            return False
    sig = signature.removeprefix("sha256=").removeprefix("v0=")
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)


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
    if not settings.VAPI_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="VAPI_WEBHOOK_SECRET non configuré")
    body = await request.body()
    signature = request.headers.get("X-Vapi-Signature", "")
    timestamp = request.headers.get("X-Vapi-Timestamp")
    if not _verify_hmac_sha256(settings.VAPI_WEBHOOK_SECRET, body, signature, timestamp):
        raise HTTPException(status_code=401, detail="Signature Vapi invalide")
    payload = await request.json()
    return {"success": True, "event": payload.get("event"), "call_id": payload.get("call_id")}


@router.post("/twilio/sms")
async def twilio_sms_webhook(request: Request):
    settings = get_settings()
    if not settings.TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=503, detail="TWILIO_AUTH_TOKEN non configuré")
    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    form = await request.form()
    post_params = dict(form)
    if not _verify_twilio_signature(settings.TWILIO_AUTH_TOKEN, url, post_params, signature):
        raise HTTPException(status_code=401, detail="Signature Twilio invalide")
    return {"success": True, "message_sid": form.get("MessageSid")}


@router.post("/twilio/voice")
async def twilio_voice_webhook(request: Request):
    settings = get_settings()
    if not settings.TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=503, detail="TWILIO_AUTH_TOKEN non configuré")
    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    form = await request.form()
    post_params = dict(form)
    if not _verify_twilio_signature(settings.TWILIO_AUTH_TOKEN, url, post_params, signature):
        raise HTTPException(status_code=401, detail="Signature Twilio invalide")
    return {"success": True, "call_sid": form.get("CallSid")}


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    settings = get_settings()
    if not settings.WHATSAPP_APP_SECRET:
        raise HTTPException(status_code=503, detail="WHATSAPP_APP_SECRET non configuré")
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not _verify_hmac_sha256(settings.WHATSAPP_APP_SECRET, body, signature):
        raise HTTPException(status_code=401, detail="Signature WhatsApp invalide")
    return {"success": True}


@router.post("/sendgrid")
async def sendgrid_webhook(request: Request):
    settings = get_settings()
    if not settings.SENDGRID_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="SENDGRID_WEBHOOK_SECRET non configuré")
    body = await request.body()
    signature = request.headers.get("X-Twilio-Email-Event-Webhook-Signature", "")
    if not _verify_hmac_sha256(settings.SENDGRID_WEBHOOK_SECRET, body, signature):
        raise HTTPException(status_code=401, detail="Signature SendGrid invalide")
    return {"success": True}
