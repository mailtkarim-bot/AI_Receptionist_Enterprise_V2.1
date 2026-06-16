from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class CallCreate(BaseModel):
    customer_id: str
    phone_number: str
    direction: str = "outbound"

class CallResponse(BaseModel):
    id: str
    business_id: str
    customer_id: Optional[str] = None
    direction: str
    status: str
    phone_number: Optional[str] = None
    recording_url: Optional[str] = None
    notes: Optional[List[str]] = None
    metadata: Optional[dict] = None
    ended_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CallNoteCreate(BaseModel):
    note: str
