from pydantic import BaseModel
from typing import Optional

class DashboardSummary(BaseModel):
    total_calls: int
    total_customers: int
    total_appointments: int
    active_campaigns: int
