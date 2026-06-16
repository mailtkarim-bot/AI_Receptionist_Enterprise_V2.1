"""Appointments router — atomic booking, SELECT FOR UPDATE."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.appointment import Appointment
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter()


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None


@router.get("/", response_model=list[AppointmentResponse])
async def list_appointments(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Appointment)
        .where(Appointment.business_id == business.id)
        .order_by(desc(Appointment.start_time))
        .offset(skip)
        .limit(min(limit, 100))
    )
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
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentResponse.model_validate(appointment)


@router.post("/", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    data: AppointmentCreate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=422, detail="end_time doit être postérieur à start_time")

    async with db.begin():
        conflict = await db.execute(
            select(Appointment)
            .where(
                Appointment.business_id == business.id,
                Appointment.status != "cancelled",
                Appointment.start_time < data.end_time,
                Appointment.end_time > data.start_time,
            )
            .with_for_update()
        )
        if conflict.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Conflit de créneau horaire")
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
        await db.flush()
        await db.refresh(appointment)
    return AppointmentResponse.model_validate(appointment)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
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
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.business_id == business.id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.status = "cancelled"
    await db.commit()
    return {"success": True, "appointment_id": appointment_id, "status": "cancelled"}


@router.get("/calendar")
async def get_calendar_view(
    start_date: datetime,
    end_date: datetime,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Appointment)
        .where(
            Appointment.business_id == business.id,
            Appointment.start_time >= start_date,
            Appointment.end_time <= end_date,
            Appointment.status != "cancelled",
        )
        .order_by(Appointment.start_time)
    )
    appointments = result.scalars().all()
    return [AppointmentResponse.model_validate(a) for a in appointments]
