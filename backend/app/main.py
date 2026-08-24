from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import engine, Base, SessionLocal
from app.routers import products, pricing, competitors
from app.ml.demand_estimator import demand_estimator
from app.seed import seed_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dynamic Pricing Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    
    # Train ML model
    logger.info("Training demand estimator model...")
    demand_estimator.train()
    
    # Seed DB
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    
    logger.info("Startup complete.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic Pricing Engine API"}
