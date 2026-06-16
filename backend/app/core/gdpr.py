"""GDPR compliance: consent, purge, erasure, breach notification."""

import logging
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func

from app.models.call import Call
from app.models.customer import Customer
from app.models.sms_message import SMSMessage

logger = logging.getLogger(__name__)
DEFAULT_RETENTION_DAYS = 90


@dataclass
class ConsentRecord:
    consent_id: str
    caller_phone_hash: str
    business_id: str
    timestamp: datetime
    channel: str
    purpose: str
    consent_given: bool


class ConsentLogger:
    def __init__(self):
        self._records: List[ConsentRecord] = []

    def log_consent(self, caller_phone: str, business_id: str, channel: str, purpose: str, consent_given: bool) -> str:
        consent_id = secrets.token_hex(32)
        phone_hash = hashlib.sha256(caller_phone.encode()).hexdigest()
        record = ConsentRecord(consent_id=consent_id, caller_phone_hash=phone_hash, business_id=business_id,
                               timestamp=datetime.now(timezone.utc), channel=channel, purpose=purpose, consent_given=consent_given)
        self._records.append(record)
        logger.info(f"Consent logged: id={consent_id}, business={business_id}, channel={channel}, given={consent_given}")
        return consent_id


consent_logger = ConsentLogger()


async def purge_expired_voice_data(db: AsyncSession, retention_days: int = DEFAULT_RETENTION_DAYS) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    result_calls = await db.execute(delete(Call).where(Call.created_at < cutoff))
    result_sms = await db.execute(delete(SMSMessage).where(SMSMessage.created_at < cutoff))
    await db.commit()
    logger.info(f"GDPR purge: {result_calls.rowcount} calls, {result_sms.rowcount} SMS deleted (>{retention_days} days)")
    return {"calls_deleted": result_calls.rowcount, "sms_deleted": result_sms.rowcount, "retention_days": retention_days}


async def erase_customer_data(db: AsyncSession, customer_id: str, business_id: str) -> dict:
    result_calls = await db.execute(delete(Call).where(Call.customer_id == customer_id, Call.business_id == business_id))
    result_sms = await db.execute(delete(SMSMessage).where(SMSMessage.customer_id == customer_id, SMSMessage.business_id == business_id))
    await db.execute(update(Customer).where(Customer.id == customer_id, Customer.business_id == business_id).values(
        phone=None, email=None, name="[DELETED]", preferences={}, tags=[], embedding=None, is_deleted=True, deleted_at=datetime.now(timezone.utc)))
    await db.commit()
    return {"customer_id": customer_id, "calls_deleted": result_calls.rowcount, "sms_deleted": result_sms.rowcount, "status": "erased"}


def hash_pii(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def mask_pii(value: str, visible_chars: int = 4) -> str:
    if len(value) <= visible_chars * 2:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars * 2) + value[-visible_chars:]


@dataclass
class BreachNotification:
    breach_id: str
    detected_at: datetime
    severity: str
    description: str


class BreachNotifier:
    def __init__(self):
        self._breaches: List[BreachNotification] = []

    def report_breach(self, severity: str, description: str) -> str:
        breach_id = secrets.token_hex(16)
        breach = BreachNotification(breach_id=breach_id, detected_at=datetime.now(timezone.utc), severity=severity, description=description)
        self._breaches.append(breach)
        logger.critical(f"GDPR BREACH: id={breach_id}, severity={severity}")
        return breach_id


breach_notifier = BreachNotifier()
