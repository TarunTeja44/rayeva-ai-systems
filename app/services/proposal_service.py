"""
Module 2 Business Logic: Proposal Service.
Handles the business rules and database operations, separate from AI logic.
"""

import logging
from sqlalchemy.orm import Session
from app.models.proposal import Proposal, ProposalItem
from app.schemas.proposal import ProposalItemSchema, CostBreakdown
from app.ai.proposal_ai import generate_proposal
from app.ai.client import ai_client

logger = logging.getLogger(__name__)


def create_proposal(
    client_name: str,
    client_industry: str,
    budget: float,
    requirements: str,
    db: Session,
) -> dict:
    """
    Business flow:
    1. Call AI to generate proposal
    2. Validate against Pydantic schema (fail-fast guard)
    3. Store proposal and line items
    4. Return structured response
    """
    # Step 1: AI generates proposal
    ai_result = generate_proposal(client_name, client_industry, budget, requirements, db)

    # Step 2: Pydantic schema validation — fail-fast if AI output is malformed
    try:
        for item in ai_result.get("product_mix", []):
            ProposalItemSchema(**item)
        CostBreakdown(**ai_result.get("cost_breakdown", {}))
    except Exception as e:
        logger.error(f"AI output failed schema validation: {e} | raw={ai_result}")
        raise ValueError(f"AI produced invalid output: {e}")

    # Step 2: Calculate totals
    total_cost = ai_result["cost_breakdown"].get("total", 0)
    savings = ai_result["cost_breakdown"].get("estimated_savings_vs_conventional", 0)
    savings_pct = round((savings / total_cost * 100), 1) if total_cost > 0 else 0

    # Step 3: Store proposal in DB
    proposal = Proposal(
        client_name=client_name,
        client_industry=client_industry,
        budget=budget,
        requirements=requirements,
        product_mix=ai_result["product_mix"],
        budget_allocation=ai_result["budget_allocation"],
        cost_breakdown=ai_result["cost_breakdown"],
        impact_summary=ai_result["impact_summary"],
        total_estimated_cost=total_cost,
        savings_percentage=savings_pct,
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)

    # Store individual line items
    for item_data in ai_result["product_mix"]:
        item = ProposalItem(
            proposal_id=proposal.id,
            product_name=item_data.get("product_name", ""),
            category=item_data.get("category", ""),
            quantity=item_data.get("quantity", 0),
            unit_price=item_data.get("unit_price", 0),
            total_price=item_data.get("total_price", 0),
            sustainability_note=item_data.get("sustainability_note", ""),
        )
        db.add(item)
    db.commit()

    # Step 4: Return structured response
    return {
        "id": proposal.id,
        "client_name": proposal.client_name,
        "client_industry": proposal.client_industry,
        "budget": proposal.budget,
        "product_mix": ai_result["product_mix"],
        "budget_allocation": ai_result["budget_allocation"],
        "cost_breakdown": ai_result["cost_breakdown"],
        "impact_summary": ai_result["impact_summary"],
        "recommendations": ai_result.get("recommendations", ""),
        "ai_mode": "live" if ai_client.is_live else "mock",
        "created_at": proposal.created_at.isoformat() if proposal.created_at else None,
    }


def get_all_proposals(db: Session, skip: int = 0, limit: int = 50) -> dict:
    """Get all generated proposals."""
    proposals = db.query(Proposal).offset(skip).limit(limit).all()
    total = db.query(Proposal).count()
    return {
        "total": total,
        "proposals": [p.to_dict() for p in proposals],
    }


def get_proposal_by_id(proposal_id: int, db: Session) -> dict:
    """Get a single proposal by ID."""
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        return None
    return proposal.to_dict()
