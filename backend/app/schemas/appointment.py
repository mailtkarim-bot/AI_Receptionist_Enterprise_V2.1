from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentCreate(BaseModel):
    customer_id: str
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    calendar_id: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    business_id: str
    customer_id: str
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    calendar_id: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
