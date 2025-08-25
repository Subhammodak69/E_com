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

def generate_temp_user_id(identifier: str) -> str:
    # Create a hash from email or email+phone to serve as temp_id
    hash_key = hashlib.sha256(identifier.lower().encode()).hexdigest()
    return hash_key[:16]

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp(db: Session, data: UserCreate, purpose: str = "signup") -> str:
    # For signup, user MUST NOT exist yet
    if purpose == "signup":
        exists = db.query(User).filter(User.email == data.email, User.is_active == True).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
    # For login, user MUST exist already
    elif purpose == "login":
        exists = db.query(User).filter(User.email == data.email, User.is_active == True).first()
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid purpose")

    identifier = data.email + (data.phone or '')
    temp_id = generate_temp_user_id(identifier)
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
