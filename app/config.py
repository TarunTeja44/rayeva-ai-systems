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
    
    # Vercel serverless functions have a read-only filesystem except for /tmp
    # So if running on Vercel (indicated by VERCEL ENV var), use /tmp for sqlite
    default_db_path = "sqlite:////tmp/rayeva.db" if os.getenv("VERCEL") else "sqlite:///./rayeva.db"
    DATABASE_URL: str = os.getenv("DATABASE_URL", default_db_path)
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @property
    def is_ai_enabled(self) -> bool:
        """Check if Gemini API key is configured."""
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.strip())


settings = Settings()
