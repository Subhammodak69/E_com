from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class SubCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class SubCategoryCreate(SubCategoryBase):
    category_id: int

class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class SubCategoryRead(SubCategoryBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True
