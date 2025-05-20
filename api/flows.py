import datetime
import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import SessionLocal
from service.flow_service import create_flow, delete_flow, get_flow, get_flows

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/flows", tags=["flows"])

class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None

class FlowCreate(FlowBase):
    pass

# You are seeing this warning because Pydantic v2 has changed the config key from orm_mode = True to from_attributes = True in your response models.
class FlowRead(FlowBase):
    id: UUID
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    class Config:
        #orm_mode = True
        from_attributes = True  # instead of orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FlowRead, status_code=201)
def api_create_flow(flow: FlowCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating flow: {flow.name}")
    new_flow = create_flow(db, flow.name, flow.description)
    return new_flow

@router.get("/", response_model=List[FlowRead])
def api_read_flows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Fetching flows")
    return get_flows(db, skip, limit)

@router.get("/{flow_id}", response_model=FlowRead)
def api_read_flow(flow_id: UUID, db: Session = Depends(get_db)):
    flow = get_flow(db, flow_id)
    if not flow:
        logger.warning(f"Flow {flow_id} not found")
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow

@router.delete("/{flow_id}", status_code=204)
def api_delete_flow(flow_id: UUID, db: Session = Depends(get_db)):
    success = delete_flow(db, flow_id)
    if not success:
        logger.warning(f"Flow {flow_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Flow not found")
    logger.info(f"Flow {flow_id} deleted")
    return