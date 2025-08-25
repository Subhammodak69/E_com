from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db 
from schemas import UserCreate,OTPVerify
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

    delete_otp(data.temp_id)
    return {"message": "OTP verified!"}