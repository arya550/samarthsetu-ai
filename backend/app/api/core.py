"""API routes: eligibility check, results, history, schemes, health."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app import store
from app.services.scheme_matching_service import SchemeMatchingService

router = APIRouter()

_service = SchemeMatchingService()


class EligibilityCheckRequest(BaseModel):
    applicant: Dict[str, Any]
    profile_sources: Optional[Dict[str, str]] = None
    document_states: Optional[Dict[str, bool]] = None


@router.post("/eligibility/check")
async def check_eligibility(request: EligibilityCheckRequest):
    """Run the full pipeline: candidates → Rule Engine → explanation → pathway."""
    if not request.applicant or not isinstance(request.applicant, dict):
        raise HTTPException(status_code=400, detail="applicant profile is required")
    try:
        states = request.document_states
        if states is None:
            states = store.load_doc_states()
        return _service.run_check(
            dict(request.applicant),
            profile_sources=request.profile_sources,
            document_states=states,
        )
    except Exception as exc:  # pragma: no cover — safety net so users never see a blank screen
        raise HTTPException(status_code=500, detail=f"Eligibility check failed: {exc}")


@router.get("/schemes")
async def list_schemes():
    """List all seeded prototype schemes (clearly labelled demo data)."""
    schemes = [
        {
            "id": s["id"],
            "code": s["code"],
            "name": s["name"],
            "headline": s.get("headline", ""),
            "best_for": s.get("best_for", ""),
            "authority": s.get("authority", ""),
            "description": s["description"],
            "status": s["status"],
            "data_label": s["data_label"],
            "official_reference": s.get("official_reference"),
            "rule_count": len(s["eligibility_rules"]),
            "required_documents": [d["name"] for d in s["documents"] if d["required"]],
            "partner": s["partner"]["name"],
        }
        for s in store.SCHEMES
    ]
    return {"schemes": schemes, "count": len(schemes), "data_label": store.DATA_LABEL}


@router.get("/schemes/{scheme_id}")
async def get_scheme(scheme_id: int):
    for s in store.SCHEMES:
        if s["id"] == scheme_id:
            return {"scheme": s, "data_label": store.DATA_LABEL}
    raise HTTPException(status_code=404, detail="Scheme not found")


@router.get("/results/{result_id}")
async def get_result(result_id: str):
    result = store.get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


class DocumentStatesRequest(BaseModel):
    document_states: Dict[str, bool]


@router.patch("/documents")
async def update_document_states(request: DocumentStatesRequest):
    """Persist the user's own document readiness choices.

    These are the user's self-marks — never verification. They are stored
    globally and merged into saved results so history reflects them.
    """
    store.save_doc_states(request.document_states)
    updated = store.apply_doc_states_to_results(request.document_states)
    return {
        "saved": True,
        "ready_count": sum(1 for v in request.document_states.values() if v),
        "results_updated": updated,
    }


@router.get("/documents")
async def get_document_states():
    return {"document_states": store.load_doc_states()}


@router.get("/history")
async def get_history():
    """Previous eligibility checks (newest first)."""
    items = []
    for r in store.list_results():
        items.append({
            "result_id": r["result_id"],
            "status": r["status"],
            "scheme_name": r.get("scheme", {}).get("name", "Unknown scheme"),
            "scheme_id": r.get("scheme", {}).get("id", 0),
            "applicant_name": (r.get("applicant_snapshot") or {}).get("name"),
            "evaluated_at": r.get("metadata", {}).get("evaluated_at"),
            "summary": r.get("summary", ""),
        })
    return {"results": items, "count": len(items)}


@router.delete("/history")
async def clear_history():
    """Clear all saved eligibility results (prototype convenience)."""
    store.clear_results()
    return {"cleared": True}


@router.get("/knowledge-graph")
async def knowledge_graph():
    """Knowledge-graph view used for candidate discovery (Rule Engine decides)."""
    return store.knowledge_graph()
