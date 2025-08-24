from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.sub_category_schema import (
    SubCategoryCreate, SubCategoryRead, SubCategoryUpdate
)
from services import sub_category_service

router = APIRouter(prefix="/subcategories", tags=["subcategories"])


@router.post("/", response_model=SubCategoryRead, status_code=status.HTTP_201_CREATED)
def create_subcategory(subcategory: SubCategoryCreate, db: Session = Depends(get_db)):
    return sub_category_service.create_subcategory(db, subcategory)


@router.get("/{subcategory_id}", response_model=SubCategoryRead)
def read_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    db_sub = sub_category_service.get_subcategory(db, subcategory_id)
    if not db_sub:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return db_sub


@router.get("/", response_model=List[SubCategoryRead])
def read_subcategories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return sub_category_service.get_subcategories(db, skip, limit)


@router.put("/{subcategory_id}", response_model=SubCategoryRead)
def update_subcategory(subcategory_id: int, subcategory: SubCategoryUpdate, db: Session = Depends(get_db)):
    db_sub = sub_category_service.update_subcategory(db, subcategory_id, subcategory)
    if not db_sub:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return db_sub

@router.patch("/{subcategory_id}", response_model=SubCategoryRead)
def patch_subcategory(subcategory_id: int, subcategory: SubCategoryUpdate, db: Session = Depends(get_db)):
    db_sub = sub_category_service.update_subcategory(db, subcategory_id, subcategory)
    if not db_sub:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return db_sub


@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    success = sub_category_service.delete_subcategory(db, subcategory_id)
    if not success:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return None
