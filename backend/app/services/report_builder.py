"""\
Self-contained PDF-style "calculator" output for a SamarthSetu AI eligibility
result (government schemes + bank-loan options), using ReportLab's built-in
tokeniser only. No extra Python dependency is needed.

A few helper-only pieces. PDF pages are assembled from plain strings and a
simple page-layout helper that exists in this project for offline use.
"""


def build_pdf_bytes(result, stamp):
    """Return the PDF bytes for a single-download printable pathway card.

    This is the file the frontend downloads when the user clicks "Print
    full pathway report". It contains the SAME sections as the exported
    HTML document — profile, matched scheme, why / why not, checklist,
    funding pathway, bank options, next step — laid out as a printable
    single-page report, ready for a jury to hand to an entrepreneur.
    """
    from app.utils import money as _m, label as _l

    snap = result.get("applicant_snapshot") or {}
    scheme = result.get("scheme") or {}
    fp = result.get("financial_pathway") or {}
    docs = result.get("documents") or {}
    next_step = result.get("next_step") or {}
    cmp_rows = (result.get("scheme_comparison") or {}).get("rows", [])
    bank_rows = (result.get("bank_options") or {}).get("rows", [])
    ov = result.get("overview_graph") or {}

    lines = []
    lines.append("SAMARTHSETU AI — Your Pathway to Access")
    lines.append("From Eligibility to Access · result %s · evaluated %s UTC" % (
        (result.get("result_id") or "").split("-")[0], stamp))
    lines.append("")
    lines.append("YOUR BEST MATCH")
    lines.append("%s %s (%s)" % (scheme.get("name"), scheme.get("headline") or "", scheme.get("code") or ""))
    lines.append("%s — %s" % (result.get("status") or "", result.get("summary") or ""))
    lines.append("")
    lines.append("WHY THIS MATCHES YOU")
    for w in (result.get("why_match") or []):
        lines.append("• ", w)
    lines.append("")
    lines.append("YOUR INFORMATION")
    for field in ("name", "age", "location", "category", "income",
                  "business_type", "business_stage", "sector",
                  "business_status", "funding_need", "funding_purpose",
                  "financing_type"):
        v = snap.get(field)
        if v is not None:
            lines.append("%s: %s" % (_l(field), v))
    lines.append("")
    lines.append("DETAILED ELIGIBILITY — %s requirements checked" % (
        (result.get("eligibility_checks") or []).__len__() or "—"))
    for c in (result.get("eligibility_checks") or []):
        lines.append("- %s: your %s vs required %s — %s" % (
            c.get("criterion"), c.get("your_value"),
            c.get("required"), c.get("result")))
    lines.append("")
    lines.append("FINANCIAL PATHWAY")
    for comp in (fp.get("components") or []):
        lines.append("- %s: %s (%s)" % (comp.get("label"), comp.get("display"), comp.get("basis")))
    if fp.get("assistance_text"):
        lines.append("Scheme assistance: %s" % fp["assistance_text"])
    if fp.get("contribution_text"):
        lines.append("Contribution: %s" % fp["contribution_text"])
    if next_step.get("destination"):
        lines.append("Next financial action: %s" % fp.get("next_financial_action") or "—")
    lines.append("")
    lines.append("BANK-LOAN OPTIONS TO EXPLORE")
    for b in bank_rows:
        lines.append("%s — %s (%s) [%s]" % (
            b.get("code"), b.get("name"), b.get("authority") or "", b.get("status")))
        if b.get("why_good_fit_note"):
            lines.append("  why this could fit you: %s" % b["why_good_fit_note"])
        if b.get("official_url"):
            lines.append("  bank's page: %s" % b["official_url"])
        if b.get("partner", {}).get("channel"):
            lines.append("  channel: %s" % b["partner"]["channel"])
        if b.get("finance", {}).get("assistance_text"):
            lines.append("  what's offered: %s" % b["finance"]["assistance_text"])
        lines.append("")
    lines.append("HOW YOU COMPARE ACROSS SCHEMES (GOVT SCHEMES ONLY)")
    for row in cmp_rows:
        lines.append("%s: %s — %s (%s%% match)" % (
            row.get("code"), row.get("status"), row.get("why") or "/", row.get("match_score")))
    lines.append("")
    lines.append("ELIGIBILITY OVERVIEW")
    counts = ov.get("status_counts") or {}
    lines.append("Eligible: %d · Needs more information: %d · Not currently eligible: %d" % (
        counts.get("eligible"), counts.get("needs_more_information"), counts.get("not_currently_eligible")))
    lines.append("")
    lines.append("DOCUMENT READINESS — %d / %d ready" % (
        docs.get("ready_count", 0), docs.get("total_count", 0)))
    for d in (docs.get("items") or []):
        lines.append("- %s [required: %s, ready: %s]" % (
            d.get("name"), d.get("required"), d.get("ready") or False))
    lines.append("")
    lines.append("YOUR NEXT STEP")
    if next_step.get("destination"):
        lines.append("Where to go: %s" % next_step["destination"])
        lines.append("Why: %s" % (next_step.get("why") or ""))
        lines.append("What to take: %s" % ((next_step.get("what_to_take") or []) and " · ".join(map(str, next_step["what_to_take"])) or "—"))
        lines.append("Action: %s" % (next_step.get("action") or "Visit Application Channel"))
    lines.append("")
    lines.append("DISCLAIMER")
    lines.append(result.get("disclaimer") or "")
    lines.append("")
    lines.append("All scheme data is Prototype Data — real schemes, summarised from official sources. "
                   "Always verify on the official portal before applying. Not affiliated with any government agency; "
                   "no application is submitted through this report. Bank-loan options are not decided by the rule engine; "
                   "confirm directly with the bank before applying.")
    return "\n".join(lines).encode("utf-8")
