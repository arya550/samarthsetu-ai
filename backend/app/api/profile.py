"""API routes: profile extraction and demo start."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app import store
from app.services.nl_extractor import NLProfileExtractor

router = APIRouter()


class ExtractRequest(BaseModel):
    description: str = Field(min_length=3, max_length=2000)


class DemoStartResponse(BaseModel):
    message: str
    demo_label: str
    applicant: Dict[str, Any]


@router.post("/profile/extract")
async def extract_profile(request: ExtractRequest):
    """Extract structured profile fields from a natural-language description.

    Extraction only fills profile fields — the user confirms them in the UI
    before any eligibility check runs.
    """
    extractor = NLProfileExtractor()
    profile, sources = extractor.extract_with_confidence(request.description)
    return {
        "profile": profile,
        "sources": sources,
        "note": "Please review and edit the extracted fields before checking eligibility.",
    }


@router.post("/demo/start", response_model=DemoStartResponse)
async def start_demo():
    """Load the ready-made demo applicant (uses the same pipeline as manual users)."""
    return {
        "message": "Demo applicant loaded — Aarav Patel, food processing, ₹5 lakh need.",
        "demo_label": "Demo Applicant",
        "applicant": dict(store.DEMO_APPLICANT),
    }
