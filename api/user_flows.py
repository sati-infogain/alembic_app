import datetime
import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import SessionLocal
from service.user_flows_service import (
    create_user_flow,
    delete_user_flow,
    get_user_flows,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user_flows", tags=["user_flows"])

class UserFlowBase(BaseModel):
    user_id: UUID
    flow_id: UUID
    permission: Optional[str] = None

class UserFlowCreate(UserFlowBase):
    pass


# You are seeing this warning because Pydantic v2 has changed the config key from orm_mode = True to from_attributes = True in your response models.
class UserFlowRead(UserFlowBase):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    class Config:
        #orm_mode = True
        from_attributes = True  # instead of orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def api_create_user_flow(assoc: UserFlowCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user_flow: user={assoc.user_id}, flow={assoc.flow_id}")
    created = create_user_flow(db, assoc.user_id, assoc.flow_id, assoc.permission)
    if not created:
        logger.warning("UserFlow association already exists")
        raise HTTPException(status_code=400, detail="UserFlow association already exists")
    return {"message": "UserFlow association created"}

@router.get("/", response_model=List[UserFlowRead])
def api_read_user_flows(db: Session = Depends(get_db)):
    logger.info("Fetching user_flows")
    result = get_user_flows(db)
    return [UserFlowRead(**row) for row in result]

@router.delete("/", status_code=204)
def api_delete_user_flow(user_id: UUID, flow_id: UUID, db: Session = Depends(get_db)):
    logger.info(f"Deleting user_flow: user={user_id}, flow={flow_id}")
    deleted = delete_user_flow(db, user_id, flow_id)
    if not deleted:
        logger.warning("UserFlow association not found for deletion")
        raise HTTPException(status_code=404, detail="UserFlow association not found")
    return