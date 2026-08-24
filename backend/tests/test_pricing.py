import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.models import Product

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pricing.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Add a test product
    p = Product(name="Test Prod", category="Test", base_price=100, cost_price=80, msrp=120, current_price=100, stock_level=50)
    db.add(p)
    db.commit()
    db.close()
    
    yield
    # Teardown
    pass

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Prod"

def test_recommend_price():
    # Product ID 1 should exist
    response = client.get("/pricing/1/recommend")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_price" in data
    assert "explanation" in data
    
def test_apply_price():
    payload = {"recommended_price": 105.0, "reason": "Test applied"}
    response = client.post("/pricing/1/apply", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["new_price"] == 105.0
