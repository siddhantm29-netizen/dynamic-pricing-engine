"""
conftest.py — pytest fixtures.

The key fix: import all models BEFORE create_all so SQLAlchemy's
metadata knows about every table. Then create_all on the TEST engine.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = "sqlite:///:memory:"

# Create test engine FIRST
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Import all models so metadata is populated, then create tables on test engine."""
    # Must import models to register them with Base.metadata
    from app.models.models import Product, CompetitorPrice, PriceHistory, DemandRecord  # noqa: F401
    from app.database import Base

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(setup_test_db):
    """TestClient with DB wired to in-memory SQLite."""
    from app.main import app
    from app.database import get_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
