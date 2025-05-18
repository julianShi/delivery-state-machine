"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create enum types
    op.execute("CREATE TYPE delivery_status AS ENUM ('CREATED', 'PICKED_UP', 'DELIVERED', 'DELIVERY_CONFIRMED', 'DELIVERY_FAILED', 'PENDING_BY_OPERATOR')")
    op.execute("CREATE TYPE delivery_failure_reason AS ENUM ('INCORRECT_ADDRESS', 'CUSTOMER_NOT_AVAILABLE', 'PACKAGE_DAMAGED', 'OTHER')")

    # Create delivery_orders table
    op.create_table(
        'delivery_orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_address_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('delivery_number', sa.String(), unique=True, nullable=True),
        sa.Column('status', sa.Enum('CREATED', 'PICKED_UP', 'DELIVERED', 'DELIVERY_CONFIRMED', 'DELIVERY_FAILED', 'PENDING_BY_OPERATOR', name='delivery_status'), nullable=False),
        sa.Column('failure_reason', sa.Enum('INCORRECT_ADDRESS', 'CUSTOMER_NOT_AVAILABLE', 'PACKAGE_DAMAGED', 'OTHER', name='delivery_failure_reason'), nullable=True),
        sa.Column('estimated_delivery_time', sa.DateTime(), nullable=True),
        sa.Column('actual_delivery_time', sa.DateTime(), nullable=True),
        sa.Column('operator_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('operator_notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['customer_address_id'], ['customer_addresses.id'], ),
        sa.ForeignKeyConstraint(['operator_id'], ['operators.id'], )
    )

    # Create delivery_state_events table
    op.create_table(
        'delivery_state_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('delivery_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_status', sa.Enum('CREATED', 'PICKED_UP', 'DELIVERED', 'DELIVERY_CONFIRMED', 'DELIVERY_FAILED', 'PENDING_BY_OPERATOR', name='delivery_status'), nullable=False),
        sa.Column('to_status', sa.Enum('CREATED', 'PICKED_UP', 'DELIVERED', 'DELIVERY_CONFIRMED', 'DELIVERY_FAILED', 'PENDING_BY_OPERATOR', name='delivery_status'), nullable=False),
        sa.Column('failure_reason', sa.Enum('INCORRECT_ADDRESS', 'CUSTOMER_NOT_AVAILABLE', 'PACKAGE_DAMAGED', 'OTHER', name='delivery_failure_reason'), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('metadata', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['delivery_id'], ['delivery_orders.id'], )
    )

    # Create indexes
    op.create_index('ix_delivery_orders_order_id', 'delivery_orders', ['order_id'])
    op.create_index('ix_delivery_orders_status', 'delivery_orders', ['status'])
    op.create_index('ix_delivery_state_events_delivery_id', 'delivery_state_events', ['delivery_id'])
    op.create_index('ix_delivery_state_events_created_at', 'delivery_state_events', ['created_at'])

def downgrade():
    # Drop tables
    op.drop_table('delivery_state_events')
    op.drop_table('delivery_orders')

    # Drop enum types
    op.execute('DROP TYPE delivery_status')
    op.execute('DROP TYPE delivery_failure_reason') 