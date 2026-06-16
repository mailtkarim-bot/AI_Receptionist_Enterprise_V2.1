from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[List[str]] = []
    preferences: Optional[Dict[str, Any]] = {}

class CustomerResponse(BaseModel):
    id: str
    business_id: str
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    tags: Optional[List[str]]
    preferences: Optional[Dict[str, Any]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
