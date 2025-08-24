from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from schemas.sub_category_schema import SubCategoryRead  


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CategoryWithSubcategories(CategoryRead):
    subcategories: List["SubCategoryRead"] = []
