from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=schemas.Product, status_code=201)
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_product(db, product_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_product(db, product_id, product_in)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))