"""
SamarthSetu AI — data store for the prototype.

The catalogue contains five REAL government schemes (PMEGP, PMFME, PM MUDRA,
Stand-Up India, PM SVANidhi) plus two real bank-loan options (HDFC Bank Business
Loans and Axis Bank SME banking / MUDRA). Bank options are grounded recommendations
from each bank's published product pages or help pages — they are NOT evaluated
by the deterministic rule engine, and each carries a "why this fits you" note.

Facts are summarised from official scheme documents and bank pages (linked per
scheme) and clearly labelled as prototype summaries — they must be verified on
the official portals before applying. Eligibility results are persisted to a
local JSON file so History survives server restarts. A PostgreSQL backend can
replace this store later without touching the rule engine or API contracts.
"""
from __future__ import annotations

import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.utils import doc_is_marked

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")

DATA_LABEL = "Prototype Data — real schemes, summarised from official sources"

_lock = threading.Lock()


def _rule(
    field: str,
    operator: str,
    expected_value: Any,
    criterion: str,
    required: bool = True,
    why_it_matters: str = "",
) -> Dict[str, Any]:
    return {
        "field": field,
        "operator": operator,
        "expected_value": expected_value,
        "required": required,
        "criterion": criterion,
        "why_it_matters": why_it_matters,
    }


