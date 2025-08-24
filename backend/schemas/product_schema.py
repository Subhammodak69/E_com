from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: str
    subcategory_id: int
    is_active: Optional[bool] = True
    created_at: date=None
    updated_at: date=None


class ProductCreate(BaseModel):
    name: str
    description: str
    subcategory_id: int
    is_active: Optional[bool] = True
    created_at: date=None
    updated_at: date=None


class ProductUpdate(BaseModel):
    name: str
    description: str
    subcategory_id: int
    is_active: Optional[bool] = True
    created_at: date
    updated_at: date

class ProductInDBBase(BaseModel):
    id: int
    name: str
    description: str
    subcategory_id: int
    is_active: Optional[bool] = True
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class Product(ProductInDBBase):
    id: int
    name: str
    description: str
    subcategory_id: int
    is_active: Optional[bool] = True
    created_at: date=None
    updated_at: date=None


class ProductPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    subcategory_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: date= None
    updated_at: date=None
