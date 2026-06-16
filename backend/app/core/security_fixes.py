"""Security hardening: Redis-backed rate limiting, CORS, JWT validation, brute force.

Corrections Némésis:
- Rate limiter Redis sliding window (cross-instance, cross-worker)
- Brute force Redis-backed
- CORS restrictif en production
- JWT secret validation (no default in production)
"""

import time
import hmac
import hashlib
import secrets
from typing import Optional, Callable
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.config import get_settings
from app.core.token_store import rate_limit_check


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware de rate limiting Redis-backed (cross-instance)."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # Rate limit auth endpoints: 5 req/min par IP
        if path.startswith("/api/v1/auth/") and path not in ["/api/v1/auth/me"]:
            blocked, retry_after = await rate_limit_check(
                f"ratelimit:auth:{client_ip}", limit=5, window_seconds=60
            )
            if blocked:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many authentication attempts.",
                    headers={"Retry-After": str(retry_after)},
                )

        # General API: 50 req/s par IP
        blocked, retry_after = await rate_limit_check(
            f"ratelimit:general:{client_ip}", limit=50, window_seconds=1
        )
        if blocked:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: 50 requests per second.",
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)


class BruteForceProtection:
    """Brute force protection Redis-backed (cross-instance)."""

    async def record_attempt(self, key: str, success: bool) -> None:
        """Record a login attempt in Redis."""
        from app.core.token_store import get_redis
        r = await get_redis()
        now = time.time()
        await r.zadd(f"brute:{key}", {str(now): now})
        # Clean old entries (> 15 minutes)
        cutoff = now - 900
        await r.zremrangebyscore(f"brute:{key}", 0, cutoff)

    async def is_blocked(self, key: str) -> tuple[bool, int]:
        """Check if key is blocked. Returns (blocked, retry_after_seconds)."""
        from app.core.token_store import get_redis
        r = await get_redis()
        now = time.time()
        cutoff = now - 900
        # Count failed attempts in last 15 minutes
        failed_count = await r.zcount(f"brute:{key}", cutoff, now)
        if failed_count >= 10:
            return True, 900
        if failed_count >= 5:
            return True, 300
        return False, 0


brute_force = BruteForceProtection()


async def check_brute_force(key: str) -> None:
    """Raise HTTPException if key is blocked due to brute force."""
    blocked, retry_after = await brute_force.is_blocked(key)
    if blocked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed attempts. Retry in {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )


def get_cors_middleware() -> dict:
    """Return CORS configuration based on environment."""
    settings = get_settings()
    if settings.DEBUG:
        return {
            "allow_origins": ["*"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    return {
        "allow_origins": [
            "https://app.aireceptionist.example.com",
            "https://admin.aireceptionist.example.com",
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "X-Client-Version",
        ],
        "expose_headers": ["X-Request-ID", "X-RateLimit-Remaining"],
        "max_age": 86400,
    }


def validate_jwt_secret() -> None:
    """Ensure JWT secret is not the default value in production."""
    settings = get_settings()
    DEFAULT_SECRETS = [
        "change-me-in-production",
        "changeme",
        "secret",
        "default",
        "",
    ]
    if not settings.DEBUG and settings.JWT_SECRET in DEFAULT_SECRETS:
        raise RuntimeError(
            "CRITICAL SECURITY ERROR: JWT_SECRET is using a default value in production."
        )
    if len(settings.JWT_SECRET) < 32:
        raise RuntimeError(
            "CRITICAL SECURITY ERROR: JWT_SECRET must be at least 32 characters long."
        )


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to every request for distributed tracing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", secrets.token_hex(16))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def get_request_id(request: Request) -> str:
    """Retrieve the request ID from the current request state."""
    return getattr(request.state, "request_id", "unknown")
