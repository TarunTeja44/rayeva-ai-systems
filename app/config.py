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
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def is_ai_enabled(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY.strip())


settings = Settings()
