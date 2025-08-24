from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Dict, Any
from models.product_item_model import ProductItem
from schemas.product_item_schema import ProductItemCreate, ProductItemUpdate
from datetime import date
from error_handling import handle_integrity_error


def get_productitem(db: Session, productitem_id: int) -> ProductItem:
    item = db.query(ProductItem).filter(ProductItem.id == productitem_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductItem not found")
    return item


def get_productitems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductItem).offset(skip).limit(limit).all()


def convert_enum_to_int(data: Dict[str, Any], fields: list):
    for field in fields:
        if field in data and data[field] is not None:
            data[field] = data[field].value
    return data


def create_productitem(db: Session, productitem: ProductItemCreate):
    db_item = ProductItem(
        product_id=productitem.product_id,
        availibility=productitem.availibility,
        size=productitem.size.value,
        color=productitem.color.value,
        price=productitem.price,
        photo_url=str(productitem.photo_url),
        is_active=productitem.is_active,
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_item)
    return db_item


def update_productitem(db: Session, productitem_id: int, productitem_update: ProductItemUpdate):
    db_item = get_productitem(db, productitem_id)
    data = productitem_update.dict()
    data = convert_enum_to_int(data, ['size', 'color'])
    for field, value in data.items():
        setattr(db_item, field, value)
    db_item.updated_at = date.today()
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_item)
    return db_item


def patch_productitem(db: Session, productitem_id: int, update_data: Dict[str, Any]):
    db_item = get_productitem(db, productitem_id)
    update_data = convert_enum_to_int(update_data, ['size', 'color'])
    for key, value in update_data.items():
        if hasattr(db_item, key):
            setattr(db_item, key, value)
    db_item.updated_at = date.today()
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
    db.refresh(db_item)
    return db_item


def delete_productitem(db: Session, productitem_id: int):
    db_item = get_productitem(db, productitem_id)
    db.delete(db_item)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)
