"""
Modèles GDPR persistés en base de données — Grade Production.

ARCH-06 corrigé : ConsentRecord et BreachLog ne sont PLUS en mémoire.
Ils sont maintenant des tables SQLAlchemy persistées.

Obligations légales :
- RGPD Art. 5(2)  : responsabilité — preuve de conformité
- RGPD Art. 30    : registre des activités de traitement
- RGPD Art. 33    : notification de violation dans les 72h
- RGPD Art. 7(1)  : preuve du consentement
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, String, DateTime, Boolean, Text
from app.db.database import Base


class ConsentRecord(Base):
    """
    Enregistrement de consentement RGPD — persisté, jamais supprimé.

    Chaque interaction avec un appelant génère un enregistrement
    de consentement horodaté et lié au business concerné.

    Règle d'or : cette table ne doit JAMAIS être purgée automatiquement.
    Elle constitue la preuve légale de conformité RGPD.
    """
    __tablename__ = "consent_records"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Hash SHA-256 du numéro de téléphone (PII non stockée en clair)
    # Note : utiliser un salt par business pour résister aux rainbow tables (EC-08)
    caller_phone_hash = Column(String(64), nullable=False, index=True)
    business_id = Column(String, nullable=False, index=True)
    channel = Column(String(50), nullable=False)   # 'voice', 'sms', 'whatsapp'
    purpose = Column(String(200), nullable=False)  # Ex: 'ai_call_recording'
    consent_given = Column(Boolean, nullable=False)
    ip_address_hash = Column(String(64), nullable=True)  # Hash de l'IP si disponible
    timestamp = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class BreachLog(Base):
    """
    Journal des violations de données RGPD (Art. 33).

    Chaque violation doit être documentée et notifiée à l'autorité
    de contrôle (CNIL/DPA) dans les 72 heures suivant la détection.

    Ce log constitue la preuve que l'obligation de notification a été respectée.
    """
    __tablename__ = "breach_logs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    severity = Column(
        String(20),
        nullable=False,
        index=True,
    )  # 'low', 'medium', 'high', 'critical'
    description = Column(Text, nullable=False)
    affected_business_ids = Column(Text, nullable=True)  # JSON array as text
    estimated_affected_records = Column(String, nullable=True)
    detected_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    notified_dpa_at = Column(DateTime, nullable=True)  # Date notification CNIL/DPA
    resolved_at = Column(DateTime, nullable=True)
    dpa_reference = Column(String(100), nullable=True)  # Numéro de dossier CNIL
