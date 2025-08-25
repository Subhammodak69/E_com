from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db  # Your SQLAlchemy session dependency
from models import User     # Your SQLAlchemy User model
from utils.cache import store_otp_in_memory
from utils.email import send_otp_email
import hashlib
import random

app = FastAPI()
router = APIRouter(prefix="/auth", tags=["auth"])


class EmailRequest(BaseModel):
    email: EmailStr


def generate_temp_user_id(email: str) -> str:
    temp_id = hashlib.sha256(email.lower().encode()).hexdigest()
    return temp_id[:16]


def generate_otp() -> str:
    otp = str(random.randint(100000, 999999))
    print(otp)
    return otp


@router.post("/send-otp")
def send_login_otp(data: EmailRequest, db: Session = Depends(get_db)):
    # Check if user exists and is active
    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )

    temp_id = generate_temp_user_id(data.email)
    otp = generate_otp()

    # Store OTP in cache (memory, Redis, etc.)
    store_otp_in_memory(temp_id, otp)

    # Send OTP via email or SMS
    send_otp_email(data.email, otp)

    return {"temp_id": temp_id, "message": "OTP sent to your email."}


app.include_router(router)
