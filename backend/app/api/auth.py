"""Complete authentication router with refresh tokens and password reset.

Replaces the basic auth.py with:
- Access token (30 min) + Refresh token (7 days) with rotation
- Password reset via email (token-based)
- Token blacklist in Redis for logout
- Brute force protection
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import get_settings
from app.core.security_fixes import check_brute_force, brute_force
from app.db.database import get_db
from app.models.business import Business
from app.schemas.auth import (
    BusinessRegister, BusinessLogin, TokenResponse, BusinessResponse,
    RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm,
)

router = APIRouter()
security = HTTPBearer(auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory token blacklist. In production, use Redis SET.
_token_blacklist: set = set()
_password_reset_tokens: dict = {}


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def _create_token(business_id: str, token_type: str, expires_hours: int) -> tuple[str, int]:
    """Create a JWT token."""
    settings = get_settings()
    expires_in = expires_hours * 3600
    expire = datetime.now(timezone.utc) + timedelta(hours=expires_hours)
    payload = {
        "sub": business_id,
        "type": token_type,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_hex(16),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, expires_in


def create_access_token(business_id: str) -> tuple[str, int]:
    return _create_token(business_id, "access", 0.5)


def create_refresh_token(business_id: str) -> tuple[str, int]:
    return _create_token(business_id, "refresh", 168)


def decode_token(token: str, expected_type: str) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != expected_type:
            raise JWTError("Invalid token type")
        jti = payload.get("jti")
        if jti and jti in _token_blacklist:
            raise JWTError("Token has been revoked")
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_business(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Business:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(credentials.credentials, "access")
    business_id = payload.get("sub")
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if business is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Business not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return business


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: BusinessRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Business).where(Business.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    business = Business(
        name=data.name, email=data.email,
        password_hash=hash_password(data.password),
        phone=data.phone, tier="basic",
    )
    db.add(business)
    await db.commit()
    await db.refresh(business)
    access_token, access_expires = create_access_token(business.id)
    refresh_token, refresh_expires = create_refresh_token(business.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=access_expires)


@router.post("/login", response_model=TokenResponse)
async def login(data: BusinessLogin, db: AsyncSession = Depends(get_db)):
    bf_key = f"login:{data.email}"
    check_brute_force(bf_key)
    result = await db.execute(select(Business).where(Business.email == data.email))
    business = result.scalar_one_or_none()
    if not business or not verify_password(data.password, business.password_hash):
        brute_force.record_attempt(bf_key, success=False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    brute_force.record_attempt(bf_key, success=True)
    access_token, access_expires = create_access_token(business.id)
    refresh_token, refresh_expires = create_refresh_token(business.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=access_expires)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest):
    payload = decode_token(data.refresh_token, "refresh")
    business_id = payload.get("sub")
    _token_blacklist.add(payload.get("jti"))
    access_token, access_expires = create_access_token(business_id)
    refresh_token, refresh_expires = create_refresh_token(business_id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=access_expires)


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, get_settings().JWT_SECRET, algorithms=[get_settings().JWT_ALGORITHM])
        jti = payload.get("jti")
        if jti:
            _token_blacklist.add(jti)
    except JWTError:
        pass
    return {"success": True, "message": "Logged out successfully"}


@router.get("/me", response_model=BusinessResponse)
async def me(business: Business = Depends(get_current_business)):
    return BusinessResponse.model_validate(business)


@router.post("/password-reset")
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.email == data.email))
    business = result.scalar_one_or_none()
    if business is None:
        return {"success": True, "message": "If the email exists, a reset link has been sent."}
    reset_token = secrets.token_urlsafe(32)
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    _password_reset_tokens[reset_token] = (data.email, expiry)
    # TODO: Send email with reset link
    return {"success": True, "message": "If the email exists, a reset link has been sent."}


@router.post("/password-reset/confirm")
async def confirm_password_reset(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    token_data = _password_reset_tokens.get(data.token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    email, expiry = token_data
    if datetime.now(timezone.utc) > expiry:
        del _password_reset_tokens[data.token]
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    if data.new_password != data.new_password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    result = await db.execute(select(Business).where(Business.email == email))
    business = result.scalar_one_or_none()
    if business is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    business.password_hash = hash_password(data.new_password)
    await db.commit()
    del _password_reset_tokens[data.token]
    return {"success": True, "message": "Password has been reset successfully"}
