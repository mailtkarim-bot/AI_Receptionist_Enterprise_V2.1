"""Tier management and business authentication dependency."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import get_settings
from app.db.database import get_db
from app.models.business import Business

security = HTTPBearer(auto_error=False)

async def get_current_business(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Business:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(credentials.credentials, get_settings().JWT_SECRET, algorithms=[get_settings().JWT_ALGORITHM])
        business_id = payload.get("sub")
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}", headers={"WWW-Authenticate": "Bearer"})
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if business is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Business not found", headers={"WWW-Authenticate": "Bearer"})
    return business


def check_feature_access(business: Business, feature: str):
    if feature not in (business.features or []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Feature '{feature}' not available in your tier")


def check_tier_limit(business: Business, metric: str, current: int):
    limits = business.limits or {}
    max_val = limits.get(metric)
    if max_val is not None and current >= max_val:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Tier limit reached for {metric}: {max_val}")
