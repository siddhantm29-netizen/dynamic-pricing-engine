"""
Tests for the Dynamic Pricing Engine API.
Uses the in-memory SQLite DB from conftest.py — no production data touched.
"""
from app.models.models import Product
from app.database import get_db


def _seed_product(client):
    """Helper: insert a product directly via the DB override and return its id."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.database import Base

    # Re-use the override already registered on the app
    app = client.app
    # Grab a DB session from the override
    gen = app.dependency_overrides[get_db]()
    db = next(gen)
    p = Product(
        name="Test Laptop",
        category="Electronics",
        base_price=1000.0,
        cost_price=700.0,
        msrp=1400.0,
        current_price=1000.0,
        stock_level=50,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    pid = p.id
    try:
        next(gen)
    except StopIteration:
        pass
    return pid


def test_health_check(client):
    """GET / returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """GET /health returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_products_empty(client):
    """GET /products/ returns a list (may be empty on fresh DB)."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dashboard_stats(client):
    """GET /pricing/dashboard/stats returns expected keys."""
    response = client.get("/pricing/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert "avg_price_change_pct" in data
    assert "products_needing_review" in data


def test_product_not_found(client):
    """GET /pricing/99999/recommend returns 404 for non-existent product."""
    response = client.get("/pricing/99999/recommend")
    assert response.status_code == 404


def test_competitor_update(client):
    """POST /competitors/update returns 200."""
    response = client.post("/competitors/update")
    assert response.status_code == 200
