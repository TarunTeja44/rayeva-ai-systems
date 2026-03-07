"""
Module 2 AI Logic: B2B Proposal Generator.
Separated from business logic for clean architecture.
"""

from sqlalchemy.orm import Session
from app.ai.client import ai_client
from app.ai.prompts import PROPOSAL_SYSTEM_PROMPT, PROPOSAL_USER_PROMPT


def generate_proposal(
    client_name: str,
    client_industry: str,
    budget: float,
    requirements: str,
    db: Session,
) -> dict:
    """
    Use AI to generate a B2B sustainable product proposal.
    Returns structured dict with product mix, budget allocation, cost breakdown, and impact summary.
    """
    system_prompt = PROPOSAL_SYSTEM_PROMPT
    user_prompt = PROPOSAL_USER_PROMPT.format(
        client_name=client_name,
        client_industry=client_industry,
        budget=f"{budget:,.0f}",
        requirements=requirements or "General sustainable product sourcing",
    )

    result = ai_client.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        module="proposal_generator",
        db=db,
        temperature=0.7,
        max_tokens=3000,
    )

    return _validate_proposal_response(result, budget)


def _validate_proposal_response(data: dict, budget: float) -> dict:
    """Validate AI response and ensure it meets business constraints."""
    validated = {
        "product_mix": data.get("product_mix", []),
        "budget_allocation": data.get("budget_allocation", {}),
        "cost_breakdown": data.get("cost_breakdown", {}),
        "impact_summary": data.get("impact_summary", ""),
        "recommendations": data.get("recommendations", ""),
    }

    # Validate product mix
    if isinstance(validated["product_mix"], list):
        for item in validated["product_mix"]:
            if "total_price" not in item and "unit_price" in item and "quantity" in item:
                item["total_price"] = item["unit_price"] * item["quantity"]

    # Ensure cost breakdown has required fields
    cost = validated["cost_breakdown"]
    if not cost.get("total"):
        total = sum(item.get("total_price", 0) for item in validated["product_mix"])
        cost["total"] = total
        cost.setdefault("subtotal", total)
        cost.setdefault("sustainable_premium", round(total * 0.1, 2))
        cost.setdefault("estimated_savings_vs_conventional", round(total * 0.15, 2))
        cost["remaining_budget"] = round(budget - total, 2)

    # Ensure total doesn't exceed budget (business rule)
    if cost.get("total", 0) > budget:
        # Scale down proportionally
        scale = budget * 0.9 / cost["total"]
        for item in validated["product_mix"]:
            item["total_price"] = round(item.get("total_price", 0) * scale, 2)
            if item.get("quantity") and item.get("unit_price"):
                item["unit_price"] = round(item["total_price"] / item["quantity"], 2)
        cost["total"] = round(cost["total"] * scale, 2)
        cost["subtotal"] = cost["total"]
        cost["remaining_budget"] = round(budget - cost["total"], 2)

    return validated
