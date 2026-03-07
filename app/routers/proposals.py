"""
Module 2 API Routes: AI B2B Proposal Generator endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.proposal import ProposalInput, ProposalResponse, ProposalListResponse
from app.services.proposal_service import create_proposal, get_all_proposals, get_proposal_by_id

router = APIRouter(prefix="/api/proposals", tags=["Module 2: B2B Proposal Generator"])


@router.post("/generate", response_model=ProposalResponse)
def generate_proposal(proposal: ProposalInput, db: Session = Depends(get_db)):
    """
    📄 AI B2B Proposal Generator

    Takes client details and budget, returns:
    - Suggested sustainable product mix
    - Budget allocation by category
    - Estimated cost breakdown
    - Impact positioning summary
    - Strategic recommendations

    All results stored in database with full AI logging.
    """
    try:
        result = create_proposal(
            proposal.client_name,
            proposal.client_industry,
            proposal.budget,
            proposal.requirements or "",
            db,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proposal generation failed: {str(e)}")


@router.get("/", response_model=ProposalListResponse)
def list_proposals(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """📋 List all generated proposals."""
    return get_all_proposals(db, skip, limit)


@router.get("/{proposal_id}")
def get_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """🔍 Get a specific proposal by ID."""
    result = get_proposal_by_id(proposal_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return result
