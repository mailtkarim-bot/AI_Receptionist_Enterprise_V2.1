"""Security hardening: rate limiting, CORS, JWT validation, brute force."""

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


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self._requests: dict = {}
        self._blocked: dict = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        now = time.time()
        if client_ip in self._blocked and now < self._blocked[client_ip]:
            raise HTTPException(status_code=429, detail="Too many requests.", headers={"Retry-After": str(int(self._blocked[client_ip] - now))})
        if client_ip not in self._requests:
            self._requests[client_ip] = []
        self._requests[client_ip] = [(t, p) for t, p in self._requests[client_ip] if now - t < 60]
        self._requests[client_ip].append((now, path))
        if path.startswith("/api/v1/auth/") and path not in ["/api/v1/auth/me"]:
            auth_reqs = [r for r in self._requests[client_ip] if r[1].startswith("/api/v1/auth/")]
            if len(auth_reqs) > 5:
                self._blocked[client_ip] = now + 300
                raise HTTPException(status_code=429, detail="Too many auth attempts. Blocked 5min.", headers={"Retry-After": "300"})
        recent = [r for r in self._requests[client_ip] if now - r[0] < 1]
        if len(recent) > 50:
            self._blocked[client_ip] = now + 60
            raise HTTPException(status_code=429, detail="Rate limit: 50 req/s.", headers={"Retry-After": "60"})
        return await call_next(request)


def get_cors_middleware() -> dict:
    settings = get_settings()
    if settings.DEBUG:
        return {"allow_origins": ["*"], "allow_credentials": True, "allow_methods": ["*"], "allow_headers": ["*"]}
    return {
        "allow_origins": ["https://app.aireceptionist.example.com", "https://admin.aireceptionist.example.com"],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type", "X-Request-ID", "X-Client-Version"],
        "expose_headers": ["X-Request-ID", "X-RateLimit-Remaining"],
        "max_age": 86400,
    }


def validate_jwt_secret() -> None:
    settings = get_settings()
    DEFAULTS = ["change-me-in-production", "changeme", "secret", "default", ""]
    if not settings.DEBUG and settings.JWT_SECRET in DEFAULTS:
        raise RuntimeError("CRITICAL: JWT_SECRET is default in production.")
    if len(settings.JWT_SECRET) < 32:
        raise RuntimeError("CRITICAL: JWT_SECRET must be >= 32 chars.")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", secrets.token_hex(16))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


class BruteForceProtection:
    def __init__(self):
        self._attempts: dict = {}

    def record_attempt(self, key: str, success: bool) -> None:
        now = time.time()
        if key not in self._attempts:
            self._attempts[key] = []
        self._attempts[key].append((now, success))
        self._attempts[key] = [(t, s) for t, s in self._attempts[key] if now - t < 900]

    def is_blocked(self, key: str) -> tuple[bool, int]:
        now = time.time()
        if key not in self._attempts:
            return False, 0
        recent = [s for t, s in self._attempts[key] if now - t < 900]
        failed = sum(1 for s in recent if not s)
        if failed >= 10:
            return True, 900
        if failed >= 5:
            return True, 300
        return False, 0


brute_force = BruteForceProtection()


def check_brute_force(key: str) -> None:
    blocked, retry_after = brute_force.is_blocked(key)
    if blocked:
        raise HTTPException(status_code=429, detail=f"Too many failed attempts. Retry in {retry_after}s.", headers={"Retry-After": str(retry_after)})
