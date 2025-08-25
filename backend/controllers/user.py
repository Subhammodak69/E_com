from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db 
from schemas import UserCreate, UserRead, UserUpdate,OTPVerify,UserCreateWithOTP
from services import user_service
from utils.cache import get_otp

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/send-otp")
def send_otp(user: UserCreate, db: Session = Depends(get_db)):
    temp_id = user_service.send_otp(db, user)
    return {"temp_id": temp_id, "message": "OTP sent to your email."}


@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    cached_otp = get_otp(data.temp_id)
    if not cached_otp or cached_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "OTP verified!"}

@router.post("/", response_model=UserRead)
def create_user(data: UserCreateWithOTP, db: Session = Depends(get_db)):
    user_data = UserCreate(**data.dict())
    temp_id = data.temp_id
    otp_input = data.otp_input
    db_user = user_service.create_user(db, user_data, otp_input, temp_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid OTP or user already exists")
    return db_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip, limit)
    return users

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.patch_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
