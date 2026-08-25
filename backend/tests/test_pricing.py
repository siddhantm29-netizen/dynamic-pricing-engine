"""
Tests for Dynamic Pricing Engine API.
TESTING=1 and DATABASE_URL are set in conftest.py before any import.
"""


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_products_empty(client):
    """GET /products/ on empty DB returns empty list."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_dashboard_stats_empty(client):
    """Dashboard stats on empty DB returns zeros."""
    response = client.get("/pricing/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert data["total_products"] == 0


def test_product_not_found(client):
    """Non-existent product returns 404."""
    response = client.get("/pricing/99999/recommend")
    assert response.status_code == 404
