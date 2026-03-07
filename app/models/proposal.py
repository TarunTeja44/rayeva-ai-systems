"""
Proposal models for Module 2: AI B2B Proposal Generator.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Proposal(Base):
    """AI-generated B2B proposal for sustainable product sourcing."""
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(200), nullable=False)
    client_industry = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    requirements = Column(Text, nullable=True)

    # AI-generated fields
    product_mix = Column(JSON, nullable=True)
    budget_allocation = Column(JSON, nullable=True)
    cost_breakdown = Column(JSON, nullable=True)
    impact_summary = Column(Text, nullable=True)

    # Metadata
    total_estimated_cost = Column(Float, nullable=True)
    savings_percentage = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    items = relationship("ProposalItem", back_populates="proposal", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "client_industry": self.client_industry,
            "budget": self.budget,
            "requirements": self.requirements,
            "product_mix": self.product_mix or [],
            "budget_allocation": self.budget_allocation or {},
            "cost_breakdown": self.cost_breakdown or {},
            "impact_summary": self.impact_summary,
            "total_estimated_cost": self.total_estimated_cost,
            "savings_percentage": self.savings_percentage,
            "items": [item.to_dict() for item in self.items],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ProposalItem(Base):
    """Individual product line item in a B2B proposal."""
    __tablename__ = "proposal_items"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    sustainability_note = Column(Text, nullable=True)

    # Relationships
    proposal = relationship("Proposal", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "category": self.category,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "sustainability_note": self.sustainability_note,
        }
