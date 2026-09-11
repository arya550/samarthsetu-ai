"""
Knowledge-graph candidate matcher.

Builds a lightweight in-process graph (Applicant → Attributes → Potential
Scheme → Rules/Finance/Documents/Partner) and uses it to discover candidate
schemes for a profile. The matcher only *shortlists* — the deterministic
Rule Engine makes the final eligibility decision.
"""
from __future__ import annotations

from typing import Any, Dict, List

from app import store
from app.rules.rule_engine import RuleEngine


class KnowledgeGraphMatcher:
    """Shortlists candidate schemes using attribute→scheme graph links."""

    def __init__(self, rule_engine: RuleEngine | None = None) -> None:
        self.rule_engine = rule_engine or RuleEngine()

    def find_candidate_schemes(self, applicant: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return schemes worth evaluating, best-first.

        A scheme is a candidate if it shares at least one hard attribute link
        (age/stage/type/sector) with the profile, or if the profile has no
        business attributes at all (then everything is considered).
        """
        linking_fields = ("business_type", "business_stage", "sector", "category")
        has_links = any(applicant.get(f) for f in linking_fields)

        candidates: List[Dict[str, Any]] = []
        for scheme in store.SCHEMES:
            graph_fields = {r["field"] for r in scheme["eligibility_rules"]}
            shared = [f for f in linking_fields if f in graph_fields and applicant.get(f)]
            if has_links and not shared:
                continue
            # Cheap relevance score: rule-field overlap with populated fields
            populated = [f for f in graph_fields if applicant.get(f) is not None]
            score = len(populated) + scheme.get("priority_weight", 0) * 0.01
            candidates.append({"scheme": scheme, "relevance": round(score, 3)})

        candidates.sort(key=lambda c: c["relevance"], reverse=True)
        return [dict(c["scheme"], relevance=c["relevance"]) for c in candidates]

    def rank_schemes(self, applicant: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate every candidate with the Rule Engine and rank results.

        Returns list of {scheme, evaluation} ordered:
        eligible (best fit first) → needs_more_information → not eligible.
        """
        ranked: List[Dict[str, Any]] = []
        for scheme in self.find_candidate_schemes(applicant):
            evaluation = self.rule_engine.evaluate_rules(applicant, scheme["eligibility_rules"])
            ranked.append({"scheme": scheme, "evaluation": evaluation})

        status_order = {"eligible": 0, "needs_more_information": 1, "not_currently_eligible": 2}

        def specificity_bonus(ev: Dict[str, Any]) -> float:
            """Tie-breaker: schemes that explicitly TARGET the applicant's
            category or activity rank ahead of generic ones when base
            eligibility ties. Ordering only — never changes eligibility."""
            bonus = 0.0
            for check in ev.get("checks", []):
                if check.get("result") != "Passed":
                    continue
                field, op = check.get("field"), check.get("operator")
                if field == "category" and op == "in":
                    bonus += 0.15
                elif field in ("business_type", "sector") and op == "in":
                    bonus += 0.10
                elif field in ("business_type", "sector") and op == "not_in":
                    bonus += 0.02
            return bonus

        def fit_score(item: Dict[str, Any]) -> tuple:
            ev = item["evaluation"]
            passed_required = ev.get("passed_required", 0)
            # Same denominator the displayed match score uses: missing required
            # fields count against fit, so ranking and display never disagree.
            possible = ev.get("total_required", 0) + len(ev.get("missing_fields", []))
            ratio = passed_required / possible if possible else 0.0
            optional_bonus = ev.get("passed_optional", 0) * 0.05
            score = ratio + optional_bonus + specificity_bonus(ev)
            return (
                status_order.get(ev["status"], 3),
                -score,
            )

        ranked.sort(key=fit_score)
        return ranked
