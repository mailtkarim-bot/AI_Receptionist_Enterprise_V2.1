from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class CustomerCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[List[str]] = None
    preferences: Optional[dict] = None

class CustomerResponse(BaseModel):
    id: str
    business_id: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[List[str]] = None
    preferences: Optional[dict] = None
    is_deleted: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SMSMessageResponse(BaseModel):
    id: str
    business_id: str
    customer_id: Optional[str] = None
    direction: str
    content: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
