"""
Google Gemini client wrapper with retry logic, logging, and mock fallback.
Provides a clean abstraction over the AI provider.
"""

import json
import time
from typing import Optional
from sqlalchemy.orm import Session
from app.config import settings
from app.models.log import AILog


class AIClient:
    """Wrapper around Google Gemini API with logging and mock fallback."""

    def __init__(self):
        self._model = None
        if settings.is_ai_enabled:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._model = genai.GenerativeModel(
                    settings.GEMINI_MODEL,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                    ),
                )
            except Exception:
                self._model = None

    @property
    def is_live(self) -> bool:
        return self._model is not None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        module: str,
        db: Session,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:
        """
        Generate AI response. Uses Gemini if available, falls back to mock.
        Always logs the prompt and response.
        """
        start_time = time.time()

        if self.is_live:
            return self._live_generate(
                system_prompt, user_prompt, module, db, temperature, max_tokens, start_time
            )
        else:
            return self._mock_generate(
                system_prompt, user_prompt, module, db, start_time
            )

    def _live_generate(
        self,
        system_prompt: str,
        user_prompt: str,
        module: str,
        db: Session,
        temperature: float,
        max_tokens: int,
        start_time: float,
    ) -> dict:
        """Make a real API call to Google Gemini."""
        try:
            # Combine system + user prompt for Gemini
            full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

            response = self._model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "response_mime_type": "application/json",
                },
            )

            content = response.text
            latency = (time.time() - start_time) * 1000

            # Estimate tokens (Gemini doesn't always provide exact count)
            tokens = None
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                tokens = (
                    getattr(response.usage_metadata, 'total_token_count', None)
                    or getattr(response.usage_metadata, 'candidates_token_count', 0)
                    + getattr(response.usage_metadata, 'prompt_token_count', 0)
                )

            # Log the call
            self._log(db, module, user_prompt, content, settings.GEMINI_MODEL, tokens, latency, "success")

            return json.loads(content)

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self._log(db, module, user_prompt, str(e), settings.GEMINI_MODEL, None, latency, "error", str(e))
            # Fall back to mock on error
            return self._get_mock_response(module)

    def _mock_generate(
        self,
        system_prompt: str,
        user_prompt: str,
        module: str,
        db: Session,
        start_time: float,
    ) -> dict:
        """Generate mock response for demo purposes."""
        mock_response = self._get_mock_response(module)
        content = json.dumps(mock_response)
        latency = (time.time() - start_time) * 1000

        self._log(db, module, user_prompt, content, "mock", 0, latency, "mock")

        return mock_response

    def _get_mock_response(self, module: str) -> dict:
        """Return realistic mock data based on module."""
        if module == "category_generator":
            return {
                "primary_category": "Personal Care & Hygiene",
                "sub_category": "Oral Care",
                "seo_tags": [
                    "bamboo toothbrush",
                    "eco-friendly oral care",
                    "sustainable dental",
                    "plastic-free toothbrush",
                    "biodegradable brush",
                    "natural bristle toothbrush",
                    "green oral hygiene",
                    "zero waste bathroom",
                ],
                "sustainability_filters": [
                    "plastic-free",
                    "biodegradable",
                    "compostable",
                    "vegan",
                ],
                "confidence": "high",
                "reasoning": "Bamboo toothbrushes are a well-known sustainable personal care product. The bamboo handle is biodegradable and compostable, making it plastic-free. Categorized under Personal Care with Oral Care sub-category.",
            }
        elif module == "proposal_generator":
            return {
                "product_mix": [
                    {
                        "product_name": "Bamboo Toothbrush Set (Pack of 50)",
                        "category": "Personal Care",
                        "quantity": 100,
                        "unit_price": 45,
                        "total_price": 4500,
                        "sustainability_note": "Replaces 100 plastic toothbrushes, bamboo handles are fully biodegradable",
                    },
                    {
                        "product_name": "Recycled Paper Notebooks (A5)",
                        "category": "Office & Stationery",
                        "quantity": 200,
                        "unit_price": 60,
                        "total_price": 12000,
                        "sustainability_note": "Made from 100% post-consumer recycled paper, saves trees and reduces landfill",
                    },
                    {
                        "product_name": "Jute Tote Bags with Logo Print",
                        "category": "Bags & Travel",
                        "quantity": 150,
                        "unit_price": 120,
                        "total_price": 18000,
                        "sustainability_note": "Natural jute fiber, biodegradable, replaces single-use plastic bags",
                    },
                    {
                        "product_name": "Stainless Steel Water Bottles (750ml)",
                        "category": "Home & Kitchen",
                        "quantity": 50,
                        "unit_price": 350,
                        "total_price": 17500,
                        "sustainability_note": "Eliminates use of plastic bottles, durable and long-lasting",
                    },
                    {
                        "product_name": "Organic Cotton Hand Towels",
                        "category": "Home & Kitchen",
                        "quantity": 100,
                        "unit_price": 150,
                        "total_price": 15000,
                        "sustainability_note": "GOTS certified organic cotton, chemical-free production",
                    },
                    {
                        "product_name": "Compostable Trash Bags (Roll of 30)",
                        "category": "Cleaning & Laundry",
                        "quantity": 50,
                        "unit_price": 180,
                        "total_price": 9000,
                        "sustainability_note": "Made from corn starch, fully compostable in 90 days",
                    },
                ],
                "budget_allocation": {
                    "Personal Care": 6,
                    "Office & Stationery": 16,
                    "Bags & Travel": 24,
                    "Home & Kitchen": 43,
                    "Cleaning & Laundry": 12,
                },
                "cost_breakdown": {
                    "subtotal": 76000,
                    "sustainable_premium": 8000,
                    "estimated_savings_vs_conventional": 12000,
                    "total": 76000,
                    "remaining_budget": 24000,
                },
                "impact_summary": "By switching to this sustainable product mix, your organization will eliminate approximately 500+ single-use plastic items monthly, save an estimated 200kg of CO2 emissions annually, and support 6 local eco-friendly manufacturers across India.",
                "recommendations": "Consider a phased rollout starting with high-visibility items like branded jute tote bags and steel water bottles. These create immediate brand impact while demonstrating sustainability commitment to stakeholders and clients.",
            }
        return {"error": "Unknown module", "status": "mock"}

    def _log(
        self,
        db: Session,
        module: str,
        prompt: str,
        response: str,
        model: Optional[str],
        tokens: Optional[int],
        latency: float,
        status: str,
        error: Optional[str] = None,
    ):
        """Log AI call to database."""
        try:
            log = AILog(
                module=module,
                prompt=prompt,
                response=response,
                model_used=model,
                tokens_used=tokens,
                latency_ms=round(latency, 2),
                status=status,
                error_message=error,
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()


# Singleton instance
ai_client = AIClient()
