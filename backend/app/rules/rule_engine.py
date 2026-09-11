"""
Deterministic Rule Engine — the single authority for eligibility.

Rules come from seeded scheme data; nothing here is scheme-specific logic.
AI never determines or modifies eligibility — it only explains the structured
result this engine produces.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from app.utils import format_money, format_field_value


class RuleEngine:
    OPERATORS = {
        "equals", "not_equals", "greater_than", "greater_than_or_equal",
        "less_than", "less_than_or_equal", "between", "in", "not_in",
    }

    def evaluate_rules(
        self,
        applicant: Dict[str, Any],
        rules: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Evaluate every rule for one scheme against the applicant profile.

        Returns: {status, checks, failed_fields, missing_fields, passed_required,
                  total_required, passed_optional, total_optional}
        status ∈ 'eligible' | 'not_currently_eligible' | 'needs_more_information'
        """
        checks: List[Dict[str, Any]] = []
        failed_fields: List[str] = []
        missing_fields: List[str] = []
        passed_required = total_required = 0
        passed_optional = total_optional = 0

        for rule in rules:
            field = rule.get("field", "")
            operator = rule.get("operator", "")
            expected = rule.get("expected_value")
            required = bool(rule.get("required", True))
            criterion = rule.get("criterion") or field.replace("_", " ").title()
            why = rule.get("why_it_matters", "")

            value = applicant.get(field)
            is_missing = value is None or value == "" or value == []

            if is_missing:
                if required:
                    missing_fields.append(field)
                    checks.append(self._check(criterion, field, None, expected, operator, "Unknown", why))
                # Optional rules with no value are silently skipped.
                continue

            passed = self._evaluate_single(value, operator, expected)

            if required:
                total_required += 1
                if passed:
                    passed_required += 1
                else:
                    failed_fields.append(field)
            else:
                total_optional += 1
                if passed:
                    passed_optional += 1

            checks.append(self._check(
                criterion, field, value, expected, operator,
                "Passed" if passed else "Failed", why,
            ))

        if missing_fields:
            status = "needs_more_information"
        elif failed_fields:
            status = "not_currently_eligible"
        else:
            status = "eligible"

        return {
            "status": status,
            "checks": checks,
            "failed_fields": failed_fields,
            "missing_fields": missing_fields,
            "passed_required": passed_required,
            "total_required": total_required,
            "passed_optional": passed_optional,
            "total_optional": total_optional,
        }

    # ------------------------------------------------------------------
    def _check(
        self, criterion: str, field: str, value: Any, expected: Any,
        operator: str, result: str, why: str,
    ) -> Dict[str, Any]:
        if result == "Unknown":
            your_value = "Not provided"
        else:
            your_value = format_field_value(field, value)
        return {
            "criterion": criterion,
            "field": field,
            "operator": operator,
            "your_value": your_value,
            "required": self._format_expected(field, operator, expected),
            "result": result,
            "why_it_matters": why,
        }

    def _evaluate_single(self, value: Any, operator: str, expected: Any) -> bool:
        handler = getattr(self, f"_op_{operator}", None)
        if handler is None:
            return False
        try:
            return bool(handler(value, expected))
        except (TypeError, ValueError):
            return False

    def _as_number(self, value: Any) -> Optional[float]:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip()
        text = re.sub(r"[₹,\s]", "", text)
        try:
            return float(text)
        except ValueError:
            return None

    def _as_list(self, expected: Any) -> List[Any]:
        if isinstance(expected, (list, tuple, set)):
            return list(expected)
        return [item.strip() for item in str(expected).split(",") if item.strip()]

    def _as_range(self, expected: Any) -> Optional[tuple]:
        if isinstance(expected, (list, tuple)) and len(expected) == 2:
            lo, hi = self._as_number(expected[0]), self._as_number(expected[1])
        else:
            parts = str(expected).split(",")
            if len(parts) != 2:
                return None
            lo, hi = self._as_number(parts[0]), self._as_number(parts[1])
        if lo is None or hi is None:
            return None
        return (min(lo, hi), max(lo, hi))

    # --- operators -----------------------------------------------------
    def _op_equals(self, value, expected):
        return str(value).strip().lower() == str(expected).strip().lower()

    def _op_not_equals(self, value, expected):
        return not self._op_equals(value, expected)

    def _op_greater_than(self, value, expected):
        num = self._as_number(value)
        return num is not None and num > float(expected)

    def _op_greater_than_or_equal(self, value, expected):
        num = self._as_number(value)
        return num is not None and num >= float(expected)

    def _op_less_than(self, value, expected):
        num = self._as_number(value)
        return num is not None and num < float(expected)

    def _op_less_than_or_equal(self, value, expected):
        num = self._as_number(value)
        return num is not None and num <= float(expected)

    def _op_between(self, value, expected):
        rng = self._as_range(expected)
        num = self._as_number(value)
        return rng is not None and num is not None and rng[0] <= num <= rng[1]

    def _op_in(self, value, expected):
        options = [str(o).strip().lower() for o in self._as_list(expected)]
        return str(value).strip().lower() in options

    def _op_not_in(self, value, expected):
        return not self._op_in(value, expected)

    # --- display --------------------------------------------------------
    def _format_expected(self, field: str, operator: str, expected: Any) -> str:
        def money(v: Any) -> str:
            num = self._as_number(v)
            return format_money(num) if num is not None else str(v)

        field_lower = str(field)
        # money-styled fields; age is numeric but formatted as a plain number
        numeric = field_lower in ("income", "annual_income", "funding_need")

        def fmt(v: Any) -> str:
            return money(v) if numeric and self._as_number(v) is not None else str(v)

        def fmt_list(items: List[Any]) -> str:
            return ", ".join(fmt(i) for i in items)

        if operator == "between":
            rng = self._as_range(expected)
            if rng and numeric:
                return f"{fmt(rng[0])} – {fmt(rng[1])}"
            return f"between {fmt(expected[0])} and {fmt(expected[1])}" if isinstance(expected, (list, tuple)) else f"between {expected}"
        if operator == "in":
            return f"one of: {fmt_list(self._as_list(expected))}"
        if operator == "not_in":
            return f"not one of: {fmt_list(self._as_list(expected))}"
        if operator == "equals":
            return f"= {fmt(expected)}"
        if operator == "not_equals":
            return f"≠ {fmt(expected)}"
        if operator in ("greater_than", "greater_than_or_equal"):
            return f"≥ {fmt(expected)}" if operator == "greater_than_or_equal" else f"> {fmt(expected)}"
        if operator in ("less_than", "less_than_or_equal"):
            return f"≤ {fmt(expected)}" if operator == "less_than_or_equal" else f"< {fmt(expected)}"
        return f"{operator} {expected}"
