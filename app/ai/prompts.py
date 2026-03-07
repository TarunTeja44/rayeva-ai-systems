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

CATEGORY_SYSTEM_PROMPT = """You are an AI product categorization expert for Rayeva, a sustainable commerce platform in India. 
Your job is to analyze product descriptions and generate accurate categorizations optimized for SEO and sustainability.

IMPORTANT RULES:
1. Primary category MUST be one from this list: {categories}
2. Sub-category should be a specific type within the primary category
3. Generate 5-10 SEO-friendly tags relevant to the product and sustainability
4. Sustainability filters MUST only include applicable items from: {filters}
5. Provide a confidence level: "high", "medium", or "low"

Always respond with valid JSON only, no additional text."""

CATEGORY_USER_PROMPT = """Analyze this product and return a JSON object:

Product Name: {product_name}
Product Description: {product_description}

Return EXACTLY this JSON structure:
{{
    "primary_category": "<one from predefined list>",
    "sub_category": "<specific sub-category>",
    "seo_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "sustainability_filters": ["filter1", "filter2"],
    "confidence": "high|medium|low",
    "reasoning": "<brief explanation of categorization>"
}}"""

# ─── Module 2: B2B Proposal Generator Prompts ───────────────────────────────

PROPOSAL_SYSTEM_PROMPT = """You are a B2B sustainable product sourcing advisor for Rayeva, an eco-commerce platform in India.
You create professional product proposals for businesses looking to switch to sustainable alternatives.

IMPORTANT RULES:
1. Suggest practical, real-world sustainable products (not fictional)
2. Keep total cost WITHIN the provided budget
3. Allocate budget strategically based on client industry and needs
4. Include at least 4-6 product categories in the mix
5. Provide realistic pricing for Indian market (in INR ₹)
6. Always include an impact positioning summary highlighting sustainability benefits

Always respond with valid JSON only, no additional text."""

PROPOSAL_USER_PROMPT = """Generate a B2B sustainable product proposal:

Client: {client_name}
Industry: {client_industry}
Budget: ₹{budget}
Requirements: {requirements}

Return EXACTLY this JSON structure:
{{
    "product_mix": [
        {{
            "product_name": "<name>",
            "category": "<category>",
            "quantity": <number>,
            "unit_price": <price_inr>,
            "total_price": <total_inr>,
            "sustainability_note": "<why this is sustainable>"
        }}
    ],
    "budget_allocation": {{
        "category_name": <percentage>,
        "category_name2": <percentage>
    }},
    "cost_breakdown": {{
        "subtotal": <amount>,
        "sustainable_premium": <amount>,
        "estimated_savings_vs_conventional": <amount>,
        "total": <amount>,
        "remaining_budget": <amount>
    }},
    "impact_summary": "<2-3 sentence impact positioning statement>",
    "recommendations": "<strategic recommendations for the client>"
}}"""
