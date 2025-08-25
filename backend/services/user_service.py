from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
import random
from schemas import UserCreate, UserUpdate
from error_handling import handle_integrity_error
from utils.cache import store_otp_in_memory, get_otp, delete_otp
from utils.email import send_otp_email
from typing import Optional
import hashlib

def generate_temp_user_id(email: str, phone: str) -> str:
    unique_string = f"{email.lower()}_{phone}"
    temp_id = hashlib.sha256(unique_string.encode()).hexdigest()
    # Return a shorter unique id (e.g., the first 16 characters)
    return temp_id[:16]


def generate_otp():
    otp = str(random.randint(100000, 999999))
    print(otp)
    return otp

def send_otp(db: Session, data: UserCreate) -> str:
    # Check if a user with the same email and active already exists
    is_user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if is_user:
        # Raise HTTPException to return an error response
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    temp_id = generate_temp_user_id(data.email, data.phone)
    otp = generate_otp()
    store_otp_in_memory(temp_id, otp)
    send_otp_email(data.email, otp)
    return temp_id

def create_user(db: Session, data: UserCreate, otp_input: str, temp_id: str) -> Optional[User]:
    cached_otp = get_otp(temp_id)
    if not cached_otp or cached_otp != otp_input:
        return None  # Will trigger HTTP error

    user_data = data.dict()
    user_data["is_active"] = True
    db_user = User(**user_data)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
        return None
    delete_otp(temp_id)
    return db_user


def verify_otp(db: Session, user_id: int, otp_input: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    cached_otp = get_otp(user_id)
    if not cached_otp or cached_otp != otp_input:
        return None

    user.is_active = True
    db.commit()
    db.refresh(user)
    delete_otp(user_id)

    return user




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
