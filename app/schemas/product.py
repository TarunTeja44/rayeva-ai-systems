"""
Pydantic schemas for Module 1: Product categorization requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ProductInput(BaseModel):
    """Input schema for product categorization."""
    name: str = Field(..., min_length=2, max_length=200, description="Product name")
    description: str = Field(..., min_length=10, max_length=2000, description="Product description")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bamboo Toothbrush",
                    "description": "Eco-friendly toothbrush made from sustainably sourced bamboo with charcoal-infused bristles. Biodegradable handle, BPA-free, comes in recyclable packaging.",
                }
            ]
        }
    }


class CategoryResult(BaseModel):
    """Structured JSON output for AI-generated categorization."""
    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]
    confidence: str
    reasoning: str


class ProductResponse(BaseModel):
    """Full product response with AI categorization."""
    id: int
    name: str
    description: str
    categorization: CategoryResult
    ai_mode: str = Field(description="'live' if using OpenAI, 'mock' if using demo data")
    created_at: Optional[str] = None


class ProductListResponse(BaseModel):
    """List of categorized products."""
    total: int
    products: List[dict]
