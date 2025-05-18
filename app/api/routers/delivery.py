from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum

router = APIRouter()

# Models
class DeliveryStatus(str, Enum):
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    DELIVERY_CONFIRMED = "DELIVERY_CONFIRMED"
    DELIVERY_FAILED = "DELIVERY_FAILED"
    PENDING_BY_OPERATOR = "PENDING_BY_OPERATOR"

class DeliveryFailureReason(str, Enum):
    INCORRECT_ADDRESS = "INCORRECT_ADDRESS"
    CUSTOMER_NOT_AVAILABLE = "CUSTOMER_NOT_AVAILABLE"
    PACKAGE_DAMAGED = "PACKAGE_DAMAGED"
    OTHER = "OTHER"

class DeliveryBase(BaseModel):
    order_id: UUID4
    customer_address_id: UUID4
    estimated_delivery_time: Optional[datetime] = None

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    status: DeliveryStatus
    failure_reason: Optional[DeliveryFailureReason] = None
    delivery_number: Optional[str] = None
    actual_delivery_time: Optional[datetime] = None

class DeliveryResponse(DeliveryBase):
    id: UUID4
    status: DeliveryStatus
    delivery_number: Optional[str]
    failure_reason: Optional[DeliveryFailureReason]
    actual_delivery_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Dependencies
async def get_delivery_service():
    # TODO: Implement dependency injection for delivery service
    pass

# Endpoints
@router.post("/", response_model=DeliveryResponse)
async def create_delivery(
    delivery: DeliveryCreate,
    background_tasks: BackgroundTasks,
    delivery_service = Depends(get_delivery_service)
):
    """Create a new delivery order"""
    try:
        return await delivery_service.create_delivery(delivery, background_tasks)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(
    delivery_id: UUID4,
    delivery_service = Depends(get_delivery_service)
):
    """Get delivery details by ID"""
    delivery = await delivery_service.get_delivery(delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@router.patch("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(
    delivery_id: UUID4,
    delivery_update: DeliveryUpdate,
    background_tasks: BackgroundTasks,
    delivery_service = Depends(get_delivery_service)
):
    """Update delivery status and details"""
    try:
        return await delivery_service.update_delivery(
            delivery_id, 
            delivery_update,
            background_tasks
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/order/{order_id}", response_model=List[DeliveryResponse])
async def get_deliveries_by_order(
    order_id: UUID4,
    delivery_service = Depends(get_delivery_service)
):
    """Get all deliveries for an order"""
    return await delivery_service.get_deliveries_by_order(order_id)

@router.post("/{delivery_id}/confirm")
async def confirm_delivery(
    delivery_id: UUID4,
    background_tasks: BackgroundTasks,
    delivery_service = Depends(get_delivery_service)
):
    """Confirm delivery receipt by customer"""
    try:
        return await delivery_service.confirm_delivery(delivery_id, background_tasks)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 