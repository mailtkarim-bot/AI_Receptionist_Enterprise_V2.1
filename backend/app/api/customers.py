"""Customers router with all endpoints.

Endpoints:
- GET / → list customers
- GET /{id} → customer details
- PATCH /{id} → update customer
- GET /{id}/interactions → history
- POST /{id}/tag → tag customer
- DELETE /{id} → delete customer
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.customer import Customer
from app.models.call import Call
from app.models.sms_message import SMSMessage
from app.models.business import Business
from app.services.tier_manager import get_current_business
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter()


class TagRequest(BaseModel):
    tag: str
    action: str = "add"  # add or remove


@router.get("/", response_model=list[CustomerResponse])
async def list_customers(
    search: Optional[str] = None,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    query = select(Customer).where(Customer.business_id == business.id).order_by(desc(Customer.created_at))
    if search:
        query = query.where(Customer.name.ilike(f"%{search}%") | Customer.phone.ilike(f"%{search}%"))
    result = await db.execute(query)
    customers = result.scalars().all()
    return [CustomerResponse.model_validate(c) for c in customers]


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return CustomerResponse.model_validate(customer)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    data: CustomerUpdate,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return CustomerResponse.model_validate(customer)


@router.get("/{customer_id}/interactions")
async def get_customer_history(
    customer_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    calls = await db.execute(select(Call).where(Call.customer_id == customer_id).order_by(desc(Call.created_at)))
    sms = await db.execute(select(SMSMessage).where(SMSMessage.customer_id == customer_id).order_by(desc(SMSMessage.created_at)))

    return {
        "customer_id": customer_id,
        "calls": [CallResponse.model_validate(c) for c in calls.scalars().all()],
        "sms_messages": [SMSResponse.model_validate(s) for s in sms.scalars().all()],
    }


@router.post("/{customer_id}/tag")
async def tag_customer(
    customer_id: str,
    data: TagRequest,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    tags = set(customer.tags or [])
    if data.action == "add":
        tags.add(data.tag)
    elif data.action == "remove":
        tags.discard(data.tag)
    customer.tags = list(tags)
    await db.commit()
    return {"success": True, "customer_id": customer_id, "tags": customer.tags}


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: str,
    business: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id, Customer.business_id == business.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    await db.delete(customer)
    await db.commit()
    return {"success": True, "message": "Customer deleted"}
