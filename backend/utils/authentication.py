from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from models import User 
from main import secret_key
from datetime import datetime, timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # Adjust token url as per your auth


SECRET_KEY = secret_key
ALGORITHM = "HS256" 

# print(SECRET_KEY)
# print(ALGORITHM)





def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()





ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

