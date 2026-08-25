"""
Tests for Dynamic Pricing Engine API.
Uses in-memory SQLite DB from conftest.py.
"""
import os
os.environ["TESTING"] = "1"


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
    """GET /products/ on empty DB returns empty list."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_dashboard_stats_empty(client):
    """GET /pricing/dashboard/stats on empty DB returns zeros."""
    response = client.get("/pricing/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert data["total_products"] == 0


def test_product_not_found(client):
    """GET /pricing/99999/recommend returns 404."""
    response = client.get("/pricing/99999/recommend")
    assert response.status_code == 404
