"""Application configuration with environment validation."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/ai_receptionist"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    VAPI_API_KEY: str = ""
    VAPI_WEBHOOK_SECRET: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    SENDGRID_API_KEY: str = ""
    SENDGRID_WEBHOOK_SECRET: str = ""
    OPENAI_API_KEY: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_APP_SECRET: str = ""
    WEB3_RPC_URL: str = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY"
    USDC_CONTRACT_ADDRESS: str = "0xA0b86a33E6441e0A421e56E4773C3C1C0E0F47d0"
    PLATFORM_WALLET_ADDRESS: str = ""
    PLATFORM_PRIVATE_KEY: str = ""
    BLOCKCHAIN_NETWORK: str = "base"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
