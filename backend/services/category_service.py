from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryCreate, CategoryUpdate, CategoryBase
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from error_handling import handle_integrity_error





def create_category(db: Session, category_create: CategoryCreate) -> Category:
    db_category = Category(
        name=category_create.name,
        description=category_create.description,
        image=str(category_create.image) if category_create.image else None
    )
    db.add(db_category)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Category:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, category_update: CategoryUpdate) -> Category:
    db_category = get_category(db, category_id)  # raises 404 if not found
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> None:
    db_category = get_category(db, category_id)  # raises 404 if not found
    db.delete(db_category)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)


def update_category_full(db: Session, category_id: int, category: CategoryBase) -> Category:
    db_category = get_category(db, category_id)  # raises 404 if not found

    # Full update: overwrite all fields
    db_category.name = category.name
    db_category.description = category.description
    db_category.image = str(category.image) if category.image else None

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_category)
    return db_category
