"""Application configuration — ZERO default secrets."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = Field(..., pattern=r"^postgresql\+asyncpg://")
    REDIS_URL: str = Field(default="redis://redis:6379/0")

    # Security — NO DEFAULTS
    JWT_SECRET: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=1, le=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=30)
    METRICS_API_KEY: str = Field(default="")

    # Debug
    DEBUG: bool = Field(default=False)

    # External APIs
    VAPI_API_KEY: str = Field(default="")
    VAPI_WEBHOOK_SECRET: str = Field(default="")
    TWILIO_ACCOUNT_SID: str = Field(default="")
    TWILIO_AUTH_TOKEN: str = Field(default="")
    TWILIO_PHONE_NUMBER: str = Field(default="")
    SENDGRID_API_KEY: str = Field(default="")
    SENDGRID_WEBHOOK_SECRET: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    WHATSAPP_ACCESS_TOKEN: str = Field(default="")
    WHATSAPP_APP_SECRET: str = Field(default="")

    # Web3
    WEB3_RPC_URL: str = Field(default="")
    USDC_CONTRACT_ADDRESS: str = Field(default="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
    PLATFORM_WALLET_ADDRESS: str = Field(default="")
    PLATFORM_PRIVATE_KEY: str = Field(default="")
    BLOCKCHAIN_NETWORK: str = Field(default="base")

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_not_default(cls, v: str) -> str:
        forbidden = {"change-me-in-production", "changeme", "secret", "default", ""}
        if v.lower() in forbidden:
            raise ValueError("JWT_SECRET cannot be a default/weak value.")
        return v

    @field_validator("USDC_CONTRACT_ADDRESS")
    @classmethod
    def validate_usdc_address(cls, v: str) -> str:
        if v and v.lower() != "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913":
            raise ValueError("Invalid USDC contract address for Base network.")
        return v

@lru_cache()
def get_settings() -> Settings:
    return Settings()
