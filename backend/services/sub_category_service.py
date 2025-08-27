from sqlalchemy.orm import Session
from models import SubCategory
from schemas import SubCategoryCreate, SubCategoryUpdate
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from error_handling import handle_integrity_error
from typing import Any, Dict


def create_subcategory(db: Session, subcategory: SubCategoryCreate) -> SubCategory:
    db_sub = SubCategory(**subcategory.dict())
    db.add(db_sub)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_sub)
    return db_sub


def get_subcategory(db: Session, subcategory_id: int) -> SubCategory:
    db_sub = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not db_sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SubCategory not found")
    return db_sub


def get_subcategories(db: Session, skip: int = 0, limit: int = 100) -> List[SubCategory]:
    return db.query(SubCategory).offset(skip).limit(limit).all()


def update_subcategory(db: Session, subcategory_id: int, sub_update: SubCategoryUpdate) -> SubCategory:
    db_sub = get_subcategory(db, subcategory_id)  # raises 404 if not found
    update_data = sub_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sub, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_sub)
    return db_sub


def delete_subcategory(db: Session, subcategory_id: int) -> None:
    db_sub = get_subcategory(db, subcategory_id)  # raises 404 if not found
    db.delete(db_sub)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)


def patch_subcategory(
    db: Session,
    subcategory_id: int,
    sub_patch: SubCategoryUpdate,  # Use same update schema but partial fields only
) -> SubCategory:
    db_sub = get_subcategory(db, subcategory_id)  # raises 404 if not found

    update_data: Dict[str, Any] = sub_patch.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for patch update"
        )

    for field, value in update_data.items():
        if hasattr(db_sub, field):
            setattr(db_sub, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)

    db.refresh(db_sub)
    return db_sub