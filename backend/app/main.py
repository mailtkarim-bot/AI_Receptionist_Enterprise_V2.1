"""AI Receptionist Enterprise — Hardened FastAPI Entry Point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.security_fixes import (
    RedisRateLimitMiddleware, RequestIDMiddleware, get_cors_middleware
)
from app.core.monitoring import MetricsMiddleware, health_check, metrics_endpoint
from app.db.database import engine

from app.api.auth import router as auth_router
from app.api.business import router as business_router
from app.api.calls import router as calls_router
from app.api.customers import router as customers_router
from app.api.appointments import router as appointments_router
from app.api.analytics import router as analytics_router
from app.api.outbound import router as outbound_router
from app.api.web3 import router as web3_router
from app.api.webhooks import router as webhooks_router
from app.api.settings import router as settings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ AI Receptionist Enterprise API started")
    yield
    await engine.dispose()
    print("🛑 AI Receptionist Enterprise API stopped")

settings = get_settings()
app = FastAPI(
    title="AI Receptionist Enterprise API",
    description="Multi-Channel AI Voice Agent with Web3 Payments — 3-Tier SaaS",
    version="2.1.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs" if settings.DEBUG else None,
    redoc_url="/api/v1/redoc" if settings.DEBUG else None,
    openapi_url="/api/v1/openapi.json" if settings.DEBUG else None,
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.aireceptionist.example.com", "localhost"] if settings.DEBUG else ["*.aireceptionist.example.com"])
app.add_middleware(RedisRateLimitMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(MetricsMiddleware)

cors_config = get_cors_middleware()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config["allow_origins"],
    allow_credentials=cors_config["allow_credentials"],
    allow_methods=cors_config["allow_methods"],
    allow_headers=cors_config["allow_headers"],
    expose_headers=cors_config.get("expose_headers", []),
    max_age=cors_config.get("max_age", 600),
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    logger = logging.getLogger(__name__)
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unhandled exception [req_id={request_id}]: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request_id},
    )

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(business_router, prefix="/api/v1/business", tags=["Business Management"])
app.include_router(calls_router, prefix="/api/v1/calls", tags=["Calls"])
app.include_router(customers_router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(appointments_router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(outbound_router, prefix="/api/v1/campaigns", tags=["Outbound Campaigns"])
app.include_router(web3_router, prefix="/api/v1/payments", tags=["Web3 Payments"])
app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(settings_router, prefix="/api/v1/settings", tags=["Settings"])

app.add_api_route("/api/v1/metrics", metrics_endpoint, methods=["GET"], tags=["Monitoring"], include_in_schema=False)
app.add_api_route("/api/v1/health", health_check, methods=["GET"], tags=["Health"])

@app.get("/")
async def root():
    return {"name": "AI Receptionist Enterprise API", "version": "2.1.0", "status": "operational"}
