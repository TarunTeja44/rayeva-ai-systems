"""
Seed data for demo purposes.
Pre-populates categories and sample products.
"""

from sqlalchemy.orm import Session
from app.models.product import Category
from app.ai.prompts import PREDEFINED_CATEGORIES


def seed_categories(db: Session):
    """Seed predefined categories into the database."""
    existing = db.query(Category).count()
    if existing > 0:
        return  # Already seeded

    for name in PREDEFINED_CATEGORIES:
        category = Category(name=name)
        db.add(category)

    db.commit()
    print(f"✅ Seeded {len(PREDEFINED_CATEGORIES)} categories")
