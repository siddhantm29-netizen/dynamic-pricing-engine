import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app.routers import products, pricing, competitors
from app.ml.demand_estimator import demand_estimator
from app.seed import seed_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dynamic Pricing Engine API",
    description="ML-powered dynamic pricing for e-commerce",
    version="1.0.0",
)

# Read allowed origins from env var (comma-separated), default to all in dev
_raw_origins = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in _raw_origins.split(",")] if _raw_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(pricing.router)
app.include_router(competitors.router)

@app.on_event("startup")
def on_startup():
    logger.info("Starting up Dynamic Pricing Engine...")
    logger.info("Training demand estimator model...")
    demand_estimator.train()
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    logger.info("Startup complete.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic Pricing Engine API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Ping with UptimeRobot (free) every 5 min to prevent Render sleep."""
    return {"status": "ok"}
