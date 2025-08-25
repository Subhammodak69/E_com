from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db 
from schemas import UserCreate, UserRead, UserUpdate,OTPVerify,UserCreateWithOTP_NoOTPFlag
from services.user_service import *
from utils.cache import get_otp
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


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
    
    if data.purpose == "signup":
        # Don't delete OTP here for signup - keep it for final user creation
        return {"message": "OTP verified!"}
    
    return {"message": "OTP verified!"}



@router.post("/")
def create_user_endpoint(user_data: UserCreateWithOTP_NoOTPFlag, db: Session = Depends(get_db)):
    # user_data now includes all user fields + otp_verified flag
    if not user_data.otp_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not verified")

    try:
        user_data_dict = user_data.dict(exclude={"otp_verified"})
        user = create_user(db, UserCreate(**user_data_dict))

        if user is None:
            raise HTTPException(status_code=400, detail="User creation failed")

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with provided email or phone already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




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
