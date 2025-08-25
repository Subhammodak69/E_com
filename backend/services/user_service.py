from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas.user_schema import *
from error_handling import handle_integrity_error
from utils.email import send_otp_email
from typing import Optional
from utils.cache import *


def send_otp(db: Session, data: UserCreate) -> str:
    exists = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    temp_id = generate_temp_user_id()
    otp = generate_otp()
    store_otp_in_memory(temp_id, otp, ttl_seconds=300)  # OTP valid for 1 minute
    send_otp_email(data.email, otp)
    return temp_id



def create_user(db: Session, data: UserCreate) -> Optional[User]:
    user_data = data.dict()
    user_data["is_active"] = True
    db_user = User(**user_data)

    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        handle_integrity_error()
        return None

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
