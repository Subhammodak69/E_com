from sqlalchemy.orm import Session
from typing import Dict, Any
from models.product_model import Product
from schemas.product_schema import ProductCreate, ProductUpdate
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from error_handling import handle_integrity_error


def get_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        subcategory_id=product.subcategory_id,
        is_active=product.is_active,
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)  # get_product raises 404 if not found
    db_product.name = product.name
    db_product.description = product.description
    db_product.subcategory_id = product.subcategory_id
    db_product.is_active = product.is_active
    db_product.updated_at = date.today()
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)  # raises 404 if not found
    db.delete(db_product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    return db_product


def patch_product(db: Session, product_id: int, update_data: Dict[str, Any]):
    db_product = get_product(db, product_id)  # raises 404 if not found
    for key, value in update_data.items():
        if hasattr(db_product, key):
            setattr(db_product, key, value)
    db_product.updated_at = date.today()
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_product)
    return db_product
