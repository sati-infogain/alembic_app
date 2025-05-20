from sqlalchemy.orm import Session

from models.user import User


def create_user(db: Session, name: str, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return None
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True