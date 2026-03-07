"""
Product, Category, and Tag models for Module 1: AI Auto-Category & Tag Generator.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Category(Base):
    """Predefined product categories for sustainable commerce."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category_rel")


class Product(Base):
    """Product with AI-generated categorization and tags."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # AI-generated fields
    primary_category = Column(String(100), nullable=True)
    sub_category = Column(String(100), nullable=True)
    seo_tags = Column(JSON, nullable=True)  # List of 5-10 SEO tags
    sustainability_filters = Column(JSON, nullable=True)  # e.g. plastic-free, vegan

    # Metadata
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    ai_confidence = Column(String(20), nullable=True)  # high, medium, low
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    category_rel = relationship("Category", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "primary_category": self.primary_category,
            "sub_category": self.sub_category,
            "seo_tags": self.seo_tags or [],
            "sustainability_filters": self.sustainability_filters or [],
            "ai_confidence": self.ai_confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
