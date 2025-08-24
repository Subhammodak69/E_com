# models.py
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from enum import IntEnum

Base = declarative_base()

class GenderEnum(IntEnum):
    MALE = 1
    FEMALE = 2
    OTHERS = 3

class RoleEnum(IntEnum):
    ADMIN = 1
    ENDUSER = 2

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    gender = Column(Integer, nullable=False, default=GenderEnum.OTHERS.value)
    role = Column(Integer, nullable=False, default=RoleEnum.ENDUSER.value)
    profile_photo_url = Column(String, nullable=True)
