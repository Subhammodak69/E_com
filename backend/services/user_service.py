from sqlalchemy.orm import Session
from models import User
from typing import Optional
from schemas import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate) -> User:
    user_data = user.dict()
    if user_data.get("profile_photo_url") is not None:
        user_data["profile_photo_url"] = str(user_data["profile_photo_url"])
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserCreate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    user_data = user_update.dict()
    if user_data.get("profile_photo_url") is not None:
        user_data["profile_photo_url"] = str(user_data["profile_photo_url"])
    for field, value in user_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def patch_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    if update_data.get("profile_photo_url") is not None:
        update_data["profile_photo_url"] = str(update_data["profile_photo_url"])
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
