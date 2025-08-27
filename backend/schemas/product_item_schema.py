from pydantic import BaseModel
from datetime import date
from typing import Optional
from enums import Size, Color


class ProductItemBase(BaseModel):
    product_id: int
    availibility: int
    size: Size
    color: Color
    price: int
    photo_url: str
    is_active: Optional[bool] = True


class ProductItemCreate(ProductItemBase):
    product_id: int
    availibility: int
    size: Size
    color: Color
    price: int
    photo_url: str
    is_active: Optional[bool] = True


class ProductItemUpdate(ProductItemBase):
    product_id: int
    availibility: int
    size: Size
    color: Color
    price: int
    photo_url: str
    is_active: Optional[bool] = True


class ProductItemInDBBase(ProductItemBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class ProductItem(ProductItemInDBBase):
    product_id: int
    availibility: int
    size: Size
    color: Color
    price: int
    photo_url: str
    is_active: Optional[bool] = True


class ProductItemPatch(BaseModel):
    product_id: Optional[int]
    availibility: Optional[int]
    size: Optional[Size] = None
    color: Optional[Color] = None
    price: Optional[int] = None
    photo_url: Optional[str] = None
    is_active: Optional[bool] = None
