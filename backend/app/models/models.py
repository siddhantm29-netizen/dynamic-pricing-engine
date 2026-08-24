from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    base_price = Column(Float)
    cost_price = Column(Float)
    msrp = Column(Float)
    current_price = Column(Float)
    stock_level = Column(Integer, default=100)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    competitor_prices = relationship("CompetitorPrice", back_populates="product", cascade="all, delete-orphan")
    demand_records = relationship("DemandRecord", back_populates="product", cascade="all, delete-orphan")

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    competitor_name = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="competitor_prices")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    reason = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="price_history")

class DemandRecord(Base):
    __tablename__ = "demand_records"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    units_sold = Column(Integer)
    price_at_sale = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="demand_records")
