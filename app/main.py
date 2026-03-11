"""
Rayeva AI Systems — FastAPI Application Entry Point.
AI-powered modules for sustainable commerce.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.config import settings
from app.database import init_db, get_db, SessionLocal
from app.routers import categories, proposals
from app.models.log import AILog
from app.seed import seed_categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed data on startup."""
    init_db()
    db = SessionLocal()
    try:
        seed_categories(db)
    finally:
        db.close()
    print(f"🚀 {settings.APP_NAME} started")
    print(f"🤖 AI Mode: {'LIVE (Gemini)' if settings.is_ai_enabled else 'MOCK (Demo Data)'}") 
    yield

# ─── App Initialization ─────────────────────────────────────────────────────

app = FastAPI(
    title="Rayeva AI Systems",
    description="AI-powered modules for sustainable commerce — Auto-Category & Tag Generator, B2B Proposal Generator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow_credentials must be False when origins is wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ──────────────────────────────────────────────────────────────────

app.include_router(categories.router)
app.include_router(proposals.router)


@app.get("/api/health")
def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "ai_mode": "live" if settings.is_ai_enabled else "mock (demo)",
        "app": settings.APP_NAME,
    }


@app.get("/api/logs")
def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """📊 View AI prompt/response logs."""
    logs = db.query(AILog).order_by(AILog.created_at.desc()).offset(skip).limit(limit).all()
    total = db.query(AILog).count()
    return {
        "total": total,
        "logs": [log.to_dict() for log in logs],
    }


# ─── Static Files & Frontend ────────────────────────────────────────────────

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def serve_frontend():
    """Serve the demo UI."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Rayeva AI Systems API", "docs": "/docs"}


# Startup logic is handled by the lifespan context manager above.
