"""
Vercel serverless entry point for Rayeva AI Systems.
All requests are handled by the FastAPI application.
"""

from app.main import app  # noqa: F401 — Vercel picks up the 'app' variable
