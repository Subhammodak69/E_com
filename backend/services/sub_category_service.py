from sqlalchemy.orm import Session
from models import Category, SubCategory
from schemas import CategoryCreate, CategoryUpdate, SubCategoryCreate, SubCategoryUpdate
from typing import Optional, List


def create_subcategory(db: Session, subcategory: SubCategoryCreate) -> SubCategory:
    db_sub = SubCategory(**subcategory.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub


def get_subcategory(db: Session, subcategory_id: int) -> Optional[SubCategory]:
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def get_subcategories(db: Session, skip: int = 0, limit: int = 100) -> List[SubCategory]:
    return db.query(SubCategory).offset(skip).limit(limit).all()


def update_subcategory(db: Session, subcategory_id: int, sub_update: SubCategoryUpdate) -> Optional[SubCategory]:
    db_sub = get_subcategory(db, subcategory_id)
    if not db_sub:
        return None
    for field, value in sub_update.dict(exclude_unset=True).items():
        setattr(db_sub, field, value)
    db.commit()
    db.refresh(db_sub)
    return db_sub


def delete_subcategory(db: Session, subcategory_id: int) -> bool:
    db_sub = get_subcategory(db, subcategory_id)
    if not db_sub:
        return False
    db.delete(db_sub)
    db.commit()
    return True