# ---------------------------------------------------------------------------
# Real schemes — government schemes + two real bank-loan options.
# ---------------------------------------------------------------------------
SCHEMES: List[Dict[str, Any]] = [
    # ---- Government schemes (5) ----
    {
        "id": 1,
        "code": "PMEGP",
        "name": "PMEGP — Prime Minister's Employment Generation Programme",
        "headline": "Bank loan + 15–35% margin-money subsidy for new micro units (project cost up to ₹50 lakh).",
        "best_for": "New micro units wanting a subsidy-backed bank loan.",
        "description": (
            "Central government credit-linked subsidy scheme implemented by the Khadi & Village "
            "Industries Commission (KVIC), Ministry of MSME, for setting up NEW micro enterprises "
            "in manufacturing, services and trading. Project cost caps: ₹50 lakh (manufacturing) "
            "and ₹20 lakh (service/trading). Summarised from official scheme documents — verify "
            "on the official portal before applying."
        ),
        "authority": "Ministry of MSME, Government of India (via KVIC/KVIB/DIC)",
        "category_tag": "central_government",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 3,
        "official_reference": {
            "label": "KVIC — official PMEGP portal & guidelines",
            "url": "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
        },
        "eligibility_rules": [
            _rule("age", "greater_than_or_equal", 18, "Age",
                  why_it_matters="Applicants must be adults (18+) to enter a PMEGP project agreement."),
            _rule("business_stage", "equals", "early_stage", "Business Stage",
                  why_it_matters="PMEGP funds NEW units only — existing units are served by other schemes."),
            _rule("business_type", "not_in", ["agriculture"], "Business Type",
                  why_it_matters="PMEGP covers non-farm sector activity; farm-sector activity has separate schemes."),
            _rule("funding_need", "between", [100000, 5000000], "Funding Need",
                  why_it_matters="Maximum project cost is ₹50 lakh (manufacturing) / ₹20 lakh (service & trading)."),
            _rule("financing_type", "in", ["loan", "subsidy", "mixed", "any"], "Financing Preference",
                  required=False,
                  why_it_matters="Assistance is delivered as a bank loan with a government margin-money subsidy."),
            _rule("funding_purpose", "in", ["equipment", "machinery", "working_capital", "setup"], "Funding Purpose",
                  required=False,
                  why_it_matters="The scheme funds productive assets and working capital for the new unit."),
        ],
        "finance": {
            "financing_type": "loan_with_subsidy",
            "assistance_text": (
                "Bank loan covering most of the project cost, with a government margin-money subsidy "
                "of 15–35% credited to the loan account (15% urban general; 25–35% for special "
                "categories and rural areas)."
            ),
            "contribution_text": "Own contribution of 10% of project cost (5% for special categories and rural areas).",
            "subsidy_rate_min": 0.15,
            "subsidy_rate_max": 0.35,
            "margin_rate": 0.10,
            "notes": "Subsidy is back-ended into the loan account after disbursement. Caps: ₹50 lakh project cost (manufacturing), ₹20 lakh (service/trading).",
        },
        "documents": [
            {"name": "Identity Proof (Aadhaar / PAN)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Project Report / Business Plan", "required": True},
            {"name": "Bank Account Details", "required": True},
            {"name": "Special Category Certificate (SC/ST/OBC/Minority/Woman)", "required": False},
            {"name": "Education Certificate (for larger projects)", "required": False},
        ],
        "partner": {
            "name": "KVIC / KVIB / District Industries Centre (DIC)",
            "channel": "Apply on the official PMEGP ePortal",
            "url": "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
            "notes": "Applications go through the PMEGP ePortal of the Khadi & Village Industries Commission; DICs help prepare the project report.",
        },
    },
    {
        "id": 2,
        "code": "PMFME",
        "name": "PMFME — PM Formalisation of Micro Food Processing Enterprises",
        "headline": "35% credit-linked subsidy (cap ₹10 lakh) for micro food-processing units.",
        "best_for": "Micro food-processing units — new or upgrading.",
        "description": (
            "Centrally sponsored scheme of the Ministry of Food Processing Industries (MoFPI) for "
            "individual micro food-processing units, FPOs, SHGs and producer cooperatives. Provides "
            "a credit-linked capital subsidy of 35% of eligible project cost, capped at ₹10 lakh per "
            "unit, for setting up or upgrading units, aligned with ODOP (One District One Product). "
            "Summarised from official scheme documents — verify on the official portal before applying."
        ),
        "authority": "Ministry of Food Processing Industries, Government of India",
        "category_tag": "centrally_sponsored",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 3,
        "official_reference": {
            "label": "MoFPI — official PMFME portal & guidelines",
            "url": "https://pmfme.mofpi.gov.in/",
        },
        "eligibility_rules": [
            _rule("age", "greater_than_or_equal", 18, "Age",
                  why_it_matters="Applicants must be adults to enter the bank loan and subsidy agreement."),
            _rule("business_type", "in", ["food_processing", "agriculture"], "Business Type",
                  why_it_matters="The scheme supports micro food-processing activity (including agri-linked food units)."),
            _rule("business_stage", "in", ["early_stage", "existing"], "Business Stage",
                  why_it_matters="Both new units and existing units upgrading their operations are covered."),
            _rule("funding_need", "between", [50000, 2000000], "Funding Need",
                  why_it_matters="The 35% subsidy applies to eligible project cost, capped at ₹10 lakh per unit."),
            _rule("financing_type", "in", ["loan", "subsidy", "mixed", "any"], "Financing Preference",
                  required=False,
                  why_it_matters="The subsidy is credit-linked — it comes attached to a bank loan."),
        ],
        "finance": {
            "financing_type": "loan_with_subsidy",
            "assistance_text": (
                "Credit-linked capital subsidy of 35% of eligible project cost, capped at ₹10 lakh per "
                "unit, delivered through a bank term loan."
            ),
            "contribution_text": "Beneficiary margin money as per bank norms (indicatively about 10%).",
            "subsidy_rate_min": 0.35,
            "subsidy_rate_max": 0.35,
            "margin_rate": 0.10,
            "notes": "Subsidy is released to the loan account after the unit is set up or upgraded. The scheme also supports FSSAI registration, branding and training.",
        },
        "documents": [
            {"name": "Identity Proof (Aadhaar / PAN)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Project Report / Business Plan", "required": True},
            {"name": "Bank Account Details", "required": True},
            {"name": "Udyam (MSME) Registration", "required": False},
            {"name": "FSSAI Registration", "required": False},
        ],
        "partner": {
            "name": "Nodal Agency / District Resource Person (PMFME)",
            "channel": "Apply on the PMFME portal",
            "url": "https://pmfme.mofpi.gov.in/",
            "notes": "District Resource Persons help with applications, ODOP alignment, FSSAI and Udyam registration support.",
        },
    },
    {
        "id": 3,
        "code": "MUDRA",
        "name": "PM MUDRA (PMMY) — Collateral-free Micro Enterprise Loan",
        "headline": "Collateral-free bank loans from ₹50,000 up to ₹20 lakh in four tiers.",
        "best_for": "Micro and small businesses needing a straightforward bank loan.",
        "description": (
            "Flagship bank-loan scheme (Pradhan Mantri Mudra Yojana) for non-farm, non-corporate "
            "income-generating micro and small enterprises. Collateral-free loans in tiers: Shishu "
            "up to ₹50,000; Kishore ₹50,001–₹5 lakh; Tarun ₹5,00,001–₹10 lakh; and Tarun Plus up "
            "to ₹20 lakh. Summarised from official scheme documents — verify with your lender before applying."
        ),
        "authority": "Department of Financial Services, Ministry of Finance (refinanced by MUDRA)",
        "category_tag": "bank_led",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 2,
        "official_reference": {
            "label": "MUDRA — official scheme offerings",
            "url": "https://www.mudra.org.in/",
        },
        "eligibility_rules": [
            _rule("age", "greater_than_or_equal", 18, "Age",
                  why_it_matters="Borrowers must be adults to sign the loan agreement."),
            _rule("business_type", "not_in", ["agriculture"], "Business Type",
                  why_it_matters="MUDRA covers non-farm, non-corporate income-generating activity."),
            _rule("business_stage", "in", ["early_stage", "existing"], "Business Stage",
                  why_it_matters="Both new and existing micro businesses can borrow under PMMY."),
            _rule("funding_need", "between", [10000, 2000000], "Funding Need",
                  why_it_matters="Tiered loans: Shishu up to ₹50,000; Kishore up to ₹5 lakh; Tarun up to ₹10 lakh; Tarun Plus up to ₹20 lakh."),
            _rule("financing_type", "in", ["loan", "any"], "Financing Preference",
                  required=False,
                  why_it_matters="Assistance is delivered as a collateral-free bank loan."),
        ],
        "finance": {
            "financing_type": "loan",
            "assistance_text": (
                "Collateral-free bank loan — Shishu up to ₹50,000; Kishore ₹50,001–₹5 lakh; "
                "Tarun ₹5,00,001–₹10 lakh; Tarun Plus up to ₹20 lakh."
            ),
            "contribution_text": "No fixed margin prescribed; individual lenders may apply their own norms.",
            "notes": "Refinanced by MUDRA; interest rates vary by lender. No collateral required within the scheme limits.",
        },
        "documents": [
            {"name": "Identity Proof (KYC)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Business Proof / Shop Establishment", "required": True},
            {"name": "Bank Statement (last 6 months)", "required": True},
            {"name": "Equipment Quotation", "required": False},
        ],
        "partner": {
            "name": "Banks, NBFCs and Micro-Finance Institutions",
            "channel": "Any bank branch or the JanSamarth portal",
            "url": "https://www.jansamarth.in/",
            "notes": "Every scheduled commercial bank, many RRBs, cooperatives and NBFC-MFIs lend under PMMY; JanSamarth is the government's credit-linkage portal.",
        },
    },
    {
        "id": 4,
        "code": "SUI",
        "name": "Stand-Up India — Bank Loans for SC/ST & Women Entrepreneurs",
        "headline": "Bank loans ₹10 lakh–₹1 crore for SC/ST & women greenfield entrepreneurs.",
        "best_for": "SC/ST and women entrepreneurs launching a large greenfield venture.",
        "description": (
            "Facilitates composite bank loans between ₹10 lakh and ₹1 crore for greenfield "
            "enterprises in manufacturing, services or trading, for at least one Scheduled Caste "
            "or Scheduled Tribe borrower and at least one woman borrower per bank branch. "
            "Summarised from official scheme documents — verify on the official portal before applying."
        ),
        "authority": "Department of Financial Services, Ministry of Finance (facilitated by SIDBI)",
        "category_tag": "bank_led",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 2,
        "official_reference": {
            "label": "Stand-Up India — official portal",
            "url": "https://www.standupmitra.in/",
        },
        "eligibility_rules": [
            _rule("age", "greater_than_or_equal", 18, "Age",
                  why_it_matters="Borrowers must be adults to sign the loan agreement."),
            _rule("category", "in", ["sc", "st", "women"], "Category / Community",
                  why_it_matters="The scheme specifically serves SC, ST and women first-generation entrepreneurs."),
            _rule("business_stage", "equals", "early_stage", "Business Stage",
                  why_it_matters="Only greenfield (brand-new) ventures are funded under this scheme."),
            _rule("business_type", "not_in", ["agriculture"], "Business Type",
                  why_it_matters="Covers greenfield enterprises in manufacturing, services or trading."),
            _rule("funding_need", "between", [1000000, 10000000], "Funding Need",
                  why_it_matters="Composite loans run from ₹10 lakh up to ₹1 crore."),
            _rule("financing_type", "in", ["loan", "any"], "Financing Preference",
                  required=False,
                  why_it_matters="Assistance is delivered as a bank loan."),
        ],
        "finance": {
            "financing_type": "loan",
            "assistance_text": (
                "Composite bank loan between ₹10 lakh and ₹1 crore for a greenfield enterprise, "
                "covering up to 85% of project cost."
            ),
            "contribution_text": "Margin money of about 15% (per bank norms).",
            "margin_rate": 0.15,
            "notes": "Repayment up to 7 years with a moratorium as per bank norms. Every bank branch funds at least one SC/ST and one woman beneficiary.",
        },
        "documents": [
            {"name": "Identity Proof (Aadhaar / PAN)", "required": True},
            {"name": "Caste Certificate (for SC/ST applicants)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Project Report / Business Plan", "required": True},
            {"name": "Machinery / Equipment Quotation", "required": True},
            {"name": "Bank Statement (last 6 months)", "required": True},
        ],
        "partner": {
            "name": "Any Scheduled Commercial Bank (Stand-Up Mitra support)",
            "channel": "Bank branch or the Stand-Up India portal",
            "url": "https://www.standupmitra.in/",
            "notes": "Every bank branch funds at least one SC/ST and one woman entrepreneur; the Stand-Up Mitra portal helps with handholding and mentoring.",
        },
    },
    {
        "id": 5,
        "code": "PMSVANIDHI",
        "name": "PM SVANidhi — Working Capital Loans for Street Vendors",
        "headline": "Collateral-free ₹10k–₹50k tranches + 7% interest subsidy for street vendors.",
        "best_for": "Street vendors building repayment history tranche by tranche.",
        "description": (
            "Micro-credit facility of the Ministry of Housing & Urban Affairs for street vendors "
            "holding vending rights. Provides collateral-free working-capital loans in progressive "
            "tranches — ₹10,000, then ₹20,000, then ₹50,000 — with a 7% interest subsidy on timely "
            "or early repayment. Summarised from official scheme documents — verify on the official "
            "portal before applying."
        ),
        "authority": "Ministry of Housing & Urban Affairs, Government of India",
        "category_tag": "central_government",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 1,
        "official_reference": {
            "label": "MoHUA — official PM SVANidhi portal",
            "url": "https://pmsvanidhi.mohua.gov.in/",
        },
        "eligibility_rules": [
            _rule("age", "greater_than_or_equal", 18, "Age",
                  why_it_matters="Borrowers must be adults to sign the loan agreement."),
            _rule("business_type", "in", ["retail", "trading", "services"], "Business Type",
                  why_it_matters="Street-vending activity maps to retail, trading or small services."),
            _rule("funding_need", "between", [10000, 50000], "Funding Need",
                  why_it_matters="Working-capital loans come in tranches of ₹10,000, ₹20,000 and ₹50,000."),
            _rule("financing_type", "in", ["loan", "any"], "Financing Preference",
                  required=False,
                  why_it_matters="Assistance is delivered as a collateral-free micro loan."),
        ],
        "finance": {
            "financing_type": "loan",
            "assistance_text": (
                "Collateral-free working-capital loans in progressive tranches — ₹10,000, then "
                "₹20,000, then ₹50,000 — with a 7% interest subsidy on timely or early repayment."
            ),
            "contribution_text": "None — the loan covers working capital in full.",
            "notes": "Digital-transaction cashback and priority for subsequent tranches. Requires vending rights (Letter of Vending).",
        },
        "documents": [
            {"name": "Identity Proof (Aadhaar)", "required": True},
            {"name": "Letter of Vending / Vending Certificate", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Bank Account Details", "required": True},
        ],
        "partner": {
            "name": "Lending Institutions via Urban Local Bodies (PM SVANidhi)",
            "channel": "Apply on the PM SVANidhi portal",
            "url": "https://pmsvanidhi.mohua.gov.in/",
            "notes": "Applications through lending institutions and MFIs coordinated by Urban Local Bodies; a Letter of Vending is required.",
        },
    },
    # ---- Bank-loan options (2) ----
    {
        "id": 6,
        "code": "HDFC",
        "name": "HDFC Bank Business Loans (for Existing Businesses)",
        "headline": "Existing businesses can apply for a business loan through HDFC Bank — amount and rate depend on the business profile.",
        "best_for": "Existing businesses with a track record looking to borrow from a large private bank.",
        "description": (
            "HDFC Bank offers business loans (including business loans for existing businesses, "
            "and bank-funded MUDRA loans to eligible micro enterprises) through its existing-business "
            "and SME channels. Loan amount, rate and tenure depend on the applicant's business "
            "profile — age of the business, turnover, repayment track record and collateral "
            "availability where relevant. Summarised from the bank's published loan pages and help "
            "content — exact eligibility, documents and rates are set by the bank at the time of "
            "application, so confirm on the bank's website or a branch before applying."
        ),
        "authority": "HDFC Bank (private sector bank)",
        "category_tag": "bank_loan_option",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 0,
        "official_reference": {
            "label": "HDFC Bank — business loans (published product pages)",
            "url": "https://www.hdfcbank.com/personal/business-loans.html",
        },
        "eligibility_rules": [],
        "finance": {
            "financing_type": "loan",
            "assistance_text": "Bank loan for eligible existing businesses — amount and terms depend on the applicant's business profile.",
            "contribution_text": "Any margin / own contribution required is set by the bank at the time of application.",
            "notes": "Eligibility, documents, interest rate and tenure are decided by the bank per application. This is a prototype summary, not a guaranteed offer.",
        },
        "documents": [
            {"name": "Identity Proof (KYC)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Business Proof / Trade License / GST", "required": True},
            {"name": "Business Bank Statements / Financials", "required": True},
            {"name": "Income Tax Returns (where applicable)", "required": False},
        ],
        "partner": {
            "name": "HDFC Bank — business-loan channel",
            "channel": "HDFC Bank website or nearest branch",
            "url": None,
            "notes": "Apply on the bank's business-loan pages or approach a branch. Bank decisions are per application and not made by SamarthSetu.",
        },
        "why_good_fit_note": (
            "A large private bank like HDFC can be a natural fit once your business is "
            "underway — it can fund expansion, equipment or working capital where you have a "
            "track record, and it also lends MUDRA loans to eligible micro enterprises through "
            "the same bank channel."
        ),
    },
    {
        "id": 7,
        "code": "AXIS",
        "name": "Axis Bank SME Banking & Loan Products",
        "headline": "Axis Bank offers SME business loans (including collateral-free options and bank-funded MUDRA loans) for eligible micro, small and medium enterprises.",
        "best_for": "Micro and small businesses looking for an SME loan or bank-funded MUDRA loan from a private bank.",
        "description": (
            "Axis Bank offers a range of business/SME loan and banking products — including collateral-free "
            "business-loan options for eligible enterprises and bank-funded MUDRA loans for eligible micro "
            "enterprises — with amount, rate and tenure depending on the business profile. Summarised from "
            "the bank's published SME and MUDRA product information and help content — exact eligibility, "
            "documents and rates are set by the bank at the time of application, so confirm on the bank's "
            "website or a branch before applying."
        ),
        "authority": "Axis Bank (private sector bank)",
        "category_tag": "bank_loan_option",
        "status": "active",
        "data_label": DATA_LABEL,
        "version": "2.0-real",
        "priority_weight": 0,
        "official_reference": {
            "label": "Axis Bank — business loans / SME banking",
            "url": "https://www.axisbank.com/retail/business-loan.html",
        },
        "eligibility_rules": [],
        "finance": {
            "financing_type": "loan",
            "assistance_text": "Bank loan (and bank-funded MUDRA loan where eligible) for eligible micro, small and medium enterprises.",
            "contribution_text": "Any margin / own contribution required is set by the bank at the time of application.",
            "notes": "Eligibility, documents, interest rate and tenure are decided by the bank per application. This is a prototype summary, not a guaranteed offer.",
        },
        "documents": [
            {"name": "Identity Proof (KYC)", "required": True},
            {"name": "Address Proof", "required": True},
            {"name": "Business Proof / Trade License / GST", "required": True},
            {"name": "Business Bank Statements / Financials", "required": True},
            {"name": "Income Tax Returns (where applicable)", "required": False},
        ],
        "partner": {
            "name": "Axis Bank — SME banking channel",
            "channel": "Axis Bank website or nearest branch",
            "url": None,
            "notes": "Apply on the bank's business/SME loan pages or approach a branch. Bank decisions are per application and not made by SamarthSetu.",
        },
        "why_good_fit_note": (
            "Axis Bank's SME banking can be a good fit for micro businesses that want a bank loan — "
            "including collateral-free options and bank-funded MUDRA loans for eligible micro enterprises "
            "— where the business fits the bank's eligibility at the time of application."
        ),
    },
]

DEMO_APPLICANT: Dict[str, Any] = {
    "name": "Aarav Patel",
    "age": 28,
    "location": "Ahmedabad",
    "category": "general",
    "income": 500000,
    "business_type": "food_processing",
    "business_stage": "early_stage",
    "sector": "food_processing",
    "business_status": "not_registered",
    "funding_need": 500000,
    "funding_purpose": "equipment",
    "financing_type": "loan",
    "natural_language_description": (
        "I am Aarav Patel, 28, from Ahmedabad. I am starting a small food-processing "
        "business and need around ₹5 lakh for equipment and working capital."
    ),
}

DISCLAIMER = (
    "This result is an eligibility assessment based on the information provided. "
    "It is not an approval or funding guarantee."
)


# ---------------------------------------------------------------------------
# Result persistence (JSON file)
# ---------------------------------------------------------------------------
def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_results() -> Dict[str, dict]:
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_results(results: Dict[str, dict]) -> None:
    _ensure_data_dir()
    tmp = RESULTS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, RESULTS_FILE)


