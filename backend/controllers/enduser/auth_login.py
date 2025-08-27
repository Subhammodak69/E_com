from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db  # Your SQLAlchemy session dependency
from models import User     # Your SQLAlchemy User model
from utils.cache import store_otp_in_memory
from utils.email import send_otp_email
import hashlib
import random
from utils.authentication import *
from schemas.user_schema import LoginWithTempId,LoginWithOtpRequest
from utils.cache import get_otp
from jose import JWTError, jwt
from schemas.user_schema import UserRead

app = FastAPI()
router = APIRouter(prefix="/auth", tags=["auth"])



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if not user:
        raise credentials_exception
    return user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


class EmailRequest(BaseModel):
    email: EmailStr


def generate_temp_user_id(email: str) -> str:
    temp_id = hashlib.sha256(email.lower().encode()).hexdigest()
    return temp_id[:16]

def get_user_by_temp_id(db: Session, temp_id: str) -> User | None:
    """
    Retrieve a user from the database by matching temp_id with 
    the first 16 chars of SHA256 hash of the user's email (lowercased).
    """
    users = db.query(User).all()
    for user in users:
        hashed_email = hashlib.sha256(user.email.lower().encode()).hexdigest()[:16]
        if hashed_email == temp_id:
            return user
    return None

def generate_otp() -> str:
    otp = str(random.randint(100000, 999999))
    print(otp)
    return otp


@router.post("/login-with-temp-id")
def login_with_otp(data: LoginWithTempId, db: Session = Depends(get_db)):
    print(f"Received flag: {data.flag!r}, temp_id: {data.temp_id!r}")

    if data.flag != 'is_otp_verified':
        raise HTTPException(status_code=400, detail="OTP not verified")

    temp_id = data.temp_id
    if not temp_id:
        raise HTTPException(status_code=400, detail="Temp id not found")

    user = get_user_by_temp_id(db, temp_id)  # new function to find user by temp_id hash


    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/send-otp")
def send_login_otp(data: EmailRequest, db: Session = Depends(get_db)):
    print("fdhdbjkfndjbfjhbdbfjdsbjfhbdshbfhsdbfbdsbfdsbnfbdsfdsfbdsnfdsnbfnbdsnbfbds100000000")
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


@router.post("/login/verify-otp")
def verify_otp(data: LoginWithOtpRequest, db: Session = Depends(get_db)):
    print("rbdnfbdbbnf dsnbfdsnbfsndbvfn       dsbfjbdshbfbdsbfdsbfbds6475454t574t75")
    cached_otp = get_otp(data.temp_id)
    if not cached_otp or cached_otp != data.otp:
        print("payniiii")
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    print("peye6e")
    return {"message": "OTP verified!"}

app.include_router(router)



