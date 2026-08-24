import random
from sqlalchemy.orm import Session
from app.models.models import Product, PriceHistory, DemandRecord
from app.services.competitor_service import competitor_service
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

def seed_db(db: Session):
    if db.query(Product).first():
        logger.info("Database already seeded.")
        return

    logger.info("Seeding database with sample products...")
    categories = ["Electronics", "Clothing", "Books", "Appliances"]
    
    sample_products = [
        {"name": "iPhone 15 Pro", "category": "Electronics", "base_price": 999, "cost_price": 750, "msrp": 1099},
        {"name": "Samsung 65\" 4K TV", "category": "Electronics", "base_price": 799, "cost_price": 500, "msrp": 899},
        {"name": "Sony WH-1000XM5", "category": "Electronics", "base_price": 348, "cost_price": 250, "msrp": 399},
        {"name": "MacBook Air M2", "category": "Electronics", "base_price": 1099, "cost_price": 850, "msrp": 1199},
        {"name": "Nintendo Switch OLED", "category": "Electronics", "base_price": 349, "cost_price": 280, "msrp": 349},
        {"name": "Levi's 501 Original Fit Jeans", "category": "Clothing", "base_price": 59, "cost_price": 25, "msrp": 79},
        {"name": "Nike Air Force 1", "category": "Clothing", "base_price": 110, "cost_price": 45, "msrp": 120},
        {"name": "Patagonia Better Sweater", "category": "Clothing", "base_price": 149, "cost_price": 60, "msrp": 149},
        {"name": "The Great Gatsby", "category": "Books", "base_price": 15, "cost_price": 5, "msrp": 17},
        {"name": "Atomic Habits", "category": "Books", "base_price": 20, "cost_price": 8, "msrp": 27},
        {"name": "Dune by Frank Herbert", "category": "Books", "base_price": 18, "cost_price": 7, "msrp": 22},
        {"name": "Dyson V15 Detect", "category": "Appliances", "base_price": 699, "cost_price": 450, "msrp": 749},
        {"name": "Instant Pot Duo 7-in-1", "category": "Appliances", "base_price": 99, "cost_price": 55, "msrp": 129},
        {"name": "Ninja Creami Ice Cream Maker", "category": "Appliances", "base_price": 199, "cost_price": 110, "msrp": 229},
        {"name": "Vitamix 5200 Blender", "category": "Appliances", "base_price": 429, "cost_price": 250, "msrp": 479},
    ]

    for p_data in sample_products:
        current_price = p_data["base_price"]
        stock_level = random.randint(20, 300)
        
        product = Product(
            name=p_data["name"],
            category=p_data["category"],
            base_price=p_data["base_price"],
            cost_price=p_data["cost_price"],
            msrp=p_data["msrp"],
            current_price=current_price,
            stock_level=stock_level
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # Generate 30 days of price history and demand
        now = datetime.now(timezone.utc)
        hist_price = p_data["base_price"]
        for i in range(30, -1, -1):
            date_record = now - timedelta(days=i)
            
            # slight variation in history
            if random.random() > 0.7:
                hist_price = round(hist_price * random.uniform(0.95, 1.05), 2)
            
            history = PriceHistory(
                product_id=product.id,
                price=hist_price,
                reason="Algorithm adjustment",
                timestamp=date_record
            )
            db.add(history)
            
            demand = DemandRecord(
                product_id=product.id,
                units_sold=random.randint(5, 50),
                price_at_sale=hist_price,
                timestamp=date_record
            )
            db.add(demand)
            
        db.commit()
        
        # Initial competitor prices
        competitor_service.simulate_price_update(product.id, db)
        
    logger.info("Database seeded successfully.")
