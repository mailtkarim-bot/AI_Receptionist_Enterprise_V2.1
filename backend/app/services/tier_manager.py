"""Tier management and business authentication dependency.

Corrections Némésis:
- Vérifie la blacklist Redis pour TOUTES les routes
- Bloque les comptes suspendus (is_active)
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import get_settings
from app.core.token_store import is_jti_blacklisted
from app.db.database import get_db
from app.models.business import Business

security = HTTPBearer(auto_error=False)


async def get_current_business(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Business:
    """Guard utilisé par toutes les routes — vérifie blacklist Redis + compte actif."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            credentials.credentials,
            get_settings().JWT_SECRET,
            algorithms=[get_settings().JWT_ALGORITHM],
            options={"require": ["exp", "iat", "jti", "sub", "type"]},
        )
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = payload.get("jti")
    if not jti or await is_jti_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token révoqué",
            headers={"WWW-Authenticate": "Bearer"},
        )

    business_id = payload["sub"]
    result = await db.execute(
        select(Business).where(Business.id == business_id, Business.is_active == True)
    )
    business = result.scalar_one_or_none()
    if business is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Compte introuvable ou suspendu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return business


def check_feature_access(business: Business, feature: str):
    if feature not in (business.features or []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Feature '{feature}' not available in your tier",
        )


def check_tier_limit(business: Business, metric: str, current: int):
    limits = business.limits or {}
    max_val = limits.get(metric)
    if max_val is not None and current >= max_val:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tier limit reached for {metric}: {max_val}",
        )
