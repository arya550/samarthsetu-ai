"""
Pathway Assembler — builds the financial pathway, document readiness and
next-step routing from scheme data and the confirmed profile.

Calculated values are always derived from the scheme's stated rates and the
applicant's funding need; nothing is invented. Demo data stays labelled.
"""
from __future__ import annotations

from typing import Any, Dict, List

from app import store
from app.utils import doc_is_marked, format_money


class PathwayAssembler:
    def assemble(
        self,
        scheme: Dict[str, Any],
        applicant: Dict[str, Any],
        document_states: Dict[str, bool] | None = None,
    ) -> Dict[str, Any]:
        return {
            "financial_pathway": self._financial_pathway(scheme, applicant),
            "documents": self._documents(scheme, document_states),
            "next_step": self._next_step(scheme, applicant),
        }

    # ------------------------------------------------------------------
    def _financial_pathway(self, scheme: Dict[str, Any], applicant: Dict[str, Any]) -> Dict[str, Any]:
        finance = scheme["finance"]
        need = applicant.get("funding_need")
        financing_type = finance.get("financing_type", "loan")

        pathway: Dict[str, Any] = {
            "funding_need": need,
            "funding_need_display": format_money(need),
            "assistance": finance.get("assistance_text"),
            "contribution": finance.get("contribution_text"),
            "structure": finance.get("notes"),
            "financing_type": financing_type,
            "next_financial_action": (
                "Prepare your project cost estimate and confirm the margin money you can "
                "contribute before approaching the partner below."
            ),
        }

        components: List[Dict[str, Any]] = []
        if need:
            rate_min, rate_max = finance.get("subsidy_rate_min"), finance.get("subsidy_rate_max")
            margin_rate = finance.get("margin_rate")

            if rate_max:  # subsidy component exists
                lo = round(need * (rate_min or rate_max))
                hi = round(need * rate_max)
                label = "Capital subsidy (grant portion)" if financing_type == "grant_plus_loan" else "Capital subsidy"
                components.append({
                    "kind": "subsidy",
                    "label": label,
                    "display": f"{format_money(lo)} – {format_money(hi)}"
                    if hi > lo else format_money(lo),
                    "basis": f"{rate_min * 100:g}%–{rate_max * 100:g}% of project cost (calculated)"
                    if hi > lo else f"{rate_max * 100:g}% of project cost (calculated)",
                })
            if margin_rate:
                components.append({
                    "kind": "contribution",
                    "label": "Your contribution (margin money)",
                    "display": format_money(round(need * margin_rate)),
                    "basis": f"{margin_rate * 100:g}% of project cost (calculated)",
                })
            subsidised = rate_max or 0
            loan_share = 1 - subsidised - (margin_rate or 0)
            if loan_share > 0:
                components.append({
                    "kind": "loan",
                    "label": "Bank loan (term loan)",
                    "display": format_money(round(need * loan_share)),
                    "basis": f"balance of project cost (calculated)",
                })
            components.append({
                "kind": "calculated_total",
                "label": "Total project cost",
                "display": format_money(need),
                "basis": "your stated funding need",
            })

        pathway["components"] = components
        pathway["calculated"] = bool(components)
        return pathway

    def _documents(self, scheme: Dict[str, Any], states: Dict[str, bool] | None) -> Dict[str, Any]:
        marked = [name for name, ready in (states or {}).items() if ready]
        items = []
        ready_count = 0
        for doc in scheme["documents"]:
            ready = doc_is_marked(doc["name"], marked)
            ready_count += 1 if ready else 0
            items.append({
                "name": doc["name"],
                "required": doc["required"],
                "ready": ready,
                "status_note": "Marked as ready by you" if ready else "Not yet marked",
            })
        return {
            "ready_count": ready_count,
            "total_count": len(items),
            "items": items,
            "verification_note": "Readiness is self-marked, not verified.",
        }

    def _next_step(self, scheme: Dict[str, Any], applicant: Dict[str, Any]) -> Dict[str, Any]:
        partner = scheme["partner"]
        req_docs = [d["name"] for d in scheme["documents"] if d["required"]]
        return {
            "destination": partner["name"],
            "why": partner.get("notes", "This partner processes applications for this scheme."),
            "channel": partner.get("channel", "Visit the application channel"),
            "what_to_take": req_docs,
            "action": "Visit Application Channel",
            "routing_note": "Prototype routing — external application handoff is not connected in this demo.",
            "official_url": partner.get("url"),
        }
