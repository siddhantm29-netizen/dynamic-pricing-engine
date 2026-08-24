import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

class DemandEstimator:
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def generate_synthetic_data(self) -> pd.DataFrame:
        np.random.seed(42)
        n_samples = 1000
        
        # Features
        price = np.random.uniform(10, 1000, n_samples)
        day_of_week = np.random.randint(0, 7, n_samples)
        month = np.random.randint(1, 13, n_samples)
        competitor_avg_price = price * np.random.uniform(0.9, 1.1, n_samples)
        stock_level = np.random.randint(10, 500, n_samples)
        is_weekend = (day_of_week >= 5).astype(int)
        
        # Base demand logic
        # Lower price compared to competitor -> higher demand
        price_ratio = competitor_avg_price / price
        
        # Weekend boost for some categories (simulated generally)
        weekend_boost = is_weekend * 1.5
        
        # Low stock creates scarcity (slight increase in conversion)
        scarcity_multiplier = np.where(stock_level < 50, 1.2, 1.0)
        
        # Calculate target (demand / units sold)
        base_demand = np.random.normal(50, 10, n_samples)
        target = base_demand * price_ratio * weekend_boost * scarcity_multiplier
        target = np.clip(target, 0, None) # No negative demand
        
        df = pd.DataFrame({
            'price': price,
            'day_of_week': day_of_week,
            'month': month,
            'competitor_avg_price': competitor_avg_price,
            'stock_level': stock_level,
            'is_weekend': is_weekend,
            'demand': target
        })
        return df

    def train(self, df: pd.DataFrame = None):
        if df is None:
            logger.info("Generating synthetic data for model training.")
            df = self.generate_synthetic_data()
            
        X = df[['price', 'day_of_week', 'month', 'competitor_avg_price', 'stock_level', 'is_weekend']]
        y = df['demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        logger.info(f"Model trained. Train R2: {train_score:.2f}, Test R2: {test_score:.2f}")
        self.is_trained = True

    def predict(self, features: dict) -> float:
        if not self.is_trained:
            self.train()
            
        df = pd.DataFrame([features])
        # Ensure column order
        df = df[['price', 'day_of_week', 'month', 'competitor_avg_price', 'stock_level', 'is_weekend']]
        prediction = self.model.predict(df)[0]
        return float(prediction)

# Singleton instance
demand_estimator = DemandEstimator()
