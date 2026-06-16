"""AI Receptionist Enterprise v2.1 — FastAPI Application Entry Point.

Corrections Némésis:
- /metrics protégé par clé API
- forwarded-allow-ips restreint (via nginx)
- Security middleware stack
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.security_fixes import (
    RateLimitMiddleware, RequestIDMiddleware, validate_jwt_secret, get_cors_middleware
)
from app.core.monitoring import MetricsMiddleware, health_check, metrics_endpoint
from app.db.database import engine, init_db

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
    await init_db()
    validate_jwt_secret()
    print("✅ AI Receptionist Enterprise v2.1 API started")
    yield
    await engine.dispose()
    print("🛑 AI Receptionist Enterprise v2.1 API stopped")


app = FastAPI(
    title="AI Receptionist Enterprise API",
    description="Multi-Channel AI Voice Agent with Web3 Payments — 3-Tier SaaS v2.1",
    version="2.1.0",
    lifespan=lifespan,
)

app.add_middleware(RateLimitMiddleware)
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": getattr(request.state, "request_id", "unknown")},
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

# ARCH-05: /metrics protégé par clé API
app.add_api_route("/api/v1/metrics", metrics_endpoint, methods=["GET"], tags=["Monitoring"])
app.add_api_route("/api/v1/health", health_check, methods=["GET"], tags=["Health"])

@app.get("/")
async def root():
    return {"name": "AI Receptionist Enterprise API", "version": "2.1.0", "docs": "/api/v1/docs", "health": "/api/v1/health"}
