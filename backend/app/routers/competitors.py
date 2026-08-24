from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import CompetitorPrice
from app.schemas.schemas import CompetitorPriceSchema
from app.services.competitor_service import competitor_service

router = APIRouter(prefix="/competitors", tags=["competitors"])

@router.get("/{product_id}", response_model=List[CompetitorPriceSchema])
def get_competitor_prices(product_id: int, db: Session = Depends(get_db)):
    return db.query(CompetitorPrice).filter(CompetitorPrice.product_id == product_id).all()

@router.post("/update")
def update_all_competitor_prices(db: Session = Depends(get_db)):
    competitor_service.simulate_all_updates(db)
    return {"message": "Competitor prices updated successfully"}
