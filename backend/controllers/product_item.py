from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.product_item_schema import ProductItem, ProductItemCreate, ProductItemUpdate, ProductItemPatch
from services.product_item_service import (
    get_productitem,
    get_productitems,
    create_productitem,
    update_productitem,
    patch_productitem,
    delete_productitem,
)

router = APIRouter(prefix="/productitems", tags=["productitems"])


@router.get("/", response_model=List[ProductItem])
def read_productitems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_productitems(db, skip=skip, limit=limit)


@router.get("/{productitem_id}", response_model=ProductItem)
def read_productitem(productitem_id: int, db: Session = Depends(get_db)):
    return get_productitem(db, productitem_id)


@router.post("/", response_model=ProductItem, status_code=status.HTTP_201_CREATED)
def create_new_productitem(productitem: ProductItemCreate, db: Session = Depends(get_db)):
    return create_productitem(db, productitem)


@router.put("/{productitem_id}", response_model=ProductItem)
def update_existing_productitem(productitem_id: int, productitem: ProductItemUpdate, db: Session = Depends(get_db)):
    return update_productitem(db, productitem_id, productitem)


@router.patch("/{productitem_id}", response_model=ProductItem)
def patch_existing_productitem(productitem_id: int, productitem: ProductItemPatch, db: Session = Depends(get_db)):
    update_data = productitem.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    return patch_productitem(db, productitem_id, update_data)


@router.delete("/{productitem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_productitem(productitem_id: int, db: Session = Depends(get_db)):
    delete_productitem(db, productitem_id)
    return None
