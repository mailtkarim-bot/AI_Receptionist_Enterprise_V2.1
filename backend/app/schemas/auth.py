from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class BusinessRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=12, max_length=128)
    phone: Optional[str] = None

class BusinessLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

class BusinessResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    tier: str
    features: list
    limits: dict
    is_active: bool

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=12, max_length=128)
    new_password_confirm: str
