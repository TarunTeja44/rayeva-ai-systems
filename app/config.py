"""
Environment-based configuration management.
Loads settings from .env file with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = os.getenv("APP_NAME", "Rayeva AI Systems")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rayeva.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    @property
    def is_ai_enabled(self) -> bool:
        """Check if Gemini API key is configured."""
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.strip())


settings = Settings()
