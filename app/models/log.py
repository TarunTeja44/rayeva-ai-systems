"""
AI prompt/response logging model.
Every AI call is logged for transparency and debugging.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime, timezone
from app.database import Base


class AILog(Base):
    """Log of every AI API call for auditing and debugging."""
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(50), nullable=False)  # e.g. "category_generator", "proposal_generator"
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)
    status = Column(String(20), default="success")  # success, error, mock
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "module": self.module,
            "prompt": self.prompt[:200] + "..." if len(self.prompt) > 200 else self.prompt,
            "response": self.response[:200] + "..." if len(self.response) > 200 else self.response,
            "model_used": self.model_used,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