def save_result(result: Dict[str, Any]) -> str:
    with _lock:
        results = _load_results()
        results[result["result_id"]] = result
        _save_results(results)
    return result["result_id"]


def get_result(result_id: str) -> Optional[dict]:
    return _load_results().get(result_id)


def list_results(limit: int = 50) -> List[dict]:
    results = list(_load_results().values())
    results.sort(key=lambda r: r.get("metadata", {}).get("evaluated_at", ""), reverse=True)
    return results[:limit]


def clear_results() -> None:
    with _lock:
        _save_results({})


# ---------------------------------------------------------------------------
# User-chosen document readiness (global, synced from the UI)
# ---------------------------------------------------------------------------
DOCSTATES_FILE = os.path.join(DATA_DIR, "doc_states.json")


def load_doc_states() -> Dict[str, bool]:
    try:
        with open(DOCSTATES_FILE, "r", encoding="utf-8") as fh:
            return {k: bool(v) for k, v in json.load(fh).items()}
    except (OSError, json.JSONDecodeError):
        return {}


def save_doc_states(states: Dict[str, bool]) -> None:
    _ensure_data_dir()
    clean = {str(k): bool(v) for k, v in (states or {}).items() if v}
    tmp = DOCSTATES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(clean, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, DOCSTATES_FILE)


