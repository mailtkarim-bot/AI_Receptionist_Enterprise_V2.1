from pydantic import BaseModel
from typing import Optional, Dict, Any

class DashboardSummary(BaseModel):
    total_calls: int
    total_customers: int
    total_appointments: int
    active_campaigns: int
    revenue_usd: float

class CallAnalytics(BaseModel):
    total_calls: int
    inbound_calls: int
    outbound_calls: int
    avg_duration: float
    success_rate: float

class TrendData(BaseModel):
    date: str
    calls: int
    customers: int
    appointments: int

class SentimentReport(BaseModel):
    positive: int
    neutral: int
    negative: int
    avg_score: float

class RevenueAnalytics(BaseModel):
    total_revenue: float
    by_tier: Dict[str, float]
    by_month: Dict[str, float]
