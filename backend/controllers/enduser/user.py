from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db 
from schemas import UserCreate,UserCreateWithOTP_NoOTPFlag
from services.user_service import *
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


router = APIRouter(prefix="/users", tags=["users"])



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