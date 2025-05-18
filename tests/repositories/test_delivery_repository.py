import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.delivery import DeliveryOrder, DeliveryStateEvent
from app.repositories.delivery import DeliveryRepository
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryStatus

@pytest.fixture
def db_session():
    # TODO: Set up test database session
    pass

@pytest.fixture
def delivery_repository(db_session):
    return DeliveryRepository(db_session)

@pytest.fixture
def sample_delivery_create():
    return DeliveryCreate(
        order_id=uuid4(),
        customer_address_id=uuid4(),
        estimated_delivery_time=datetime.utcnow() + timedelta(days=1)
    )

def test_create_delivery(delivery_repository, sample_delivery_create):
    delivery = delivery_repository.create(sample_delivery_create)
    assert delivery.order_id == sample_delivery_create.order_id
    assert delivery.customer_address_id == sample_delivery_create.customer_address_id
    assert delivery.status == DeliveryStatus.CREATED

def test_get_delivery(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    retrieved_delivery = delivery_repository.get(created_delivery.id)
    assert retrieved_delivery.id == created_delivery.id

def test_update_delivery(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    update_data = DeliveryUpdate(
        status=DeliveryStatus.PICKED_UP,
        delivery_number="TEST123"
    )
    updated_delivery = delivery_repository.update(created_delivery.id, update_data)
    assert updated_delivery.status == DeliveryStatus.PICKED_UP
    assert updated_delivery.delivery_number == "TEST123"

def test_get_deliveries_by_order(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    deliveries = delivery_repository.get_by_order(sample_delivery_create.order_id)
    assert len(deliveries) == 1
    assert deliveries[0].id == created_delivery.id

def test_add_state_event(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    event = delivery_repository.add_state_event(
        delivery_id=created_delivery.id,
        from_status=DeliveryStatus.CREATED,
        to_status=DeliveryStatus.PICKED_UP,
        source="TEST",
        description="Test event"
    )
    assert event.delivery_id == created_delivery.id
    assert event.from_status == DeliveryStatus.CREATED
    assert event.to_status == DeliveryStatus.PICKED_UP

def test_get_failed_deliveries(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    delivery_repository.update(
        created_delivery.id,
        DeliveryUpdate(status=DeliveryStatus.DELIVERY_FAILED)
    )
    failed_deliveries = delivery_repository.get_failed_deliveries()
    assert len(failed_deliveries) == 1
    assert failed_deliveries[0].id == created_delivery.id

def test_get_pending_deliveries(delivery_repository, sample_delivery_create):
    created_delivery = delivery_repository.create(sample_delivery_create)
    delivery_repository.update(
        created_delivery.id,
        DeliveryUpdate(status=DeliveryStatus.PENDING_BY_OPERATOR)
    )
    pending_deliveries = delivery_repository.get_pending_deliveries()
    assert len(pending_deliveries) == 1
    assert pending_deliveries[0].id == created_delivery.id 