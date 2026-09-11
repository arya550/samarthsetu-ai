"""\
Comparison & Overview Builder.

Builds three result sections from the SAME ranked evaluations the Rule Engine
already produced — no new eligibility logic lives here:

  1. scheme_comparison — government schemes side by side: qualify or not,
     why, match score, official portal.
  2. bank_options      — HDFC and Axis as grounded recommendations,
     each with the bank's own "why good fit" note and bank's page link.
  3. overview_graph    — match-score bar data + status counts for the
     government schemes.

Everything shown is derived from structured rule-engine output and scheme data.
"""


class ComparisonBuilder:
    """Build comparison + bank-options + overview sections from ranked eval output.

    class-level note is injected here rather than imported from the service so the
    comparison layer is self-contained and easy to read/change independently.
    """

    BANK_OPTIONS_NOTE = (
        "Bank-loan options are grounded recommendations from each bank's published "
        "product pages — not decided by the rule engine. Eligibility, documents, "
        "rate and tenure are decided by the bank per application. Confirm on the "
        "bank's website before applying."
    )

    def build(self, ranked):
        comparison_rows = [self._comparison_row(item) for item in ranked]
        government_rows = []
        bank_rows = []
        for item in comparison_rows:
            tag = item.get("category_tag", "")
            if tag == "bank_loan_option":
                bank_rows.append(item)
            else:
                government_rows.append(item)

        overview = self._overview(ranked, government_rows)
        return {
            "comparison": {
                "rows": government_rows,
                "note": (
                    "Every government scheme was assessed with the same rule engine "
                    "and the same profile. Verify details on the official portal before "
                    "applying."
                ),
            },
            "bank_options": {
                "rows": bank_rows,
                "note": self.BANK_OPTIONS_NOTE,
            },
            "overview": overview,
        }

    # ------------------------------------------------------------------
    def _comparison_row(self, item):
        scheme, ev = item["scheme"], item["evaluation"]
        status = ev["status"]

        total_required = ev.get("total_required", 0)
        missing = ev.get("missing_fields", [])
        possible = total_required + len(missing)
        score = round(100 * ev.get("passed_required", 0) / possible) if possible else 0

        gaps = []
        for check in ev.get("checks", []):
            if check["result"] in ("Failed", "Unknown"):
                gaps.append({
                    "criterion": check["criterion"],
                    "your_value": check["your_value"],
                    "required": check["required"],
                    "result": check["result"],
                })
            if len(gaps) >= 3:
                break

        if status == "eligible":
            why = scheme.get("best_for") or "You satisfy every required condition of this scheme."
            why_kind = "qualified"
        elif status == "needs_more_information":
            labels = ", ".join(m.replace("_", " ") for m in missing[:2]) or "some details"
            why = f"Cannot be assessed yet — add {labels} and check again."
            why_kind = "missing_info"
        else:
            first = gaps[0] if gaps else None
            if first:
                why = (
                    f"Not currently eligible — your {first['criterion'].lower()} is "
                    f"{first['your_value']}, but the scheme requires {first['required']}."
                )
            else:
                why = "Not currently eligible under this scheme's rules."
            why_kind = "not_eligible"

        return {
            "scheme_id": scheme["id"],
            "code": scheme["code"],
            "name": scheme["name"],
            "authority": scheme.get("authority", ""),
            "category_tag": scheme.get("category_tag", ""),
            "headline": scheme.get("headline", ""),
            "best_for": scheme.get("best_for", ""),
            "status": status,
            "match_score": score,
            "passed_required": ev.get("passed_required", 0),
            "total_required": total_required,
            "missing_count": len(missing),
            "why_kind": why_kind,
            "why": why,
            "top_gaps": gaps,
            "official_url": (scheme.get("official_reference") or {}).get("url"),
        }

    # ------------------------------------------------------------------
    def _overview(self, ranked, government_rows):
        if not ranked:
            return {"has_data": False}

        best_scheme = ranked[0]["scheme"]
        best_ev = ranked[0]["evaluation"]

        match_scores = [
            {
                "code": item["scheme"]["code"],
                "name": item["scheme"]["name"],
                "status": item["evaluation"]["status"],
                "score": self._comparison_row(item)["match_score"],
            }
            for item in ranked
        ]

        return {
            "has_data": True,
            "applicant_label": "Your profile",
            "best_match": {
                "code": best_scheme["code"],
                "name": best_scheme["name"],
                "status": best_ev["status"],
                "authority": best_scheme.get("authority", ""),
            },
            "match_scores": match_scores,
            "status_counts": self._status_counts(government_rows),
            "note": (
                "Overview generated from the same rule-engine assessments shown "
                "below — the graph visualises results; it never decides eligibility."
            ),
        }

    def _status_counts(self, ranked):
        counts = {"eligible": 0, "needs_more_information": 0, "not_currently_eligible": 0}
        for item in ranked:
            status = item["evaluation"]["status"]
            if status in counts:
                counts[status] += 1
        return counts
