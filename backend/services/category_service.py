from sqlalchemy.orm import Session
from models import Category, SubCategory
from schemas import CategoryCreate, CategoryUpdate,CategoryBase
from typing import Optional, List


# ---------- Category Service ----------
def create_category(db: Session, category_create: CategoryCreate) -> Category:
    # Convert HttpUrl to str before saving
    db_category = Category(
        name=category_create.name,
        description=category_create.description,
        image=str(category_create.image) if category_create.image else None
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, category_update: CategoryUpdate) -> Optional[Category]:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    for field, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    db.delete(db_category)
    db.commit()
    return True


def update_category_full(db: Session, category_id: int, category: CategoryBase) -> Category | None:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None

    # Full update: overwrite all fields
    db_category.name = category.name
    db_category.description = category.description
    db_category.image = str(category.image) if category.image else None

    db.commit()
    db.refresh(db_category)
    return db_category



