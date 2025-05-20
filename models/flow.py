import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from .base import Base
from .user_flows import user_flows


class Flow(Base):
    __tablename__ = "flows"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    users = relationship("User", secondary=user_flows, back_populates="flows")