import os
import pickle
import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "demand_model.pkl")


class DemandEstimator:
    FEATURES = ["price", "day_of_week", "month", "competitor_avg_price",
                "stock_level", "is_weekend"]

    def __init__(self):
        self.model: GradientBoostingRegressor | None = None
        self.is_trained = False

    # ------------------------------------------------------------------
    def generate_synthetic_data(self) -> pd.DataFrame:
        np.random.seed(42)
        n = 1000
        price = np.random.uniform(10, 1000, n)
        day_of_week = np.random.randint(0, 7, n)
        month = np.random.randint(1, 13, n)
        competitor_avg_price = price * np.random.uniform(0.9, 1.1, n)
        stock_level = np.random.randint(10, 500, n)
        is_weekend = (day_of_week >= 5).astype(int)

        price_ratio = competitor_avg_price / price
        weekend_boost = is_weekend * 1.5
        scarcity = np.where(stock_level < 50, 1.2, 1.0)
        base = np.random.normal(50, 10, n)
        demand = np.clip(base * price_ratio * weekend_boost * scarcity, 0, None)

        return pd.DataFrame({
            "price": price, "day_of_week": day_of_week, "month": month,
            "competitor_avg_price": competitor_avg_price, "stock_level": stock_level,
            "is_weekend": is_weekend, "demand": demand,
        })

    # ------------------------------------------------------------------
    def train(self, df: pd.DataFrame = None) -> None:
        # Fast path: load from disk
        if os.path.exists(MODEL_PATH):
            logger.info("Loading pre-trained demand model from disk...")
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            self.is_trained = True
            logger.info("Demand model loaded in <1s ✓")
            return

        logger.info("Training demand estimation model for the first time...")
        if df is None:
            df = self.generate_synthetic_data()

        X = df[self.FEATURES]
        y = df["demand"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # n_estimators=50 → ~2× faster with minimal accuracy loss
        self.model = GradientBoostingRegressor(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)

        r2_train = self.model.score(X_train, y_train)
        r2_test = self.model.score(X_test, y_test)
        logger.info(f"Model trained. R² train={r2_train:.2f}, test={r2_test:.2f}")
        self.is_trained = True

        try:
            with open(MODEL_PATH, "wb") as f:
                pickle.dump(self.model, f)
            logger.info("Demand model saved to disk for fast future loads ✓")
        except OSError as e:
            logger.warning(f"Could not save model: {e}")

    # ------------------------------------------------------------------
    def predict(self, features: dict) -> float:
        if not self.is_trained:
            self.train()
        df = pd.DataFrame([features])[self.FEATURES]
        return float(self.model.predict(df)[0])


demand_estimator = DemandEstimator()
