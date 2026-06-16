from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CallCreate(BaseModel):
    customer_id: Optional[str] = None
    phone_number: str
    direction: str = "inbound"
    metadata: Optional[Dict[str, Any]] = None

class CallResponse(BaseModel):
    id: str
    business_id: str
    customer_id: Optional[str]
    direction: str
    status: str
    phone_number: Optional[str]
    duration: Optional[int]
    transcript: Optional[List]
    recording_url: Optional[str]
    notes: Optional[List]
    sentiment: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: Optional[datetime]
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True

class CallNoteCreate(BaseModel):
    note: str