def apply_doc_states_to_results(states: Dict[str, bool]) -> int:
    """Merge the user's document choices into every saved result's documents
    block, so reopened history always reflects what the user marked."""
    updated = 0
    with _lock:
        results = _load_results()
        for result in results.values():
            documents = result.get("documents")
            if not documents or not documents.get("items"):
                continue
            _merge_doc_states(documents, states)
            updated += 1
        if updated:
            _save_results(results)
    return updated


def _merge_doc_states(documents: Dict[str, Any], states: Dict[str, bool]) -> None:
    marked = [name for name, ready in states.items() if ready]
    ready_count = 0
    for item in documents.get("items", []):
        name = item.get("name")
        ready = doc_is_marked(name, marked) if name else bool(item.get("ready"))
        item["ready"] = ready
        item["status_note"] = "Marked as ready by you" if ready else "Not yet marked"
        ready_count += 1 if ready else 0
    documents["ready_count"] = ready_count


def new_id() -> str:
    return str(uuid.uuid4())


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Lightweight knowledge-graph representation
# ---------------------------------------------------------------------------
def knowledge_graph() -> Dict[str, Any]:
    """Return a serialisable view of the scheme knowledge graph.

    Graph: Applicant -> Attributes -> Potential Scheme -> Eligibility Rules
           -> Finance -> Documents -> Partner
    The Rule Engine — not this graph — makes the final eligibility decision.
    Government schemes only; bank options are grounded recommendations, not
    evaluated by the rule engine.
    """
    nodes: List[dict] = [{"id": "applicant", "type": "Applicant", "label": "Applicant"}]
    edges: List[dict] = []
    attr_fields = [
        "age", "location", "category", "income", "business_type",
        "business_stage", "sector", "business_status", "funding_need",
        "funding_purpose", "financing_type",
    ]
    for f in attr_fields:
        nodes.append({"id": f"attr:{f}", "type": "ApplicantAttribute", "label": f})
        edges.append({"from": "applicant", "to": f"attr:{f}", "relation": "HAS_ATTRIBUTE"})
        for s in SCHEMES:
            if s.get("category_tag") != "bank_loan_option":
                if any(r["field"] == f for r in s["eligibility_rules"]):
                    edges.append({"from": f"attr:{f}", "to": f"scheme:{s['id']}", "relation": "CONSTRAINS"})
    for s in SCHEMES:
        sid = f"scheme:{s['id']}"
        nodes.append({"id": sid, "type": "Scheme", "label": s["name"], "data_label": DATA_LABEL})
        nodes.append({"id": f"finance:{s['id']}", "type": "Finance", "label": f"{s['name']} — Finance"})
        nodes.append({"id": f"docs:{s['id']}", "type": "Documents", "label": f"{s['name']} — Documents"})
        nodes.append({"id": f"partner:{s['id']}", "type": "Partner", "label": s["partner"]["name"]})
        edges += [
            {"from": sid, "to": f"finance:{s['id']}", "relation": "HAS_FINANCE"},
            {"from": sid, "to": f"docs:{s['id']}", "relation": "REQUIRES_DOCUMENTS"},
            {"from": sid, "to": f"partner:{s['id']}", "relation": "ROUTES_TO"},
        ]
    return {"nodes": nodes, "edges": edges, "data_label": DATA_LABEL}
