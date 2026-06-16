"""GDPR compliance avec persistance DB.

Corrections Némésis:
- ConsentRecord et BreachLog sont des modèles SQLAlchemy (persistants)
- Pas de stockage en mémoire
"""

import logging
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func

from app.models.call import Call
from app.models.customer import Customer
from app.models.sms_message import SMSMessage
from app.models.consent_record import ConsentRecord, BreachLog

logger = logging.getLogger(__name__)
DEFAULT_RETENTION_DAYS = 90


def hash_pii(value: str) -> str:
    """One-way hash PII avec salt (anti-rainbow table)."""
    salt = "aireceptionist_salt_2026"  # En production, utiliser un salt par business
    return hashlib.sha256((value + salt).encode()).hexdigest()


def mask_pii(value: str, visible_chars: int = 4) -> str:
    if len(value) <= visible_chars * 2:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars * 2) + value[-visible_chars:]


async def log_consent(
    db: AsyncSession,
    caller_phone: str,
    business_id: str,
    channel: str,
    purpose: str,
    consent_given: bool,
) -> str:
    """Log consent event en base (persistant, audit trail)."""
    record = ConsentRecord(
        caller_phone_hash=hash_pii(caller_phone),
        business_id=business_id,
        channel=channel,
        purpose=purpose,
        consent_given=consent_given,
    )
    db.add(record)
    await db.commit()
    logger.info(f"Consent logged: business={business_id}, channel={channel}, given={consent_given}")
    return record.id


async def purge_expired_voice_data(db: AsyncSession, retention_days: int = DEFAULT_RETENTION_DAYS) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    result_calls = await db.execute(delete(Call).where(Call.created_at < cutoff))
    result_sms = await db.execute(delete(SMSMessage).where(SMSMessage.created_at < cutoff))
    await db.commit()
    logger.info(f"GDPR purge: {result_calls.rowcount} calls, {result_sms.rowcount} SMS deleted")
    return {"calls_deleted": result_calls.rowcount, "sms_deleted": result_sms.rowcount}


async def erase_customer_data(db: AsyncSession, customer_id: str, business_id: str) -> dict:
    result_calls = await db.execute(delete(Call).where(Call.customer_id == customer_id, Call.business_id == business_id))
    result_sms = await db.execute(delete(SMSMessage).where(SMSMessage.customer_id == customer_id, SMSMessage.business_id == business_id))
    await db.execute(
        update(Customer).where(Customer.id == customer_id, Customer.business_id == business_id).values(
            phone=None, email=None, name="[DELETED]", preferences={}, tags=[], embedding=None,
            is_deleted=True, deleted_at=datetime.now(timezone.utc),
        )
    )
    await db.commit()
    return {"customer_id": customer_id, "calls_deleted": result_calls.rowcount, "sms_deleted": result_sms.rowcount, "status": "erased"}


async def report_breach(db: AsyncSession, severity: str, description: str) -> str:
    """Report breach GDPR (Art. 33) — persistance légale obligatoire."""
    log = BreachLog(severity=severity, description=description)
    db.add(log)
    await db.commit()
    logger.critical(f"GDPR BREACH: id={log.id}, severity={severity}")
    return log.id
