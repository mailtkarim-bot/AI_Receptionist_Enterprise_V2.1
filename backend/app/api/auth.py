"""Authentication router — Grade Production.

Corrections Némésis:
- Blacklist JWT dans Redis (cross-instance, cross-worker)
- Reset tokens Redis avec GETDEL atomique
- Email envoyé via SendGrid (httpx async)
- Brute force Redis-backed
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import get_settings
from app.core.token_store import (
    blacklist_jti, is_jti_blacklisted,
    store_reset_token, consume_reset_token,
)
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


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def _create_token(business_id: str, token_type: str, expires_seconds: int) -> tuple[str, int]:
    """Crée un JWT signé avec JTI unique pour révocation."""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_seconds)
    payload = {
        "sub": str(business_id),
        "type": token_type,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_hex(32),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, expires_seconds


def create_access_token(business_id: str) -> tuple[str, int]:
    return _create_token(business_id, "access", 30 * 60)


def create_refresh_token(business_id: str) -> tuple[str, int]:
    return _create_token(business_id, "refresh", 7 * 24 * 3600)


async def decode_and_validate_token(token: str, expected_type: str) -> dict:
    """Décode le JWT et vérifie la blacklist Redis."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "jti", "sub", "type"]},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Type de token incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = payload.get("jti")
    if not jti or await is_jti_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token révoqué",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_current_business(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Business:
    """Dépendance unique pour toutes les routes — vérifie blacklist Redis."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = await decode_and_validate_token(credentials.credentials, "access")
    business_id = payload["sub"]

    result = await db.execute(
        select(Business).where(
            Business.id == business_id,
            Business.is_active == True,
        )
    )
    business = result.scalar_one_or_none()
    if business is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Compte introuvable ou suspendu",
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
        phone=data.phone, tier="basic", is_active=True,
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
    await check_brute_force(bf_key)
    result = await db.execute(select(Business).where(Business.email == data.email))
    business = result.scalar_one_or_none()
    if not business or not verify_password(data.password, business.password_hash):
        await brute_force.record_attempt(bf_key, success=False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    await brute_force.record_attempt(bf_key, success=True)
    access_token, access_expires = create_access_token(business.id)
    refresh_token, refresh_expires = create_refresh_token(business.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=access_expires)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest):
    payload = await decode_and_validate_token(data.refresh_token, "refresh")
    business_id = payload["sub"]
    old_jti = payload["jti"]
    old_exp = payload["exp"]
    ttl = max(int(old_exp - datetime.now(timezone.utc).timestamp()), 0)
    await blacklist_jti(old_jti, ttl)
    access_token, access_expires = create_access_token(business_id)
    new_refresh_token, _ = create_refresh_token(business_id)
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token, expires_in=access_expires)


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Révocation Redis du JTI — effective sur toutes les instances."""
    try:
        settings = get_settings()
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            ttl = max(int(exp - datetime.now(timezone.utc).timestamp()), 0)
            await blacklist_jti(jti, ttl)
    except JWTError:
        pass
    return {"success": True, "message": "Déconnecté avec succès"}


@router.get("/me", response_model=BusinessResponse)
async def me(business: Business = Depends(get_current_business)):
    return BusinessResponse.model_validate(business)


@router.post("/password-reset")
async def request_password_reset(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(select(Business).where(Business.email == data.email))
    business = result.scalar_one_or_none()
    if business:
        reset_token = secrets.token_urlsafe(32)
        await store_reset_token(reset_token, data.email, ttl_seconds=3600)
        background_tasks.add_task(_send_reset_email, data.email, reset_token)
    return {"success": True, "message": "Si l'email existe, un lien a été envoyé."}


async def _send_reset_email(email: str, token: str) -> None:
    """Envoi de l'email de reset via SendGrid (httpx async)."""
    settings = get_settings()
    import httpx
    reset_url = f"https://app.aireceptionist.example.com/reset-password?token={token}"
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"},
            json={
                "personalizations": [{"to": [{"email": email}]}],
                "from": {"email": "noreply@aireceptionist.example.com"},
                "subject": "Réinitialisation de votre mot de passe",
                "content": [{"type": "text/plain", "value": f"Lien : {reset_url}"}],
            },
            timeout=10.0,
        )


@router.post("/password-reset/confirm")
async def confirm_password_reset(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    email = await consume_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token invalide ou expiré")
    if data.new_password != data.new_password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Les mots de passe ne correspondent pas")
    result = await db.execute(select(Business).where(Business.email == email))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Compte introuvable")
    business.password_hash = hash_password(data.new_password)
    await db.commit()
    return {"success": True, "message": "Mot de passe réinitialisé avec succès"}
