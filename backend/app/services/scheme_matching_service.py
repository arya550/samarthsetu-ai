"""
Scheme Matching Service — orchestrates the complete pipeline:

    Applicant profile
      → Knowledge-graph candidate discovery
      → Deterministic Rule Engine (authority)
      → Explanation generation (AI layer, explanatory only)
      → Pathway assembly (finance, documents, next step)

Results are persisted via the store so History survives restarts.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app import store
from app.rules.rule_engine import RuleEngine
from app.services.comparison_builder import ComparisonBuilder
from app.services.explanation_generator import ExplanationGenerator
from app.services.matcher import KnowledgeGraphMatcher
from app.services.pathway_assembler import PathwayAssembler

TRUST_STATEMENT = "The rule engine checks the fit. AI explains the fit."


class SchemeMatchingService:
    BANK_OPTIONS_NOTE = (
        "Bank-loan options are grounded recommendations from each bank's published product pages \u2014 "
        "not decided by the rule engine. Eligibility, documents, rate and tenure are decided by "
        "the bank per application. Confirm on the bank's website before applying."
    )

    def __init__(self) -> None:
        self.matcher = KnowledgeGraphMatcher()
        self.rule_engine = RuleEngine()
        self.explainer = ExplanationGenerator()
        self.pathway = PathwayAssembler()
        self.comparator = ComparisonBuilder()

    @staticmethod
    def _all_ranked_schemes(applicant: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return every scheme in the catalogue, evaluated by the rule engine
        where it has a rule set, and as a low-fidelity recommendation otherwise
        (bank-loan options, marked with category_tag)."""
        ranked: List[Dict[str, Any]] = []
        for scheme in store.SCHEMES:
            rules = scheme.get("eligibility_rules", [])
            if rules:
                ev = RuleEngine().evaluate_rules(applicant, rules)
                ranked.append({"scheme": scheme, "evaluation": ev})
            else:
                ranked.append({"scheme": scheme, "evaluation": _bank_evaluation(scheme)})
        status_order = {"eligible": 0, "needs_more_information": 1, "not_currently_eligible": 2}
        ranked.sort(
            key=lambda item: (
                status_order.get(item["evaluation"]["status"], 3),
                -(item["evaluation"].get("passed_required", 0)
                  / max(item["evaluation"].get("total_required", 1), 1)
                  + item["evaluation"].get("passed_optional", 0) * 0.05),
            ),
        )
        return ranked

    def _rank_government_schemes(self, applicant: Dict[str, Any]) -> List[Dict[str, Any]]:
        ranked = self._all_ranked_schemes(applicant)
        return [item for item in ranked if item["scheme"].get("eligibility_rules")]

    # ------------------------------------------------------------------
    def run_check(
        self,
        applicant: Dict[str, Any],
        profile_sources: Optional[Dict[str, str]] = None,
        document_states: Optional[Dict[str, bool]] = None,
    ) -> Dict[str, Any]:
        """Run the full eligibility pipeline for one confirmed profile."""
        ranked = self._rank_government_schemes(applicant)

        if not ranked:
            return self._empty_catalogue_result(applicant)

        best = ranked[0]
        best_ev = best["evaluation"]
        explanation = self.explainer.generate(best["scheme"], best_ev)
        pathway = self.pathway.assemble(best["scheme"], applicant, document_states)

        others: List[Dict[str, Any]] = []
        for item in ranked[1:]:
            ev = item["evaluation"]
            others.append({
                "id": item["scheme"]["id"],
                "name": item["scheme"]["name"],
                "status": ev["status"],
                "passed_required": ev.get("passed_required", 0),
                "total_required": ev.get("total_required", 0),
                "gap_note": self._gap_note(ev),
            })

        all_ranked = self._all_ranked_schemes(applicant)
        comparison = self.comparator.build(all_ranked)

        result = {
            "result_id": store.new_id(),
            "trust_statement": TRUST_STATEMENT,
            "disclaimer": store.DISCLAIMER,
            "status": best_ev["status"],
            "scheme": {
                "id": best["scheme"]["id"],
                "code": best["scheme"]["code"],
                "name": best["scheme"]["name"],
                "headline": best["scheme"].get("headline", ""),
                "description": best["scheme"]["description"],
                "data_label": best["scheme"]["data_label"],
                "category_tag": best["scheme"].get("category_tag", ""),
                "authority": best["scheme"].get("authority", ""),
                "official_reference": best["scheme"].get("official_reference"),
                "why_good_fit_note": best["scheme"].get("why_good_fit_note", ""),
            },
            "summary": explanation["summary"],
            "why_match": explanation["why_match"],
            "eligibility_checks": best_ev["checks"],
            "missing_fields": best_ev.get("missing_fields", []),
            "failed_fields": best_ev.get("failed_fields", []),
            "financial_pathway": pathway["financial_pathway"],
            "documents": pathway["documents"],
            "next_step": pathway["next_step"],
            "other_schemes": others,
            "scheme_comparison": comparison["comparison"],
            "overview_graph": comparison["overview"],
            "profile_sources": profile_sources or {},
            "applicant_snapshot": {
                k: applicant.get(k)
                for k in (
                    "name", "age", "location", "category", "income",
                    "business_type", "business_stage", "sector",
                    "business_status", "funding_need", "funding_purpose",
                    "financing_type",
                )
            },
            "metadata": {
                "data_label": store.DATA_LABEL,
                "evaluated_at": store.utc_now_iso(),
                "engine": "deterministic_rule_engine",
            },
        }
        store.save_result(result)
        return result

    # ------------------------------------------------------------------
    def _gap_note(self, ev: Dict[str, Any]) -> str:
        if ev["status"] == "eligible":
            return "You also satisfy this scheme's required conditions."
        if ev["status"] == "needs_more_information":
            missing = ", ".join(ev.get("missing_fields", [])[:2]).replace("_", " ")
            return f"Add {missing} to be assessed."        failed = ", ".join(ev.get("failed_fields", [])[:2]).replace("_", " ")
        return f"Currently differs on: {failed}."


    def _bank_evaluation(scheme: Dict[str, Any]) -> Dict[str, Any]:        """Low-fidelity recommendation evaluation for bank-loan options.

        Banks are NOT decided by the rule engine; each is represented as a
        contextual suggestion derived from the applicant's funding need and
        business stage, plus the bank's own published product positioning.
        """
        return {
            "status": scheme.get("status", "bank_suggestion"),
            "checks": [],
            "failed_fields": [],
            "missing_fields": [],
            "passed_required": 0,
            "total_required": 0,
            "passed_optional": 0,
            "total_optional": 0,
        }

    def _bank_evaluation(scheme: Dict[str, Any]) -> Dict[str, Any]:    """Low-fidelity recommendation evaluation for bank-loan options.

    Banks are NOT decided by the rule engine; each is represented as a
    contextual suggestion derived from the applicant's funding need and
    business stage, plus the bank's own published product positioning.
    """
    return {
    def _bank_evaluation(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """Low-fidelity recommendation evaluation for bank-loan options.

    Banks are NOT decided by the rule engine; each is represented as a
    contextual suggestion derived from the applicant's funding need and
    business stage, plus the bank's own published product positioning.
    """
    return {def _bank_evaluation(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """Low-fidelity recommendation evaluation for bank-loan options.

    Banks are NOT decided by the rule engine; each is represented as a
    contextual suggestion derived from the applicant's funding need and
    business stage, plus the bank's own published product positioning.
    """
    return {
        "status": scheme.get("status", "bank_suggestion"),
        "checks": [],
        "failed_fields": [],
        "missing_fields": [],
        "passed_required": 0,
        "total_required": 0,
        "passed_optional": 0,
        "total_optional": 0,
    }


    def _empty_catalogue_result(self, applicant: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "result_id": store.new_id(),
            "trust_statement": TRUST_STATEMENT,
            "disclaimer": store.DISCLAIMER,
            "status": "no_match",
            "scheme": {
                "id": 0,
                "code": None,
                "name": "No matching scheme",
                "description": "No schemes in the current catalogue apply to this profile.",
                "data_label": store.DATA_LABEL,
            },
            "summary": "None of the available prototype schemes matched this profile. Review your information and try again.",
            "why_match": [],
            "eligibility_checks": [],
            "missing_fields": [],
            "failed_fields": [],
            "financial_pathway": {},
            "documents": {"ready_count": 0, "total_count": 0, "items": []},
            "next_step": {},
            "other_schemes": [],
            "scheme_comparison": {"rows": [], "note": "No schemes were available to compare."},
            "overview_graph": {"has_data": False},
            "profile_sources": {},
            "applicant_snapshot": applicant,
            "metadata": {"data_label": store.DATA_LABEL, "evaluated_at": store.utc_now_iso()},
        }
        store.save_result(result)
        return result
