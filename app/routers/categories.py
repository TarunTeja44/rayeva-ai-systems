"""
Module 1 API Routes: AI Auto-Category & Tag Generator endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductInput, ProductResponse, ProductListResponse
from app.services.category_service import categorize_product, get_all_products, get_categories

router = APIRouter(prefix="/api/categories", tags=["Module 1: Category & Tag Generator"])


@router.post("/generate", response_model=ProductResponse)
async def generate_categorization(product: ProductInput, db: Session = Depends(get_db)):
    """
    🏷️ AI Auto-Category & Tag Generator

    Takes a product name and description, returns:
    - Primary category (from predefined list)
    - Sub-category
    - 5-10 SEO tags
    - Sustainability filters
    - Confidence level and reasoning

    All results stored in database with full AI logging.
    """
    try:
        result = await categorize_product(product.name, product.description, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Categorization failed: {str(e)}")


@router.get("/products", response_model=ProductListResponse)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """📦 List all categorized products."""
    return get_all_products(db, skip, limit)


@router.get("/list")
def list_categories():
    """📋 Get predefined category list."""
    from app.ai.prompts import PREDEFINED_CATEGORIES, SUSTAINABILITY_FILTER_OPTIONS
    return {
        "categories": PREDEFINED_CATEGORIES,
        "sustainability_filters": SUSTAINABILITY_FILTER_OPTIONS,
    }
