"""Shared formatting helpers."""
from __future__ import annotations

import re
from typing import Any, Optional, Sequence

# ---------------------------------------------------------------------------
# Document categories — let one user mark (e.g. "Identity Proof (Aadhaar / PAN)")
# carry to equivalent documents in other schemes (e.g. "Identity Proof (KYC)").
# ---------------------------------------------------------------------------
_DOC_CATEGORY_PATTERNS = {
    "identity": ("identity", "aadhaar", "aadhar", "pan card", "kyc", "voter id"),
    "address": ("address", "residence", "utility bill"),
    "bank": ("bank",),
    "project_report": ("project report", "business plan"),
    "category_certificate": ("caste", "category certificate", "special category", "community certificate"),
    "registration": ("registration", "business proof", "shop establishment", "udyam", "fssai", "gst"),
    "quotation": ("quotation", "price quote"),
}


def doc_category(name: str) -> str:
    lowered = (name or "").lower()
    for category, patterns in _DOC_CATEGORY_PATTERNS.items():
        if any(p in lowered for p in patterns):
            return category
    return f"exact:{lowered}"


def doc_is_marked(doc_name: str, marked_names: Sequence[str]) -> bool:
    """True if the user marked this document (same category or exact name)."""
    target = doc_category(doc_name)
    for marked in marked_names or ():
        if marked == doc_name or doc_category(marked) == target:
            return True
    return False


def format_money(amount: Optional[float]) -> str:
    """Format an INR amount in Indian style, e.g. ₹5,00,000 (₹5 lakh)."""
    if amount is None:
        return "—"
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return str(amount)
    if amount >= 1_00_00_000:
        return f"₹{amount / 1_00_00_000:g} crore"
    if amount >= 1_00_000:
        return f"₹{amount / 1_00_000:g} lakh"
    if amount >= 1_000:
        return f"₹{amount:,.0f}"
    return f"₹{amount:g}"


def format_inr_full(amount: Optional[float]) -> str:
    """Format with Indian digit grouping, e.g. ₹5,00,000."""
    if amount is None:
        return "—"
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return str(amount)
    s = f"{amount:,.0f}".replace(",", "_").replace(".", ",").replace("_", ",")
    # The two swaps above only give western grouping; do proper Indian grouping:
    s = f"{int(amount):d}"
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return f"₹{s}"


VALUE_LABELS = {
    # categories
    "general": "General",
    "sc": "SC (Scheduled Caste)",
    "st": "ST (Scheduled Tribe)",
    "obc": "OBC",
    "minority": "Minority",
    "women": "Woman entrepreneur",
    # business stages
    "early_stage": "Early-stage",
    "existing": "Existing business",
    # business types / sectors
    "food_processing": "Food processing",
    "manufacturing": "Manufacturing",
    "services": "Services",
    "retail": "Retail / shop",
    "trading": "Trading",
    "agriculture": "Agriculture / farm",
    "technology": "Technology",
    # funding purposes
    "equipment": "Equipment / machinery",
    "machinery": "Equipment / machinery",
    "working_capital": "Working capital",
    "setup": "Business setup",
    "expansion": "Expansion",
    "marketing": "Marketing",
    # financing preferences
    "loan": "Loan",
    "grant": "Grant",
    "subsidy": "Subsidy",
    "mixed": "Loan + subsidy mix",
    "any": "No preference",
    # business status
    "registered": "Registered",
    "not_registered": "Not yet registered",
}

FIELD_LABELS = {
    "name": "Name",
    "age": "Age",
    "location": "Location",
    "category": "Category / community",
    "income": "Annual income",
    "business_type": "Business type",
    "business_stage": "Business stage",
    "sector": "Sector",
    "business_status": "Business status",
    "funding_need": "Funding need",
    "funding_purpose": "Funding purpose",
    "financing_type": "Financing preference",
    "natural_language_description": "In your own words",
}


def format_field_value(field: str, value: Any) -> str:
    """Human-readable value for a profile/rule field."""
    if value is None:
        return "Not provided"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if field in ("funding_need", "income"):
        return format_money(value)
    if isinstance(value, (int, float)):
        return f"{value:,g}"
    text = str(value)
    return VALUE_LABELS.get(text, text.replace("_", " ").title() if "_" in text else text.title())
