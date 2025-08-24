from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from enum import IntEnum
from datetime import datetime

class GenderEnum(IntEnum):
    MALE = 1
    FEMALE = 2
    OTHERS = 3

class RoleEnum(IntEnum):
    ADMIN = 1
    ENDUSER = 2

class UserBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    profile_photo_url: Optional[HttpUrl] = None
    gender: GenderEnum = GenderEnum.OTHERS
    role: RoleEnum = RoleEnum.ENDUSER
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_photo_url: Optional[HttpUrl] = None
    gender: Optional[GenderEnum] = None
    role: Optional[RoleEnum] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True
        use_enum_values = True
        from_attributes = True
