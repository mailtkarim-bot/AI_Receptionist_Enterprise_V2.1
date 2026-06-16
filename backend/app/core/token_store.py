"""Token store Redis pour blacklist JWT cross-instance et cross-worker."""

import redis.asyncio as aioredis
from app.core.config import get_settings

_redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


async def blacklist_jti(jti: str, ttl_seconds: int) -> None:
    """Ajoute le JTI à la blacklist avec TTL = durée de vie restante du token."""
    r = await get_redis()
    await r.setex(f"blacklist:jti:{jti}", ttl_seconds, "1")


async def is_jti_blacklisted(jti: str) -> bool:
    """Retourne True si le JTI est révoqué."""
    r = await get_redis()
    return await r.exists(f"blacklist:jti:{jti}") == 1


async def store_reset_token(token: str, email: str, ttl_seconds: int = 3600) -> None:
    """Stocke le token de reset en Redis avec TTL de 1h."""
    r = await get_redis()
    await r.setex(f"pwreset:{token}", ttl_seconds, email)


async def consume_reset_token(token: str) -> str | None:
    """Récupère et supprime atomiquement le token (one-time use)."""
    r = await get_redis()
    return await r.getdel(f"pwreset:{token}")


async def rate_limit_check(key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
    """Rate limiting Redis sliding window. Retourne (is_blocked, retry_after)."""
    r = await get_redis()
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window_seconds)
    results = await pipe.execute()
    count = results[0]
    if count > limit:
        ttl = await r.ttl(key)
        return True, max(ttl, 0)
    return False, 0
