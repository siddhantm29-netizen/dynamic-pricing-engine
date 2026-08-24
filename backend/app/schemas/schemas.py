from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: str
    base_price: float
    cost_price: float
    msrp: float
    current_price: float
    stock_level: int = 100

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CompetitorPriceSchema(BaseModel):
    id: int
    product_id: int
    competitor_name: str
    price: float
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class PriceHistorySchema(BaseModel):
    id: int
    product_id: int
    price: float
    reason: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class PricingRecommendation(BaseModel):
    product_id: int
    current_price: float
    recommended_price: float
    explanation: str
    competitor_avg: float
    demand_score: float

class PricingApplyRequest(BaseModel):
    recommended_price: float
    reason: str
