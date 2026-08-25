"""
conftest.py — The correct approach:
  Set DATABASE_URL env var BEFORE importing app modules,
  so the app creates its engine pointing at our test DB.
  Then create_all on that same engine.
"""
import os

# MUST be set before any app imports so database.py picks it up
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./test_pricing.db"

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    from app.database import engine, Base
    # Import all models so metadata knows about every table
    from app.models.models import Product, CompetitorPrice, PriceHistory, DemandRecord  # noqa: F401
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(setup_test_db):
    from app.main import app
    with TestClient(app) as c:
        yield c
