from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.services.pricing_engine import pricing_engine
from app.models.models import Product, PriceHistory
from app.schemas.schemas import PricingRecommendation, PricingApplyRequest
from datetime import datetime, timezone

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.get("/{product_id}/recommend", response_model=PricingRecommendation)
def recommend_price(product_id: int, db: Session = Depends(get_db)):
    recommendation = pricing_engine.calculate_optimal_price(product_id, db)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Product not found")
    return recommendation

@router.post("/{product_id}/apply")
def apply_price(product_id: int, request: PricingApplyRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_price = product.current_price
    product.current_price = request.recommended_price
    
    history = PriceHistory(
        product_id=product.id,
        price=request.recommended_price,
        reason=request.reason,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(history)
    db.commit()
    
    return {"message": "Price applied successfully", "old_price": old_price, "new_price": request.recommended_price}

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    
    # Calculate avg price change
    # Simply get all products and compare current_price to base_price
    products = db.query(Product).all()
    if not products:
        return {"total_products": 0, "avg_price_change_pct": 0, "revenue_impact_pct": 0, "products_needing_review": 0}
        
    price_changes = []
    revenue_impact = []
    needs_review = 0
    
    for p in products:
        if p.base_price > 0:
            pct = (p.current_price - p.base_price) / p.base_price * 100
            price_changes.append(pct)
            
            # Simple revenue impact heuristic
            revenue_impact.append(pct * (p.stock_level / 100.0))
            
        if p.current_price < p.cost_price * 1.15:
            needs_review += 1
            
    avg_price_change = sum(price_changes) / len(price_changes) if price_changes else 0
    avg_revenue_impact = sum(revenue_impact) / len(revenue_impact) if revenue_impact else 0
    
    return {
        "total_products": total_products,
        "avg_price_change_pct": round(avg_price_change, 2),
        "revenue_impact_pct": round(avg_revenue_impact, 2),
        "products_needing_review": needs_review
    }
