"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('businesses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('tier', sa.String(), nullable=True),
        sa.Column('features', sa.JSON(), nullable=True),
        sa.Column('limits', sa.JSON(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_businesses_email', 'businesses', ['email'], unique=False)

    op.create_table('customers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_customers_business_id', 'customers', ['business_id'], unique=False)
    op.create_index('ix_customers_phone', 'customers', ['phone'], unique=False)

    op.create_table('calls',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('direction', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('recording_url', sa.String(), nullable=True),
        sa.Column('notes', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_calls_business_id', 'calls', ['business_id'], unique=False)
    op.create_index('ix_calls_customer_id', 'calls', ['customer_id'], unique=False)

    op.create_table('appointments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('calendar_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_appointments_business_id', 'appointments', ['business_id'], unique=False)

    op.create_table('campaigns',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('target_count', sa.Integer(), nullable=True),
        sa.Column('completed_count', sa.Integer(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_campaigns_business_id', 'campaigns', ['business_id'], unique=False)

    op.create_table('payments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(18, 6), nullable=False),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('wallet_address', sa.String(), nullable=True),
        sa.Column('tx_hash', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_payments_business_id', 'payments', ['business_id'], unique=False)

    op.create_table('sms_messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('direction', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sms_messages_business_id', 'sms_messages', ['business_id'], unique=False)

    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_business_id', 'users', ['business_id'], unique=False)

    op.create_table('consent_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('caller_phone_hash', sa.String(), nullable=False),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('purpose', sa.String(), nullable=False),
        sa.Column('consent_given', sa.Boolean(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_consent_records_caller_phone_hash', 'consent_records', ['caller_phone_hash'], unique=False)
    op.create_index('ix_consent_records_business_id', 'consent_records', ['business_id'], unique=False)

    op.create_table('breach_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.Column('notified_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('breach_logs')
    op.drop_table('consent_records')
    op.drop_table('users')
    op.drop_table('sms_messages')
    op.drop_table('payments')
    op.drop_table('campaigns')
    op.drop_table('appointments')
    op.drop_table('calls')
    op.drop_table('customers')
    op.drop_table('businesses')
