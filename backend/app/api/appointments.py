"""Appointments router with all endpoints.

Endpoints:
- GET / → list appointments
- GET /{id} → appointment details
- POST / → create appointment
- PATCH /{id} → update appointment
- DELETE /{id} → cancel appointment
- GET /calendar → calendar view
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel

from app.db.database import get_db
from app.models.appointment import Appointment
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate

router = APIRouter()


class CalendarViewRequest(BaseModel):
    start_date: str
    end_date: str
    calendar_id: Optional[str] = None


@router.get("/", response_model=list[AppointmentResponse])
async def list_appointments(
    status: Optional[str] = None,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    query = select(Appointment).where(Appointment.business_id == business.id).order_by(desc(Appointment.created_at))
    if status:
        query = query.where(Appointment.status == status)
    result = await db.execute(query)
    appointments = result.scalars().all()
    return [AppointmentResponse.model_validate(a) for a in appointments]


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return AppointmentResponse.model_validate(appointment)


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    data: AppointmentCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    # Check for conflicts
    conflict = await db.execute(
        select(Appointment).where(
            Appointment.business_id == business.id,
            Appointment.status != "cancelled",
            Appointment.start_time < data.end_time,
            Appointment.end_time > data.start_time,
        )
    )
    if conflict.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Time slot conflict")

    appointment = Appointment(
        business_id=business.id,
        customer_id=data.customer_id,
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        calendar_id=data.calendar_id,
        status="confirmed",
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return AppointmentResponse.model_validate(appointment)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)
    return AppointmentResponse.model_validate(appointment)


@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    appointment.status = "cancelled"
    await db.commit()
    return {"success": True, "appointment_id": appointment_id, "status": "cancelled"}


@router.get("/calendar")
async def get_calendar_view(
    start_date: str,
    end_date: str,
    calendar_id: Optional[str] = None,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    query = select(Appointment).where(
        Appointment.business_id == business.id,
        Appointment.status != "cancelled",
        Appointment.start_time >= start_date,
        Appointment.end_time <= end_date,
    )
    if calendar_id:
        query = query.where(Appointment.calendar_id == calendar_id)
    query = query.order_by(Appointment.start_time)
    result = await db.execute(query)
    appointments = result.scalars().all()

    # Group by day
    calendar = {}
    for appt in appointments:
        day = appt.start_time.strftime("%Y-%m-%d")
        if day not in calendar:
            calendar[day] = []
        calendar[day].append(AppointmentResponse.model_validate(appt))

    return {
        "business_id": business.id,
        "start_date": start_date,
        "end_date": end_date,
        "calendar": calendar,
    }
