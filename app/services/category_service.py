"""
Module 1 Business Logic: Category Service.
Handles the business rules and database operations, separate from AI logic.
"""

import logging
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import CategoryResult
from app.ai.category_ai import generate_category_tags
from app.ai.client import ai_client

logger = logging.getLogger(__name__)


async def categorize_product(name: str, description: str, db: Session) -> dict:
    """
    Business flow:
    1. Call AI to generate categorization
    2. Validate against Pydantic schema (fail-fast guard)
    3. Store in database
    4. Return structured response
    """
    # Step 1: AI generates categorization
    ai_result = await generate_category_tags(name, description, db)

    # Step 2: Pydantic schema validation — fail-fast if AI output is malformed
    try:
        validated_schema = CategoryResult(**ai_result)
    except Exception as e:
        logger.error(f"AI output failed schema validation: {e} | raw={ai_result}")
        raise ValueError(f"AI produced invalid output: {e}")

    # Step 2: Create/find category in DB
    category = _get_or_create_category(ai_result["primary_category"], db)

    # Step 3: Store product with AI-generated data
    product = Product(
        name=name,
        description=description,
        primary_category=ai_result["primary_category"],
        sub_category=ai_result["sub_category"],
        seo_tags=ai_result["seo_tags"],
        sustainability_filters=ai_result["sustainability_filters"],
        ai_confidence=ai_result["confidence"],
        category_id=category.id if category else None,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    # Step 4: Return structured response
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "categorization": {
            "primary_category": ai_result["primary_category"],
            "sub_category": ai_result["sub_category"],
            "seo_tags": ai_result["seo_tags"],
            "sustainability_filters": ai_result["sustainability_filters"],
            "confidence": ai_result["confidence"],
            "reasoning": ai_result["reasoning"],
        },
        "ai_mode": "live" if ai_client.is_live else "mock",
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }


def get_all_products(db: Session, skip: int = 0, limit: int = 50) -> dict:
    """Get all categorized products."""
    products = db.query(Product).offset(skip).limit(limit).all()
    total = db.query(Product).count()
    return {
        "total": total,
        "products": [p.to_dict() for p in products],
    }


def get_categories(db: Session) -> list:
    """Get all predefined categories."""
    from app.ai.prompts import PREDEFINED_CATEGORIES
    return PREDEFINED_CATEGORIES


def _get_or_create_category(name: str, db: Session) -> Category:
    """Find or create a category by name."""
    category = db.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category
