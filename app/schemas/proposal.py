"""
Pydantic schemas for Module 2: B2B Proposal requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ProposalInput(BaseModel):
    """Input schema for B2B proposal generation."""
    client_name: str = Field(..., min_length=2, max_length=200, description="Client/company name")
    client_industry: str = Field(..., min_length=2, max_length=100, description="Client industry")
    budget: float = Field(..., gt=0, description="Budget in INR")
    requirements: Optional[str] = Field(None, max_length=2000, description="Specific requirements or preferences")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "client_name": "GreenTech Solutions Pvt Ltd",
                    "client_industry": "IT & Software",
                    "budget": 100000,
                    "requirements": "Looking for sustainable office supplies, employee welcome kits, and eco-friendly corporate gifts for 50 employees.",
                }
            ]
        }
    }


class ProposalItemSchema(BaseModel):
    """Individual product in the proposal."""
    product_name: str
    category: str
    quantity: int
    unit_price: float
    total_price: float
    sustainability_note: str


class CostBreakdown(BaseModel):
    """Cost breakdown for the proposal."""
    subtotal: float
    sustainable_premium: float
    estimated_savings_vs_conventional: float
    total: float
    remaining_budget: float


class ProposalResponse(BaseModel):
    """Full proposal response with AI-generated data."""
    id: int
    client_name: str
    client_industry: str
    budget: float
    product_mix: List[ProposalItemSchema]
    budget_allocation: dict
    cost_breakdown: CostBreakdown
    impact_summary: str
    recommendations: str
    ai_mode: str
    created_at: Optional[str] = None


class ProposalListResponse(BaseModel):
    """List of generated proposals."""
    total: int
    proposals: List[dict]
