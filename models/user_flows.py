import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Table, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .base import Base

user_flows = Table(
    "user_flows",
    Base.metadata,
    Column("user_id", PG_UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("flow_id", PG_UUID(as_uuid=True), ForeignKey("flows.id"), primary_key=True),
    Column("permission", Text, nullable=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column("updated_at", DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False),
    UniqueConstraint("user_id", "flow_id", name="uq_user_flow")
)