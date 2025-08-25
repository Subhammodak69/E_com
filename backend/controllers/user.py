from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db 
from schemas import UserCreate, UserRead, UserUpdate,OTPVerify,UserCreateWithOTP
from services.user_service import *
from utils.cache import get_otp

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/send-otp")
def send_otp_endpoint(user: UserCreate, purpose: str = "signup", db: Session = Depends(get_db)):
    temp_id = send_otp(db, user, purpose)
    return {"temp_id": temp_id, "message": "OTP sent to your email."}

@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    cached_otp = get_otp(data.temp_id)
    if not cached_otp or cached_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    # For login, you might verify user exists, generate token, etc.
    # For signup, OTP is verified here.
    delete_otp(data.temp_id)
    return {"message": "OTP verified!"}

@router.post("/")
def create_user(user_with_otp: UserCreateWithOTP, db: Session = Depends(get_db)):
    cached_otp = get_otp(user_with_otp.temp_id)
    if not cached_otp or cached_otp != user_with_otp.otp_input:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user_data = user_with_otp.dict()
    # Remove temp_id and otp_input keys before creating User model
    user_data.pop('temp_id')
    user_data.pop('otp_input')
    new_user = User(**user_data, is_active=True)

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create user")

    delete_otp(user_with_otp.temp_id)
    return new_user


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip, limit)
    return users

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user =update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = patch_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
