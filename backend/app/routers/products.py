from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Product, PriceHistory
from app.schemas.schemas import ProductSchema, ProductCreate, PriceHistorySchema
from datetime import datetime, timezone

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Add initial price history
    history = PriceHistory(
        product_id=db_product.id,
        price=db_product.current_price,
        reason="Initial setup",
        timestamp=datetime.now(timezone.utc)
    )
    db.add(history)
    db.commit()
    
    return db_product

@router.get("/{id}", response_model=ProductSchema)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{id}/price-history", response_model=List[PriceHistorySchema])
def get_product_price_history(id: int, db: Session = Depends(get_db)):
    history = db.query(PriceHistory).filter(PriceHistory.product_id == id).order_by(PriceHistory.timestamp.asc()).all()
    return history
