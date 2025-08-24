from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate
from error_handling import handle_integrity_error


def create_user(db: Session, user: UserCreate) -> User:
    user_data = user.dict()
    if user_data.get("profile_photo_url") is not None:
        user_data["profile_photo_url"] = str(user_data["profile_photo_url"])
    db_user = User(**user_data)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserCreate) -> User:
    db_user = get_user(db, user_id)  # Raises 404 if not found
    user_data = user_update.dict()
    if user_data.get("profile_photo_url") is not None:
        user_data["profile_photo_url"] = str(user_data["profile_photo_url"])
    for field, value in user_data.items():
        setattr(db_user, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_user)
    return db_user


def patch_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    db_user = get_user(db, user_id)  # Raises 404 if not found
    update_data = user_update.dict(exclude_unset=True)
    if update_data.get("profile_photo_url") is not None:
        update_data["profile_photo_url"] = str(update_data["profile_photo_url"])
    for field, value in update_data.items():
        setattr(db_user, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user(db, user_id)  # Raises 404 if not found
    db.delete(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
