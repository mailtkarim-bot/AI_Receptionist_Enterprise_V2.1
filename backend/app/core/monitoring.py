"""Monitoring & observability with Prometheus metrics."""

import time
import logging
from typing import Callable
from functools import wraps
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

logger = logging.getLogger(__name__)

if PROMETHEUS_AVAILABLE:
    REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status_code"])
    REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"], buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0])
    ACTIVE_CALLS = Gauge("active_calls", "Active calls", ["business_id"])
    CALLS_TOTAL = Counter("calls_total", "Total calls", ["direction", "status", "business_id"])
    SMS_TOTAL = Counter("sms_total", "Total SMS", ["direction", "business_id"])
    ERROR_COUNT = Counter("errors_total", "Total errors", ["error_type", "endpoint"])
    WEBHOOK_COUNT = Counter("webhooks_total", "Total webhooks", ["source", "status"])
    DB_CONNECTIONS = Gauge("db_connections_active", "Active DB connections")
    TIER_USAGE = Gauge("tier_usage_percentage", "Tier usage %", ["business_id", "metric"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            logger.error(f"Unhandled exception: {e}")
            raise
        finally:
            duration = time.time() - start_time
            endpoint = request.url.path
            method = request.method
            if PROMETHEUS_AVAILABLE:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
                if status_code >= 500:
                    ERROR_COUNT.labels(error_type="server_error", endpoint=endpoint).inc()
                elif status_code == 429:
                    ERROR_COUNT.labels(error_type="rate_limited", endpoint=endpoint).inc()
        return response


async def metrics_endpoint():
    if not PROMETHEUS_AVAILABLE:
        return {"error": "Prometheus client not installed"}
    from fastapi import Response
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


async def health_check() -> dict:
    return {"status": "healthy", "timestamp": time.time(), "version": "2.0.0", "checks": {"api": "ok"}}


def track_call(direction: str, business_id: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if PROMETHEUS_AVAILABLE:
                CALLS_TOTAL.labels(direction=direction, status="initiated", business_id=business_id).inc()
            return await func(*args, **kwargs)
        return wrapper
    return decorator
