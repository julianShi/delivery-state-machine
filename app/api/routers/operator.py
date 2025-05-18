from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

router = APIRouter()

# Models
class OperatorAction(str, Enum):
    RETRY_DELIVERY = "RETRY_DELIVERY"
    CANCEL_DELIVERY = "CANCEL_DELIVERY"
    UPDATE_ADDRESS = "UPDATE_ADDRESS"
    CONTACT_CUSTOMER = "CONTACT_CUSTOMER"

class OperatorActionRequest(BaseModel):
    action: OperatorAction
    notes: Optional[str] = None
    new_address_id: Optional[UUID4] = None

class OperatorActionResponse(BaseModel):
    delivery_id: UUID4
    action: OperatorAction
    status: str
    timestamp: datetime
    notes: Optional[str]

# Dependencies
async def get_operator_service():
    # TODO: Implement dependency injection for operator service
    pass

# Endpoints
@router.post("/delivery/{delivery_id}/action", response_model=OperatorActionResponse)
async def take_operator_action(
    delivery_id: UUID4,
    action_request: OperatorActionRequest,
    background_tasks: BackgroundTasks,
    operator_service = Depends(get_operator_service)
):
    """Take operator action on a delivery"""
    try:
        return await operator_service.take_action(
            delivery_id,
            action_request,
            background_tasks
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/delivery/failed", response_model=List[DeliveryResponse])
async def get_failed_deliveries(
    operator_service = Depends(get_operator_service)
):
    """Get list of failed deliveries requiring operator attention"""
    return await operator_service.get_failed_deliveries()

@router.get("/delivery/pending", response_model=List[DeliveryResponse])
async def get_pending_deliveries(
    operator_service = Depends(get_operator_service)
):
    """Get list of deliveries pending operator action"""
    return await operator_service.get_pending_deliveries()

@router.post("/delivery/{delivery_id}/notes")
async def add_operator_notes(
    delivery_id: UUID4,
    notes: str,
    operator_service = Depends(get_operator_service)
):
    """Add operator notes to a delivery"""
    try:
        return await operator_service.add_notes(delivery_id, notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 