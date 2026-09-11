"""
Explanation Generator — turns structured Rule Engine output into plain language.

This is the "AI explains the fit" layer. It only rewords the deterministic
result; it can never change, add or remove eligibility conditions.
"""
from __future__ import annotations

from typing import Any, Dict, List

from app import store
from app.utils import format_field_value

TEMPLATE_REASONS = {
    "age": "Your age ({value}) is within the scheme's supported age range.",
    "business_stage": "Your business stage ({value}) matches the stages this scheme supports.",
    "business_type": "Your business type ({value}) is covered by this scheme.",
    "category": "Your category ({value}) is among the communities this scheme prioritises.",
    "funding_need": "Your funding need ({value}) fits the scheme's supported range.",
    "funding_purpose": "Your stated purpose ({value}) is an eligible use of funds here.",
    "financing_type": "The assistance style ({value}) aligns with how this scheme delivers support.",
    "sector": "Your sector ({value}) is a focus sector for this scheme.",
}

TEMPLATE_MISSING = {
    "age": "your age",
    "location": "your location",
    "category": "your category / community",
    "income": "your annual income",
    "business_type": "your business type",
    "business_stage": "your business stage",
    "sector": "your sector",
    "funding_need": "your funding requirement",
    "funding_purpose": "your funding purpose",
    "financing_type": "your financing preference",
}


class ExplanationGenerator:
    def generate(self, scheme: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
        status = evaluation["status"]
        summary = self._summary(scheme["name"], status, evaluation)
        reasons = self._reasons(status, evaluation)
        return {"summary": summary, "why_match": reasons}

    # ------------------------------------------------------------------
    def _summary(self, scheme_name: str, status: str, evaluation: Dict[str, Any]) -> str:
        if status == "eligible":
            return (
                f"Based on the information you provided, the Rule Engine found that you "
                f"satisfy the eligibility conditions of {scheme_name}."
            )
        if status == "not_currently_eligible":
            failed = evaluation.get("failed_fields", [])
            if failed:
                first = ", ".join(TEMPLATE_MISSING.get(f, f.replace("_", " ")) for f in failed[:2])
                return (
                    f"You do not currently meet the conditions for {scheme_name} — "
                    f"mainly {first}. The detailed check below shows exactly what differs."
                )
            return f"You do not currently meet the conditions for {scheme_name}."
        missing = evaluation.get("missing_fields", [])
        if missing:
            first = ", ".join(TEMPLATE_MISSING.get(f, f.replace("_", " ")) for f in missing[:3])
            return (
                f"The Rule Engine needs a few more details before it can decide — "
                f"mainly {first}. Add them and check again."
            )
        return f"More information is needed to assess {scheme_name}."

    def _reasons(self, status: str, evaluation: Dict[str, Any]) -> List[str]:
        checks = evaluation.get("checks", [])
        reasons: List[str] = []

        if status == "eligible":
            for check in checks:
                if check["result"] == "Passed" and check["field"] in TEMPLATE_REASONS:
                    reasons.append(
                        TEMPLATE_REASONS[check["field"]].format(value=check["your_value"])
                    )
                if len(reasons) >= 5:
                    break
            if not reasons:
                reasons.append("Your profile satisfies all required eligibility conditions of this scheme.")

        elif status == "not_currently_eligible":
            for check in checks:
                if check["result"] == "Failed":
                    reasons.append(
                        f"Your {check['criterion'].lower()} is {check['your_value']}, "
                        f"but this scheme requires {check['required']}."
                    )
                if len(reasons) >= 4:
                    break

        else:  # needs_more_information
            for field in evaluation.get("missing_fields", [])[:4]:
                label = TEMPLATE_MISSING.get(field, field.replace("_", " "))
                reason = f"We couldn't assess {label} because it wasn't provided."
                rule = self._rule_why(checks, field)
                if rule:
                    reason += f" It matters because {rule[0].lower() + rule[1:]}" if not rule.endswith(".") else f" It matters because {rule}"
                reasons.append(reason)

        return reasons

    def _rule_why(self, checks: List[Dict[str, Any]], field: str) -> str | None:
        for check in checks:
            if check["field"] == field and check.get("why_it_matters"):
                return check["why_it_matters"]
        return None
