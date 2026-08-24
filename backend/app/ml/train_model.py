#!/usr/bin/env python3
"""
Pre-training script — run during Docker build so the model is baked
into the image. Cold starts then load from pickle in <1s.

Usage:
    python -m app.ml.train_model
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.ml.demand_estimator import demand_estimator

if __name__ == "__main__":
    print("Pre-training demand estimation model...")
    demand_estimator.train()
    print("Done — model saved to app/ml/demand_model.pkl")
