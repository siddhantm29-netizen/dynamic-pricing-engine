from sqlalchemy.orm import Session
from app.models.models import Product, CompetitorPrice
from app.ml.demand_estimator import demand_estimator
from datetime import datetime

class PricingEngine:
    def calculate_optimal_price(self, product_id: int, db: Session) -> dict:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        # Get competitor prices
        competitor_prices = db.query(CompetitorPrice).filter(CompetitorPrice.product_id == product_id).all()
        if not competitor_prices:
            competitor_avg = product.base_price
        else:
            competitor_avg = sum(cp.price for cp in competitor_prices) / len(competitor_prices)

        # Prepare features for demand estimation
        now = datetime.now()
        features = {
            'price': product.current_price,
            'day_of_week': now.weekday(),
            'month': now.month,
            'competitor_avg_price': competitor_avg,
            'stock_level': product.stock_level,
            'is_weekend': 1 if now.weekday() >= 5 else 0
        }

        estimated_demand = demand_estimator.predict(features)
        
        # Simple heuristic for "demand score" based on prediction
        # (Assuming baseline demand is around 50 based on synthetic data)
        demand_score = estimated_demand / 50.0

        return self.apply_pricing_rules(product, competitor_avg, demand_score)

    def apply_pricing_rules(self, product: Product, competitor_avg: float, demand_score: float) -> dict:
        recommended_price = product.current_price
        explanation = []

        # Rule 1: Competitive Matching with Demand Multiplier
        if demand_score > 1.2: # High demand
            recommended_price = competitor_avg * 1.05
            explanation.append("High demand detected. Pricing slightly above market average to maximize margin.")
        elif demand_score < 0.8: # Low demand
            recommended_price = competitor_avg * 0.95
            explanation.append("Low demand detected. Pricing below market average to increase sales volume.")
        else:
            recommended_price = competitor_avg
            explanation.append("Normal demand. Matching market average.")

        # Rule 2: Floor price (Cost + 10% margin)
        floor_price = product.cost_price * 1.10
        if recommended_price < floor_price:
            recommended_price = floor_price
            explanation.append("Recommended price hit the floor constraint. Adjusted to minimum margin (Cost + 10%).")

        # Rule 3: Ceiling price (MSRP + 20%)
        ceiling_price = product.msrp * 1.20
        if recommended_price > ceiling_price:
            recommended_price = ceiling_price
            explanation.append("Recommended price exceeded ceiling constraint. Capped at MSRP + 20%.")

        # Rule 4: Stock level penalty
        if product.stock_level > 200:
            recommended_price *= 0.95
            explanation.append("Excess stock detected. Applied 5% discount to clear inventory.")

        return {
            "product_id": product.id,
            "current_price": round(product.current_price, 2),
            "recommended_price": round(recommended_price, 2),
            "explanation": " ".join(explanation),
            "competitor_avg": round(competitor_avg, 2),
            "demand_score": round(demand_score, 2)
        }

pricing_engine = PricingEngine()
