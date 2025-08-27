from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.product_schema import Product, ProductCreate, ProductUpdate,ProductPatch
from services.product_service import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product,
    patch_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.post("/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)


@router.put("/{product_id}", response_model=Product)
def update_existing_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", response_model=Product)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.patch("/{product_id}", response_model=Product)
def patch_product_controller(
    product_id: int,
    product_patch: ProductPatch,
    db: Session = Depends(get_db),
):
    update_data = product_patch.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    db_product = patch_product(db, product_id, update_data)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product