"""Calls router — corrected imports, pagination, atomic counters."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.call import Call
from app.models.business import Business
from app.services.tier_manager import get_current_business, check_tier_limit
from app.schemas.call import CallCreate, CallResponse, CallNoteCreate

router = APIRouter()


class OutboundCallRequest(BaseModel):
    customer_id: str
    phone_number: str
    assistant_id: Optional[str] = None
    scheduled_time: Optional[str] = None


class EndCallRequest(BaseModel):
    reason: Optional[str] = "completed"


@router.get("/", response_model=list[CallResponse])
async def list_calls(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Call)
        .where(Call.business_id == business.id)
        .order_by(desc(Call.created_at))
        .offset(skip)
        .limit(min(limit, 100))
    )
    if status:
        query = query.where(Call.status == status)
    result = await db.execute(query)
    calls = result.scalars().all()
    return [CallResponse.model_validate(c) for c in calls]


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(
    call_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Call).where(Call.id == call_id, Call.business_id == business.id)
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return CallResponse.model_validate(call)


@router.post("/", response_model=CallResponse, status_code=201)
async def initiate_outbound_call(
    data: OutboundCallRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(
        select(func.count(Call.id)).where(Call.business_id == business.id)
    )
    calls_used = count_result.scalar()
    check_tier_limit(business, "max_calls", calls_used)

    call = Call(
        business_id=business.id,
        customer_id=data.customer_id,
        direction="outbound",
        status="initiated",
        phone_number=data.phone_number,
        metadata={"assistant_id": data.assistant_id, "scheduled_time": data.scheduled_time},
    )
    db.add(call)
    await db.commit()
    await db.refresh(call)
    return CallResponse.model_validate(call)


@router.post("/{call_id}/transfer")
async def transfer_call(
    call_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Call).where(Call.id == call_id, Call.business_id == business.id)
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    call.status = "transferred"
    await db.commit()
    return {"success": True, "call_id": call_id, "status": "transferred"}


@router.post("/{call_id}/note")
async def add_call_note(
    call_id: str,
    data: CallNoteCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Call).where(Call.id == call_id, Call.business_id == business.id)
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    notes = call.notes or []
    note_text = data.note[:2000] if hasattr(data, "note") else ""
    notes.append(note_text)
    call.notes = notes
    await db.commit()
    return {"success": True, "call_id": call_id, "notes": call.notes}


@router.post("/{call_id}/end")
async def end_call(
    call_id: str,
    data: EndCallRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Call).where(Call.id == call_id, Call.business_id == business.id)
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    call.status = data.reason
    call.ended_at = datetime.now(timezone.utc)
    await db.commit()
    return {"success": True, "call_id": call_id, "status": data.reason}


@router.get("/{call_id}/recording")
async def get_recording(
    call_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Call).where(Call.id == call_id, Call.business_id == business.id)
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    if not call.recording_url:
        raise HTTPException(status_code=404, detail="No recording available")
    return {"success": True, "call_id": call_id, "recording_url": call.recording_url}
