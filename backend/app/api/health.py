"""Health check route."""
from __future__ import annotations

from fastapi import APIRouter

from app import store

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "SamarthSetu AI API is running",
        "version": "1.0.0",
        "schemes_seeded": len(store.SCHEMES),
        "data_label": store.DATA_LABEL,
    }
