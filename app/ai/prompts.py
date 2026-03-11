"""
Centralized prompt templates for all AI modules.
Separation of prompts from logic enables easy tuning and auditing.
"""

# ─── Predefined Categories for Sustainable Commerce ──────────────────────────

PREDEFINED_CATEGORIES = [
    "Home & Kitchen",
    "Personal Care & Hygiene",
    "Food & Beverages",
    "Fashion & Apparel",
    "Office & Stationery",
    "Cleaning & Laundry",
    "Baby & Kids",
    "Health & Wellness",
    "Garden & Outdoor",
    "Pet Care",
    "Bags & Travel",
    "Gifting & Hampers",
    "Electronics & Accessories",
    "Arts & Crafts",
]

SUSTAINABILITY_FILTER_OPTIONS = [
    "plastic-free",
    "compostable",
    "biodegradable",
    "vegan",
    "cruelty-free",
    "recycled",
    "upcycled",
    "organic",
    "fair-trade",
    "zero-waste",
    "locally-sourced",
    "chemical-free",
    "reusable",
    "energy-efficient",
    "carbon-neutral",
]

# ─── Module 1: Category & Tag Generator Prompts ─────────────────────────────

CATEGORY_SYSTEM_PROMPT = """You are a fast AI categorizer for Rayeva eco-commerce.
1. Primary category MUST be from: {categories}
2. Sub-category must be specific.
3. Generate exactly 5 SEO tags.
4. Sustainability filters MUST be from: {filters}
5. Confidence: "high", "medium", or "low".
Respond with JSON ONLY."""

CATEGORY_USER_PROMPT = """Product: {product_name}
Desc: {product_description}

Return EXACT JSON:
{{
    "primary_category": "...",
    "sub_category": "...",
    "seo_tags": ["t1", "t2", "t3", "t4", "t5"],
    "sustainability_filters": ["f1", "f2"],
    "confidence": "high",
    "reasoning": "1 sentence explanation"
}}"""

# ─── Module 2: B2B Proposal Generator Prompts ───────────────────────────────

PROPOSAL_SYSTEM_PROMPT = """You are a fast B2B eco-sourcing advisor.
Keep total cost WITHIN budget. Allocate by percentage. 
Suggest 3-4 items max. INR pricing.
Respond with JSON ONLY."""

PROPOSAL_USER_PROMPT = """Client: {client_name} | {client_industry}
Budget: ₹{budget} | {requirements}

Return EXACT JSON:
{{
    "product_mix": [
        {{ "product_name": "...", "category": "...", "quantity": 100, "unit_price": 50, "total_price": 5000, "sustainability_note": "1 line" }}
    ],
    "budget_allocation": {{ "Cat1": 50, "Cat2": 50 }},
    "cost_breakdown": {{ "subtotal": 5000, "sustainable_premium": 500, "estimated_savings_vs_conventional": 1000, "total": 5000, "remaining_budget": 0 }},
    "impact_summary": "1 sentence",
    "recommendations": "1 sentence"
}}"""
