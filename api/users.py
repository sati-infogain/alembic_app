import datetime
import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from db import SessionLocal
from service.user_service import create_user, delete_user, get_user, get_users

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

# You are seeing this warning because Pydantic v2 has changed the config key from orm_mode = True to from_attributes = True in your response models.
class UserRead(UserBase):
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

@router.post("/", response_model=UserRead, status_code=201)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user: {user.email}")
    new_user = create_user(db, user.name, user.email)
    if not new_user:
        logger.warning("User already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

@router.get("/", response_model=List[UserRead])
def api_read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Fetching users")
    return get_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserRead)
def api_read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
def api_delete_user(user_id: UUID, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        logger.warning(f"User {user_id} not found for deletion")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User {user_id} deleted")
    return