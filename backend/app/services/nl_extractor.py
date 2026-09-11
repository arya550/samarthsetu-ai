"""
Natural-language profile extractor.

If an LLM API key is configured (OPENAI_API_KEY), it may be used for
extraction. Otherwise a deterministic rule-based extractor runs so the
prototype works offline. The extractor NEVER invents eligibility conditions —
it only fills profile fields, which the user confirms in the UI before any
eligibility check runs.
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional, Tuple

WORDS: Dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "thousand": 1_000, "lakhs": 1_00_000, "lakh": 1_00_000, "lac": 1_00_000,
    "crores": 1_00_00_000, "crore": 1_00_00_000, "cr": 1_00_00_000,
}

FIELDS = [
    "age", "location", "category", "income", "business_type",
    "business_stage", "sector", "funding_need", "funding_purpose",
    "financing_type",
]

CITIES = [
    "new delhi", "ahmedabad", "mumbai", "delhi", "bengaluru", "bangalore",
    "chennai", "kolkata", "pune", "hyderabad", "jaipur", "surat", "lucknow",
    "indore", "nagpur", "patna", "bhopal", "vadodara", "rajkot", "kanpur",
]

BUSINESS_TYPE_PATTERNS = [
    (r"food[- ]?process|food business|food (?:unit|industry)|packaged food|fssai", "food_processing"),
    (r"dairy product|papad|bakery|snack", "food_processing"),
    (r"manufactur\w*|factory|workshop|fabricat\w*", "manufacturing"),
    (r"service|salon|repair|tailor\w*|consultanc\w*|tuition|coaching", "services"),
    (r"retail|shop|store|kirana|showroom", "retail"),
    (r"trad\w*|wholesal\w*|distribut\w*", "trading"),
    (r"\bfarm\w*|agri\w*|poultry", "agriculture"),
    (r"software|startup|app|website|\btech\b", "technology"),
]

PURPOSE_PATTERNS = [
    (r"equipment|machiner\w*|\bmachine\b", "equipment"),
    (r"working capital|operations|inventory|raw material", "working_capital"),
    (r"expand\w*|grow\w*|scal\w*|second (?:unit|branch)", "expansion"),
    (r"set[- ]?up|setup|start[- ]?up costs|new unit", "setup"),
    (r"market\w*|brand\w*|advertis\w*", "marketing"),
]

CATEGORY_PATTERNS = [
    (r"\bsc\b|scheduled caste", "sc"),
    (r"\bst\b|scheduled tribe", "st"),
    (r"\bobc\b", "obc"),
    (r"minorit\w*|muslim|christian|sikh|buddhist|parsi|jain", "minority"),
    (r"woman|women|female|lady", "women"),
    (r"general categ\w*|\bgeneral\b", "general"),
]

UNIT_ALTS = r"lakh|lakhs|lac|crore|crores|cr|thousand|k\b"

# group1: digits, group2: unit after digits, group3: word number, group4: unit after word
AMOUNT_RE = re.compile(
    r"(?:₹|rs\.?|inr)?\s*"
    r"(?:(\d[\d,]*(?:\.\d+)?)\s*(lakh|lakhs|lac|crore|crores|cr|thousand|k\b)?"
    r"|(five|four|three|two|one|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty)"
    r"\s*(lakh|lakhs|lac|crore|crores|cr|thousand)?)\b",
    re.IGNORECASE,
)

INCOME_KW_RE = re.compile(r"\b(?:income|salary|turnover|earn(?:s|ing)?s?)\b", re.IGNORECASE)

MIN_PLAIN_AMOUNT = 5_000  # bare digits below this are ages/counts, not money


def _match_value(text: str, m: re.Match) -> Optional[float]:
    digits, unit_after_digits, word, unit_after_word = m.groups()
    if digits:
        value = float(digits.replace(",", ""))
        unit = (unit_after_digits or "").lower()
        if unit in WORDS:
            value *= WORDS[unit]
        elif unit == "k":
            value *= 1_000
        elif value < MIN_PLAIN_AMOUNT:
            return None  # e.g. an age — not a money amount
        return value
    if word:
        base = float(WORDS.get(word.lower(), 0))
        if base == 0:
            return None
        unit = (unit_after_word or "").lower()
        if unit:
            return base * WORDS.get(unit, 1)
        tail = text[m.end():m.end() + 20].lower()
        um = re.match(rf"\s*({UNIT_ALTS})", tail)
        if um:
            return base * WORDS[um.group(1).lower()]
    return None


def _extract_amount(text: str) -> Optional[float]:
    """Find the funding amount, ignoring numbers tied to income keywords."""
    income_spans = [(m.start(), m.end()) for m in INCOME_KW_RE.finditer(text)]
    best: Optional[float] = None
    for m in AMOUNT_RE.finditer(text):
        near_income = any(
            m.start() >= s - 3 and m.start() <= e + 25 for s, e in income_spans
        )
        if near_income:
            continue
        value = _match_value(text, m)
        if value and (best is None or value > best):
            best = value
    return best


class NLProfileExtractor:
    """Extracts structured profile fields from free text."""

    def __init__(self) -> None:
        self.use_llm = bool(os.getenv("OPENAI_API_KEY"))

    def extract_profile(self, description: str) -> Dict[str, Any]:
        text = f" {description.strip().lower()} "
        profile: Dict[str, Any] = {field: None for field in FIELDS}

        # Age: "28 years old", "age 28", "i am 28"
        m = re.search(r"(\d{2})\s*(?:years? old|yrs? old|age\b)", text)
        if not m:
            m = re.search(r"\bi am (\d{2})\b|\bage (?:is |of )?(\d{2})\b", text)
        if m:
            for g in m.groups():
                if g:
                    profile["age"] = int(g)
                    break

        # Location
        for city in CITIES:
            if city in text:
                profile["location"] = city.title()
                break

        # Category / community
        for pattern, value in CATEGORY_PATTERNS:
            if re.search(pattern, text):
                profile["category"] = value
                break

        # Income: "income ... 3 lakh", "earn(s) ... 400000"
        m = INCOME_KW_RE.search(text)
        if m:
            im = re.search(
                rf"[\w\s]{{0,25}}?(\d[\d,]*(?:\.\d+)?)\s*({UNIT_ALTS})?",
                text[m.end():m.end() + 40],
            )
            if im:
                amount = float(im.group(1).replace(",", ""))
                unit = (im.group(2) or "").lower()
                amount *= WORDS.get(unit, 1) if unit != "k" else 1_000
                profile["income"] = int(amount)

        # Business type + sector
        for pattern, value in BUSINESS_TYPE_PATTERNS:
            if re.search(pattern, text):
                profile["business_type"] = value
                profile["sector"] = value
                break

        # Business stage
        if re.search(r"start\w*|new business|new unit|plan\w* to (?:open|start)|greenfield", text):
            profile["business_stage"] = "early_stage"
        elif re.search(r"existing|been (?:running|operating)|running (?:a|my|for)|since \d{4}", text):
            profile["business_stage"] = "existing"

        # Funding need
        amount = _extract_amount(text)
        if amount:
            profile["funding_need"] = int(amount)

        # Funding purpose
        for pattern, value in PURPOSE_PATTERNS:
            if re.search(pattern, text):
                profile["funding_purpose"] = value
                break

        # Financing preference
        if re.search(r"grant|subsid\w*", text):
            profile["financing_type"] = "mixed" if re.search(r"loan", text) else "grant"
        elif re.search(r"loan|finance|credit", text):
            profile["financing_type"] = "loan"

        return profile

    def extract_with_confidence(self, description: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """Return (profile, sources) where sources maps field -> 'extracted'."""
        profile = self.extract_profile(description)
        sources = {k: "extracted" for k, v in profile.items() if v is not None}
        return profile, sources
