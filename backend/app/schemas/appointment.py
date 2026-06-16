from pydantic import BaseModel
from typing import Optional, Dict, Any
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
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    calendar_id: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    calendar_id: Optional[str] = None
    status: Optional[str] = None
