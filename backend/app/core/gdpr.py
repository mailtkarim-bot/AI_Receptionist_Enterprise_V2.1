"""GDPR compliance — persistance DB, hash avec salt, breach logging."""

import logging
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func

from app.models.call import Call
from app.models.customer import Customer
from app.models.sms_message import SMSMessage
from app.models.consent_record import ConsentRecord
from app.models.breach_log import BreachLog

logger = logging.getLogger(__name__)
DEFAULT_RETENTION_DAYS = 90
GDPR_SALT = secrets.token_hex(16)  # Généré au démarrage, idéalement via env var


async def log_consent(db: AsyncSession, caller_phone: str, business_id: str, channel: str, purpose: str, consent_given: bool) -> str:
    """Log de consentement persistant en base (GDPR Art. 7)."""
    consent_id = secrets.token_hex(32)
    phone_hash = hashlib.sha256((caller_phone + GDPR_SALT).encode()).hexdigest()
    record = ConsentRecord(
        id=consent_id,
        caller_phone_hash=phone_hash,
        business_id=business_id,
        channel=channel,
        purpose=purpose,
        consent_given=consent_given,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(record)
    await db.commit()
    logger.info(f"Consent logged: id={consent_id}, business={business_id}, channel={channel}, given={consent_given}")
    return consent_id


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
    return hashlib.sha256((value + GDPR_SALT).encode()).hexdigest()


def mask_pii(value: str, visible_chars: int = 4) -> str:
    if len(value) <= visible_chars * 2:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars * 2) + value[-visible_chars:]


async def report_breach(db: AsyncSession, severity: str, description: str) -> str:
    """Log de breach GDPR persistant (Art. 33)."""
    breach_id = secrets.token_hex(16)
    breach = BreachLog(
        id=breach_id,
        severity=severity,
        description=description,
        detected_at=datetime.now(timezone.utc),
    )
    db.add(breach)
    await db.commit()
    logger.critical(f"GDPR BREACH: id={breach_id}, severity={severity}")
    return breach_id
