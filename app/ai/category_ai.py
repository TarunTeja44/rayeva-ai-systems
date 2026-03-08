"""
Module 1 AI Logic: Auto-Category & Tag Generator.
Separated from business logic for clean architecture.
"""

import re
from sqlalchemy.orm import Session
from app.ai.client import ai_client
from app.ai.prompts import (
    CATEGORY_SYSTEM_PROMPT,
    CATEGORY_USER_PROMPT,
    PREDEFINED_CATEGORIES,
    SUSTAINABILITY_FILTER_OPTIONS,
)


def _sanitize_input(text: str, max_length: int = 2000) -> str:
    """Sanitize user input to prevent prompt injection and format-string breakage."""
    # Truncate to max length
    text = text[:max_length]
    # Escape curly braces to prevent .format() injection/crashes
    text = text.replace("{", "{{").replace("}", "}}")
    # Remove prompt injection attempts — catches 'ignore [any words] instructions/prompts/rules'
    text = re.sub(r'(?i)ignore\s+(?:\w+\s+){0,4}(instructions?|prompts?|rules?)', '[FILTERED]', text)
    text = re.sub(r'(?i)(system\s*:\s*|assistant\s*:\s*)', '[FILTERED]', text)
    return text.strip()


def generate_category_tags(product_name: str, product_description: str, db: Session) -> dict:
    """
    Use AI to generate category, sub-category, SEO tags, and sustainability filters
    for a given product.

    Returns structured dict with all categorization data.
    """
    system_prompt = CATEGORY_SYSTEM_PROMPT.format(
        categories=", ".join(PREDEFINED_CATEGORIES),
        filters=", ".join(SUSTAINABILITY_FILTER_OPTIONS),
    )

    user_prompt = CATEGORY_USER_PROMPT.format(
        product_name=_sanitize_input(product_name, 200),
        product_description=_sanitize_input(product_description, 2000),
    )

    result = ai_client.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        module="category_generator",
        db=db,
        temperature=0.5,
    )

    # Validate and sanitize the response
    return _validate_category_response(result)


def _validate_category_response(data: dict) -> dict:
    """Validate AI response and ensure it meets schema requirements."""
    validated = {
        "primary_category": data.get("primary_category", "Uncategorized"),
        "sub_category": data.get("sub_category", "General"),
        "seo_tags": data.get("seo_tags", []),
        "sustainability_filters": data.get("sustainability_filters", []),
        "confidence": data.get("confidence", "medium"),
        "reasoning": data.get("reasoning", ""),
    }

    # Ensure primary category is from predefined list
    if validated["primary_category"] not in PREDEFINED_CATEGORIES:
        # Find closest match or default
        for cat in PREDEFINED_CATEGORIES:
            if cat.lower() in validated["primary_category"].lower() or \
               validated["primary_category"].lower() in cat.lower():
                validated["primary_category"] = cat
                break
        else:
            validated["primary_category"] = "Home & Kitchen"
            validated["confidence"] = "low"

    # Ensure SEO tags is a list with 5-10 items
    if not isinstance(validated["seo_tags"], list):
        validated["seo_tags"] = []
    validated["seo_tags"] = validated["seo_tags"][:10]

    # Validate sustainability filters
    if isinstance(validated["sustainability_filters"], list):
        validated["sustainability_filters"] = [
            f for f in validated["sustainability_filters"]
            if f in SUSTAINABILITY_FILTER_OPTIONS
        ]

    return validated
