import random
from sqlalchemy.orm import Session
from app.models.models import Product, CompetitorPrice
from datetime import datetime, timezone

COMPETITORS = ["Amazon", "Walmart", "BestBuy", "Target", "Ebay"]

class CompetitorService:
    def simulate_price_update(self, product_id: int, db: Session):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return

        # Delete old competitor prices for this product
        db.query(CompetitorPrice).filter(CompetitorPrice.product_id == product_id).delete()

        new_prices = []
        for comp in COMPETITORS:
            # Competitor prices fluctuate within ±15% of the base price
            variation = random.uniform(0.85, 1.15)
            comp_price = round(product.base_price * variation, 2)
            
            cp = CompetitorPrice(
                product_id=product.id,
                competitor_name=comp,
                price=comp_price,
                timestamp=datetime.now(timezone.utc)
            )
            db.add(cp)
            new_prices.append(cp)
            
        db.commit()
        return new_prices

    def simulate_all_updates(self, db: Session):
        products = db.query(Product).all()
        for p in products:
            self.simulate_price_update(p.id, db)

competitor_service = CompetitorService()
