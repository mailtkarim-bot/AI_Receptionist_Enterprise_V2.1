"""Security hardening — Redis-backed, cluster-safe."""

import time
import hmac
import hashlib
import secrets
from typing import Optional, Callable
from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.config import get_settings
from app.core.token_store import rate_limit_check


class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    """Cluster-safe rate limiting via Redis."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        now = int(time.time())

        # Global rate limit: 50 req/s per IP (window 1s)
        blocked, retry = await rate_limit_check(
            f"ratelimit:{client_ip}:{now}", limit=50, window_seconds=2
        )
        if blocked:
            raise HTTPException(
                status_code=429,
                detail="Rate limit: 50 req/s exceeded.",
                headers={"Retry-After": str(retry)},
            )

        # Auth endpoint rate limit: 5 req/min per IP
        if path.startswith("/api/v1/auth/") and path not in ["/api/v1/auth/me"]:
            blocked, retry = await rate_limit_check(
                f"auth_limit:{client_ip}", limit=5, window_seconds=60
            )
            if blocked:
                raise HTTPException(
                    status_code=429,
                    detail="Too many auth attempts. Blocked.",
                    headers={"Retry-After": str(retry)},
                )

        return await call_next(request)


class BruteForceProtection:
    """Redis-backed brute force protection."""

    async def record_attempt(self, key: str, success: bool) -> None:
        from app.core.token_store import get_redis
        r = await get_redis()
        now = int(time.time())
        await r.zadd(f"bf:{key}", {str(now): now})
        await r.expire(f"bf:{key}", 900)
        if success:
            await r.delete(f"bf:{key}")

    async def is_blocked(self, key: str) -> tuple[bool, int]:
        from app.core.token_store import get_redis
        r = await get_redis()
        now = int(time.time())
        await r.zremrangebyscore(f"bf:{key}", 0, now - 900)
        failed = await r.zcard(f"bf:{key}")
        if failed >= 10:
            return True, 900
        if failed >= 5:
            return True, 300
        return False, 0


async def check_brute_force(key: str) -> None:
    bf = BruteForceProtection()
    blocked, retry_after = await bf.is_blocked(key)
    if blocked:
        raise HTTPException(
            status_code=429,
            detail=f"Too many failed attempts. Retry in {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )


def get_cors_middleware() -> dict:
    settings = get_settings()
    if settings.DEBUG:
        return {
            "allow_origins": ["http://localhost:5173", "http://localhost:3000"],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type", "X-Request-ID"],
            "max_age": 600,
        }
    return {
        "allow_origins": [
            "https://app.aireceptionist.example.com",
            "https://admin.aireceptionist.example.com",
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type", "X-Request-ID", "X-Client-Version"],
        "expose_headers": ["X-Request-ID", "X-RateLimit-Remaining"],
        "max_age": 86400,
    }


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", secrets.token_hex(16))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")
