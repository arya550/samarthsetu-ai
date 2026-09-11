# SamarthSetu AI — Product & Technical Blueprint (v2)

### Tester-First, Implementation-Ready Specification for Devin

**Sources of truth (in order of authority):**

1. `SmartSetu-UX-Design-Spec.md` (uploaded) — screens, navigation, layout, copy rules, design system, accessibility
2. SIH pitch-prep transcript (pasted in chat) — the actual product domain: **AI Driven Scheme Matching for Marginalized Entrepreneurs**, theme *Smart Automation*, core USP: *"One profile → one intelligent pathway to access."*

**What changed from v1:** v1 correctly refused to guess the domain and built everything around a placeholder `ProcessingEngine`. That placeholder is now resolved — the domain is confirmed. This document keeps every UX/navigation/screen/security/accessibility decision from v1 (all still correct and unaffected by the domain reveal) and replaces every domain-dependent piece — the core feature, database, API, and AI/processing layer — with the real SamarthSetu logic.

> ⚠️ **Still genuinely unknown after both sources** (kept honest — see §3): the *exact* 3–5 MVP schemes and their real eligibility rules/financial terms/document lists/partner mappings are not specified anywhere in either source. The pitch explicitly says the MVP is scoped to "3–5 representative schemes" using "verified official information," but doesn't name them. This blueprint defines the **data structures** those schemes must fill (Scheme DNA), not their content — Devin needs real scheme data from the team before Phase 2/4 can be more than structurally complete.

---

## 1. Executive Summary

SamarthSetu AI is an AI-assisted pathway system, not a scheme search engine. A marginalized entrepreneur describes their situation in plain language (age, location, income, business type/stage, financing need, category); the system extracts a structured **Applicant Profile**; matches it against a **Scheme Knowledge Graph** where every scheme is represented as **Scheme DNA** (Eligibility + Finance + Documents + Partner); runs a **deterministic Rule Engine** (never the LLM) to verify eligibility; and returns an explainable result covering four things a scheme directory never gives together: *why you're eligible, what you can receive, what documents you're missing, and where to go next.*

The critical design constraint carried through this entire document: **the LLM never decides eligibility.** It only does natural-language input extraction, multilingual interaction, and explaining a result the rule engine already computed. This is both the pitch's core defensibility argument and a hard architectural rule enforced at the API boundary (§14).

The UX shell from v1 (landing, auth, dashboard, 4-step guided flow, processing state, result screen, history, notifications, profile, settings, demo mode, error states, accessibility, design system) is unchanged and still fully applies — "Start a SmartSetu request" *is* "get matched to a scheme," and the generic `[Core action]` from v1 is now concretely "Check my eligibility" / "Find my scheme."

---

## 2. Confirmed Requirements (delta from v1)

Everything confirmed in v1 §2 remains confirmed (screens, nav, design system, accessibility, priority split, demo-mode structure). New confirmations from the SIH source:

| # Confirmed requirement Source  |                                                                                                                                                                                                            |       |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 27                              | Product name: **SamarthSetu AI**; tagline **"From Eligibility to Access"**                                                                                                                                 | pitch |
| 28                              | Problem statement: **AI Driven Scheme Matching for Marginalized Entrepreneurs**, theme *Smart Automation*                                                                                                  | pitch |
| 29                              | Pipeline: **User Input → Profile Extraction → Scheme Knowledge Graph → Rule Engine → AI Explanation → Financial & Document Engines → Partner Routing**                                                     | pitch |
| 30                              | Applicant profile fields (confirmed set): age, location, income, business type, business stage, financing requirement, category/community                                                                  | pitch |
| 31                              | Every scheme is represented as **Scheme DNA**: Eligibility, Finance, Documents, Partner(s)                                                                                                                 | pitch |
| 32                              | Scheme relationships modeled as a **Knowledge Graph**                                                                                                                                                      | pitch |
| 33                              | **Rule engine performs eligibility verification — not the LLM.** This is an explicit, non-negotiable architectural requirement                                                                             | pitch |
| 34                              | AI's confirmed scope: natural-language profile extraction, explainable recommendations, multilingual interaction                                                                                           | pitch |
| 35                              | System generates a **personalized financial pathway** (not just "you are eligible")                                                                                                                        | pitch |
| 36                              | System produces **Document Readiness** (checklist + missing-items count, e.g. "3/5 ready")                                                                                                                 | pitch |
| 37                              | System performs **Partner Routing** to the correct channel/institution/department                                                                                                                          | pitch |
| 38                              | Confirmed tech stack: **React** (frontend), **Python** (backend/AI logic), **FastAPI** (API layer), **PostgreSQL** (structured data), **Neo4j** (knowledge graph), **NLP/LLM** (language understanding)    | pitch |
| 39                              | MVP scope: **3–5 representative schemes**, full pipeline built around them, not an attempt to digitize every scheme                                                                                        | pitch |
| 40                              | Prototype uses **verified official scheme information**; any sample/placeholder data must be clearly labeled as such, never presented as official                                                          | pitch |
| 41                              | USP (memorize-level, use verbatim in UI/pitch copy where relevant): **"One profile → one intelligent pathway to access."**                                                                                 | pitch |
| 42                              | Positioning vs. existing scheme portals: they help users *discover* schemes; SamarthSetu takes them from *discovery to access*                                                                             | pitch |
| 43                              | 36-hour build plan reference (informational, not binding on Devin's actual schedule): 0–12h research/DB/graph, 12–27h frontend/matching/financial modules, 27–36h partner routing/integration/testing/demo | pitch |
| 44                              | Future scope (explicitly **not** MVP): nationwide scheme coverage, live/official APIs, OCR for document verification, deeper automation                                                                    | pitch |

---

## 3. Unknowns (updated)

v1's U1 and most of U2 are now **resolved** — struck through and replaced below. Remaining unknowns:

| ID Status Unknown Why it matters Safe assumption  |                       |                                                                          |                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------- | --------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| \~\~U1\~\~                                        | **RESOLVED**          | \~\~What SmartSetu's core action is\~\~                                  | —                                                                                                                                                                                           | Confirmed: AI-driven scheme matching + eligibility + financial/document/partner pathway for marginalized entrepreneurs (§1).                                                                                                                                                                                                                                                                             |
| \~\~U2\~\~                                        | **RESOLVED (scoped)** | \~\~Whether AI/ML is used\~\~                                            | —                                                                                                                                                                                           | Confirmed: yes, but strictly bounded to NLP extraction, explanation generation, and multilingual interaction. Eligibility itself is **never** AI-decided (Confirmed req. #33).                                                                                                                                                                                                                           |
| **U13 (new)**                                     | OPEN                  | The actual identity of the 3–5 MVP schemes and their real rules          | Without real scheme data, "Scheme DNA" and the Rule Engine have no real content to run against — this is the single biggest remaining blocker to a genuinely working (not placeholder) demo | Build the full schema (§12) and seed it with **clearly-labeled sample scheme data** modeled on realistic Indian MSME/entrepreneurship schemes (e.g., structure resembling PMEGP/Stand-Up India-style schemes), explicitly marked `is_verified_official = false` until the team supplies real, sourced scheme text. **Never present sample scheme data as officially verified** (direct requirement #40). |
| **U14 (new)**                                     | OPEN                  | Exact NLP/LLM provider and extraction approach                           | Pitch confirms NLP/LLM is used for extraction and explanation but not which model/provider/hosting                                                                                          | Backend calls an LLM through a single abstracted `NLProfileExtractor` / `ExplanationGenerator` interface (§14) so the provider is swappable; use a well-known hosted LLM API as the default assumption, key stored in secrets (§15).                                                                                                                                                                     |
| **U15 (new)**                                     | OPEN                  | Multilingual scope — which languages, and whether input, output, or both | Pitch confirms "multilingual interaction" as a feature but names no specific languages                                                                                                      | Architected as a language parameter passed through extraction + explanation (§14); default to English + Hindi as the safest MVP assumption for an India-focused SIH prototype; exact language list is an Open Decision (§22).                                                                                                                                                                            |
| **U16 (new)**                                     | OPEN                  | OCR/document upload for readiness checking                               | Pitch explicitly places OCR in **Future scope**, not MVP                                                                                                                                    | Document Readiness (§5.D, §12) is built as a **self-reported checklist** (user marks/answers "do you have X?") for MVP — no file upload, no OCR. Upload+OCR is a clearly labeled P2/future item, not built now.                                                                                                                                                                                          |
| **U17 (new)**                                     | OPEN                  | Partner data — real institutions/departments per scheme                  | Pitch confirms routing exists but gives no real partner directory                                                                                                                           | `partners` table (§12) seeded with sample/placeholder partner records per demo scheme, same "not verified" labeling rule as U13.                                                                                                                                                                                                                                                                         |
| U3–U12                                            | Unchanged from v1     | See v1 §3                                                                | Same as v1                                                                                                                                                                                  | Same as v1 — U4 (auth mechanism), U5 (saved items), U6 (roles), U7 (real application submission — **now more clearly "not yet," since routing ends at a partner/channel, not a submission**), U8 (admin), U9 (support surface), U10 (notification channels), U11 (edit/cancel), U12 (session policy) all still open exactly as in v1.                                                                    |

---

## 4. Product Definition (updated)

### What SamarthSetu AI is

An AI-assisted pathway system that takes a marginalized entrepreneur from *"what am I eligible for?"* to *"here's exactly what I qualify for, why, what I can receive, what I still need, and where to go."* It is explicitly **not** another scheme directory or a chatbot layered on search.

### What problem it solves

Schemes exist, but applicants can't tell which one applies to them, eligibility rules are complex and scattered across sources, and even a discovered scheme leaves financial terms, required documents, and the application channel unclear.

### Who it's for

Marginalized entrepreneurs (the pitch's example persona: a 32-year-old wanting to start a small manufacturing or trading business, belonging to an eligible community/category, with a defined income and financing need) — and, for the SIH build, the **jury/evaluator** as a first-time tester who must understand and trust the system in minutes.

### What makes it useful

It replaces manual cross-referencing of scattered scheme pages with one guided profile → one computed, explainable, actionable pathway — eligibility, money, documents, and destination, together.

### Main user value

Confidence and clarity: not just "you might be eligible," but a verified, explainable answer plus a concrete next step.

### Primary SamarthSetu action

Build an applicant profile (conversationally, via short guided steps) → match against the Scheme Knowledge Graph → verify eligibility via the deterministic Rule Engine → receive an explainable result with financial pathway, document readiness, and partner routing.

### Complete user journey

```
Landing → Try SamarthSetu → Demo access or Login → Dashboard
 → Start a request ("Check my eligibility")
 → About you (profile fields) → Your request (financing need/business info)
 → Review → Run eligibility check (Rule Engine + AI explanation)
 → Processing → Result (eligible scheme, why, financial pathway,
   document readiness, partner routing) → Next action
 → History / Notifications

```

### What the user receives at the end

A matched scheme (or an honest "not currently eligible" outcome), a plain-language explanation of *why*, a financial pathway describing what assistance they can receive, a document-readiness checklist showing what's ready vs. missing, and a named next channel/partner to pursue it through.

### Why a first-time tester (jury) would want to explore it

The pitch's own hook applies directly: within one flow, the evaluator sees the system go further than a scheme directory ever does — eligibility explained, money quantified, documents checked, and a destination named, using real architecture (Scheme DNA + Knowledge Graph + Rule Engine), not just an AI chat wrapper.

### SamarthSetu AI in one sentence

**SamarthSetu AI turns a marginalized entrepreneur's situation into a verified, explainable pathway to the right financial scheme — from eligibility to access.**

### SamarthSetu AI in 10 seconds

Tell SamarthSetu your situation, and it tells you which scheme you actually qualify for, what you can receive, what documents you're missing, and where to go next.

### SamarthSetu AI in 30 seconds

SamarthSetu AI replaces scattered scheme-hunting with one guided profile. You describe your situation in plain language; the system extracts a structured profile and matches it against a knowledge graph of schemes, each represented as "Scheme DNA" — eligibility rules, financial terms, required documents, and routing partners. A deterministic rule engine — never the AI — verifies eligibility, so the result is auditable, not guessed. You get back an explainable match: why you qualify, what financial assistance you can receive, a document-readiness checklist, and the exact partner or channel to pursue next. One profile, one intelligent pathway to access.

---

## 5. Feature Architecture — Updated Section D

(All other feature areas A, B, C, E–U are unchanged from v1 §5 — the UX shell, forms-as-steps, processing/result *structure*, history, notifications, profile, settings, demo mode, errors, accessibility, responsiveness, and security all still apply exactly as written. Only the *content* of the core capability changes, below.)

### D. Core SamarthSetu capabilities — **[CONFIRMED, domain resolved]**

- **Purpose:** Convert a plain-language applicant situation into a verified, explainable scheme match with a full access pathway.
- **User value:** One flow answers eligibility, financing, documents, and destination together — the exact gap the pitch identifies in existing portals.
- **Flow (five sub-stages, mapped onto the existing 4-step UX shell from v1 — see note below):** 
  1. **Profile Extraction** — user's plain-language / short-form answers → structured `applicant_profile` (age, location, income, business\_type, business\_stage, financing\_requirement, category).
  2. **Knowledge Graph Match** — profile queried against `Scheme` nodes and their `ELIGIBLE_FOR` / `REQUIRES_DOCUMENT` / `ROUTES_TO` relationships in Neo4j to shortlist candidate schemes.
  3. **Rule Engine Verification** — each candidate scheme's structured eligibility rules evaluated deterministically against the profile; only rule-engine-confirmed matches proceed. **The LLM is never called for this step.**
  4. **AI Explanation** — for confirmed (and honestly, for rejected) matches, the LLM generates a plain-language, and optionally multilingual, explanation of *why*.
  5. **Financial / Document / Partner assembly** — the matched scheme's Finance, Documents, and Partner sub-structures are assembled into the pathway shown on the Result screen.
- **Mapping onto v1's 4-step form (About you → Your request → Review → Result):** 
  - *About you* = profile fields feeding stage 1.
  - *Your request* = financing requirement + business specifics, also feeding stage 1.
  - *Review* = user confirms captured profile before stage 2–5 run.
  - *Result screen* = renders the outputs of stages 2–5 (see §5.G below, updated).
- **Required UI:** unchanged component tree from v1 §10, with `FieldGroup`s now concretely bound to the profile schema (§12 `applicant_profiles`), and `ResultPanel` sub-components now concretely populated (see below).
- **Backend logic:** orchestrated by `SchemeMatchingService`, calling `NLProfileExtractor` → `KnowledgeGraphMatcher` → `RuleEngine` → `ExplanationGenerator` → `PathwayAssembler`, in that fixed order (§14 — this *is* the resolved `ProcessingEngine` from v1).
- **Database:** `applicant_profiles`, `schemes`, `scheme_eligibility_rules`, `scheme_finance`, `scheme_documents`, `scheme_partners`, `document_readiness`, plus v1's `requests`/`results`/`activity_logs` (§12).
- **API:** `POST /api/requests/:id/run` (unchanged endpoint from v1, now with real behavior — see §13 updates).
- **Edge cases:** no scheme matches at all (honest "not currently eligible" result, still useful — shows the closest scheme and what would need to change), profile too incomplete to extract reliably (falls back to explicit guided fields instead of free text), rule engine and knowledge graph disagreeing on a candidate (rule engine always wins — it's the source of truth), LLM extraction misreading a field (user can review/edit the extracted profile before Review step confirms it — never silently trust raw NLP output).
- **Acceptance criteria:** every result traces to a rule-engine pass/fail, never an LLM guess (testable: `results.rule_engine_trace` must be non-null for every `outcome_type='found'` result); every result includes financial pathway + document readiness + partner routing together, not just an eligibility flag (matches the pitch's core differentiation claim).

---

## 6–11 (UX flow, journeys, tester timeline, curiosity strategy, screen map, frontend shell)

**Unchanged from v1 §6–§11**, with these content-level substitutions only:

- "Start a SmartSetu request" → **"Check my eligibility"** (primary CTA on the feature page and Dashboard next-action panel).
- Result screen's "What SmartSetu found" → now concretely: matched scheme name, eligibility explanation, financial pathway, document readiness, partner routing (see §12 below for the full updated Result screen structure).
- v1's seeded demo scenario ("Education support request") should be replaced with a scheme-matching-appropriate demo scenario, e.g.: **user "Priya Shah," request "Small manufacturing business — financing eligibility check," matched scheme "[Sample Scheme Name — clearly labeled as sample data, not verified official]," status "Result ready."** Exact sample scheme content is U13 — placeholder structure only until real data is supplied.

### 5.G — Result screen content (updated, replaces v1's generic version)

1. **What SamarthSetu found** — matched scheme name + status label ("Eligible" / "Not currently eligible" / "Needs more information") with icon, never color alone.
2. **Why this result appeared** — AI-generated explanation, grounded in the specific rule-engine checks that passed/failed (expandable — spec's progressive-disclosure rule still applies).
3. **Your financial pathway** — funding requirement vs. what the scheme offers (loan/subsidy/amount/structure), presented as a short sequence, not a data dump.
4. **Document readiness** — checklist (✓/✗ per required document) + a readiness ratio ("3/5 ready") + which documents are missing.
5. **What to do next** — one dominant CTA naming the matched partner/channel ("View next steps at [Partner]"), never "Apply now" unless U7 is resolved.
6. **Request details** — request ID, timestamp, status (kept subordinate, per v1's existing rule).

---

## 12. Database Design (updated — adds the Scheme DNA / Knowledge Graph layer on top of v1's tables)

v1's `users`, `sessions`, `requests`, `request_answers`, `results`, `activity_logs`, `notifications` (all in PostgreSQL) are **unchanged** — see v1 §12 for full column definitions. Added tables/store below.

### PostgreSQL — new relational tables

**`applicant_profiles`** (structured extraction output, one per request)

| Column Type Notes      |                                |                                                                                                                |
| ---------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| id                     | UUID (PK)                      |                                                                                                                |
| request\_id            | UUID (FK → requests.id) UNIQUE |                                                                                                                |
| age                    | INTEGER                        |                                                                                                                |
| location               | VARCHAR(255)                   | state/district granularity, TBD with real scheme data                                                          |
| income                 | NUMERIC                        | annual, currency assumed INR                                                                                   |
| business\_type         | VARCHAR(255)                   | e.g. "manufacturing," "trading," "services"                                                                    |
| business\_stage        | VARCHAR(64)                    | e.g. `new`, `existing`                                                                                         |
| financing\_requirement | NUMERIC                        | requested amount                                                                                               |
| category               | VARCHAR(128)                   | community/eligibility category, free-text pending real scheme rule vocabulary                                  |
| raw\_input\_text       | TEXT NULL                      | original user free-text, for audit/debugging of extraction quality                                             |
| extraction\_confidence | VARCHAR(32) NULL               | e.g. `high`/`needs_review` — surfaced to the user as a review prompt before confirming, never silently trusted |
| created\_at            | TIMESTAMPTZ DEFAULT now()      |                                                                                                                |

**`schemes`** (the canonical Scheme DNA root — mirrors the Neo4j `Scheme` node, kept in Postgres too for transactional/admin convenience)

| Column Type Notes         |                       |                                                                  |
| ------------------------- | --------------------- | ---------------------------------------------------------------- |
| id                        | UUID (PK)             |                                                                  |
| name                      | VARCHAR(255)          |                                                                  |
| description               | TEXT                  |                                                                  |
| is\_verified\_official    | BOOLEAN DEFAULT false | **must be false for any sample/placeholder scheme (U13)**        |
| source\_reference         | TEXT NULL             | citation for verified schemes (e.g. issuing ministry/department) |
| is\_demo                  | BOOLEAN DEFAULT false |                                                                  |
| created\_at / updated\_at | TIMESTAMPTZ           |                                                                  |

**`scheme_eligibility_rules`** (structured, machine-evaluable — this is what the Rule Engine actually runs against)

| Column Type Notes                                                                                                                                                          |                           |                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------- |
| id                                                                                                                                                                         | UUID (PK)                 |                                                    |
| scheme\_id                                                                                                                                                                 | UUID (FK → schemes.id)    |                                                    |
| field                                                                                                                                                                      | VARCHAR(64)               | e.g. `age`, `income`, `category`, `business_stage` |
| operator                                                                                                                                                                   | VARCHAR(16)               | `eq`, `lt`, `lte`, `gt`, `gte`, `in`, `between`    |
| value                                                                                                                                                                      | JSONB                     | comparison value(s), shape depends on operator     |
| created\_at                                                                                                                                                                | TIMESTAMPTZ DEFAULT now() |                                                    |
| Rule engine evaluates every row for a scheme as an AND-combined rule set (documented assumption — real scheme rules may need OR-groups; flagged as an Open Decision, §22). |                           |                                                    |

**`scheme_finance`**

| Column Type Notes             |                               |                                                           |
| ----------------------------- | ----------------------------- | --------------------------------------------------------- |
| id                            | UUID (PK)                     |                                                           |
| scheme\_id                    | UUID (FK → schemes.id) UNIQUE |                                                           |
| assistance\_type              | VARCHAR(32)                   | `loan`, `subsidy`, `grant`, `mixed`                       |
| min\_amount / max\_amount     | NUMERIC                       |                                                           |
| interest\_rate                | NUMERIC NULL                  | if a loan component exists                                |
| applicant\_contribution\_note | TEXT NULL                     | plain-language note on what the applicant must contribute |

**`scheme_documents`**

| Column Type Notes  |                        |                                                        |
| ------------------ | ---------------------- | ------------------------------------------------------ |
| id                 | UUID (PK)              |                                                        |
| scheme\_id         | UUID (FK → schemes.id) |                                                        |
| document\_name     | VARCHAR(255)           | e.g. "Aadhaar," "Income certificate," "Business proof" |
| is\_mandatory      | BOOLEAN DEFAULT true   |                                                        |

**`document_readiness`** (per-request, self-reported checklist responses — no OCR/upload for MVP, U16)

| Column Type Notes                                      |                                  |                  |
| ------------------------------------------------------ | -------------------------------- | ---------------- |
| id                                                     | UUID (PK)                        |                  |
| request\_id                                            | UUID (FK → requests.id)          |                  |
| scheme\_document\_id                                   | UUID (FK → scheme\_documents.id) |                  |
| has\_document                                          | BOOLEAN                          | user self-report |
| updated\_at                                            | TIMESTAMPTZ DEFAULT now()        |                  |
| Unique constraint: `(request_id, scheme_document_id)`. |                                  |                  |

**`scheme_partners`**

| Column Type Notes      |                        |                                             |
| ---------------------- | ---------------------- | ------------------------------------------- |
| id                     | UUID (PK)              |                                             |
| scheme\_id             | UUID (FK → schemes.id) |                                             |
| partner\_name          | VARCHAR(255)           | e.g. institution/department/channel name    |
| partner\_type          | VARCHAR(64)            | e.g. `bank`, `government_department`, `ngo` |
| contact\_or\_link      | TEXT NULL              | how to actually reach them, if known        |
| is\_verified\_official | BOOLEAN DEFAULT false  | same U13/U17 labeling rule                  |

**Updates to** **`results`** **(from v1 §12) — additional columns:**

| Column Type Notes            |                                      |                                                                                  |
| ---------------------------- | ------------------------------------ | -------------------------------------------------------------------------------- |
| matched\_scheme\_id          | UUID (FK → schemes.id) NULL          | null when outcome\_type = `none`                                                 |
| rule\_engine\_trace          | JSONB                                | which rules passed/failed — the auditability guarantee behind confirmed req. #33 |
| financial\_pathway           | JSONB                                | rendered `scheme_finance` + applicant's financing\_requirement, assembled        |
| document\_readiness\_summary | JSONB                                | `{ ready: n, total: m, missing: [...] }`                                         |
| routed\_partner\_id          | UUID (FK → scheme\_partners.id) NULL |                                                                                  |

### Neo4j — Knowledge Graph (new store)

```
(:Applicant {request_id})-[:HAS_PROFILE]->(:Profile {age, income, location, business_type, category, ...})
(:Scheme {id, name})-[:REQUIRES_ELIGIBILITY]->(:EligibilityRule {field, operator, value})
(:Scheme)-[:OFFERS_FINANCE]->(:Finance {type, min_amount, max_amount})
(:Scheme)-[:REQUIRES_DOCUMENT]->(:Document {name, mandatory})
(:Scheme)-[:ROUTES_TO]->(:Partner {name, type})

```

- The graph is the **matching/traversal** layer (candidate shortlisting via relationship queries — e.g. "find schemes whose eligibility rules are structurally compatible with this profile's category and business\_type").
- The **Rule Engine** (a Python service, not a graph query) then re-verifies each shortlisted candidate deterministically against `scheme_eligibility_rules` in Postgres — this two-layer design (graph for *candidate discovery*, relational rules for *authoritative verification*) is what makes confirmed req. #33 ("rule engine, not the graph or the LLM, decides eligibility") concretely true rather than just a slogan.
- Neo4j and Postgres `schemes`/`scheme_eligibility_rules` are kept in sync by a single seed/admin write path — never written independently, to avoid drift (documented as an implementation rule for Devin, not left ambiguous).

---

## 13. API Specification (updated — additions/changes only; everything else from v1 §13 unchanged)

**`POST /api/requests/:id/run`** *(replaces v1's placeholder-engine version)*

- Auth: Yes (ownership enforced)
- Body: none (uses persisted `applicant_profiles` + `request_answers`)
- Validation: profile must have passed the Review step (all required profile fields present)
- Response `202`: `{ status: "processing" }`
- Errors: `403`, `409 INCOMPLETE_PROFILE`, `500 ENGINE_ERROR`
- DB effect: `requests.status → processing`; on completion, writes `results` (with the new `matched_scheme_id`, `rule_engine_trace`, `financial_pathway`, `document_readiness_summary`, `routed_partner_id` columns), `activity_logs`, triggers `NotificationService`
- Business logic: runs the fixed pipeline — `NLProfileExtractor` (if not already run at answer-time) → `KnowledgeGraphMatcher` (Neo4j candidate query) → `RuleEngine` (Postgres-backed deterministic verification, **authoritative**) → `ExplanationGenerator` (LLM, explanation only) → `PathwayAssembler` (finance + documents + partner)

**`PATCH /api/requests/:id/answers`** *(unchanged shape from v1, now concretely field-validated)*

- `step_key: "about_you"` fields map to `applicant_profiles` columns (age, location, category, business\_stage).
- `step_key: "your_request"` fields map to `applicant_profiles` (business\_type, financing\_requirement) — free-text input here is what feeds `NLProfileExtractor`.

**`PATCH /api/requests/:id/document-readiness`** *(new)*

- Auth: Yes
- Body: `{ scheme_document_id, has_document: boolean }`
- Response `200`: `{ saved: true, summary: { ready, total, missing[] } }`
- DB effect: upsert `document_readiness`
- Business logic: recomputes the readiness ratio shown on the Result screen; can be updated after the result is generated (user checks off documents over time — matches the spec's "document readiness" being an ongoing, not one-shot, concept)

**`GET /api/schemes`** *(new, admin/internal — not a public browse feature; MVP has no "browse all schemes" UI per the pitch's discovery-vs-access positioning)*

- Auth: Yes (or internal-only, depending on whether any admin tooling is ever built — ties to U8)
- Purpose: primarily for seeding/debugging and Devin's own testing, not a user-facing endpoint in the P0 journey.

---

## 14. AI/Processing Architecture (fully replaces v1 §14's placeholder)

This is the resolved version of v1's generic `ProcessingEngine` interface — now the real SamarthSetu pipeline, split into named, independently testable modules.

```
NLProfileExtractor → KnowledgeGraphMatcher → RuleEngine → ExplanationGenerator → PathwayAssembler

```

### `NLProfileExtractor` (AI/NLP)

- **Purpose:** turn free-text "your request" input into structured `applicant_profiles` fields.
- **Inputs:** raw user text (+ any explicit guided-field values already captured).
- **Outputs:** `{ age?, location?, income?, business_type?, business_stage?, financing_requirement?, category?, extraction_confidence }`.
- **Preprocessing:** basic normalization (currency parsing for financing amounts, e.g. "₹5 lakh" → numeric).
- **Confidence handling:** low-confidence extractions are **shown back to the user for confirmation/edit before Review** — never silently trusted (this directly satisfies the pitch's own framing: "treat user-provided information as input, not as proof").
- **Fallback behavior:** on extraction failure, fall back to the explicit guided `FieldGroup` inputs already defined for the "About you"/"Your request" steps — the free-text path is an accelerant, never a hard dependency.
- **Explainability:** N/A at this stage (explaining happens after matching, see below).
- **Multilingual (U15):** language passed as a parameter; extraction prompt is language-aware; default assumption English + Hindi pending U15's resolution.

### `KnowledgeGraphMatcher` (Neo4j)

- **Purpose:** cheaply shortlist *candidate* schemes via relationship traversal (category/business\_type/location compatibility) before expensive rule verification.
- **Inputs:** the confirmed `applicant_profiles` row.
- **Outputs:** an ordered list of candidate `scheme_id`s.
- **Not authoritative:** candidates here are a shortlist, not a decision — every candidate still must pass the Rule Engine.

### `RuleEngine` (deterministic, Python, Postgres-backed) — **the eligibility authority**

- **Purpose:** the one and only component allowed to decide eligibility (confirmed req. #33 — architecturally enforced, not just documented).
- **Inputs:** `applicant_profiles` row + each candidate scheme's `scheme_eligibility_rules` rows.
- **Logic:** evaluate every rule (`field`/`operator`/`value`) against the profile; a scheme passes only if **all** its rules pass (documented AND-only assumption, §12 note; OR-groups are an Open Decision if real scheme rules need them).
- **Outputs:** per-candidate pass/fail + a full `rule_engine_trace` (which rules passed/failed and why) — this trace is what makes the result auditable, and is stored verbatim on `results.rule_engine_trace`.
- **Confidence handling:** N/A — deterministic, binary per rule.
- **Fallback behavior:** if no candidate passes, the engine still returns its trace for the *closest* candidate (most rules passed) so the Result screen can show a genuinely useful "not currently eligible — here's what's missing" outcome instead of a dead end (matches v1's "no-result request" journey, §6, still fully valid).

### `ExplanationGenerator` (AI/LLM) — explanation only, never eligibility

- **Purpose:** turn the rule engine's trace into a plain-language, optionally multilingual explanation.
- **Inputs:** `rule_engine_trace` + matched (or closest) scheme's data.
- **Outputs:** `explanation` text for `results.explanation`.
- **Confidence handling:** the LLM is prompted to explain only what the trace already shows — never to introduce new eligibility claims. This constraint should be enforced by prompt design and, ideally, a lightweight validation pass (e.g., the explanation must not assert eligibility on a field the trace marked failed) — flagged as a build-time safeguard Devin should implement, not just a prompt instruction.
- **Explainability:** this module's entire job *is* explainability — it's the answer to the pitch's own "what if AI hallucinates eligibility?" defense.
- **API integration:** single external LLM call per result generation; retried once on failure, then falls back to a template-based explanation built directly from the rule trace (never silently fails to explain).
- **Security:** LLM API key in secrets manager/env vars only (§15, unchanged from v1).
- **Cost considerations:** one call per request run (not per candidate scheme) keeps cost bounded and predictable for an MVP of 3–5 schemes.

### `PathwayAssembler`

- **Purpose:** combine `scheme_finance`, `scheme_documents` (+ `document_readiness`), and `scheme_partners` for the matched (or closest) scheme into the `financial_pathway`, `document_readiness_summary`, and `routed_partner_id` fields on `results`.
- **No AI involved** — pure data assembly from already-structured tables.

---

## 15–18 (Security, Demo Mode, Error Handling, Testing Strategy)

**Unchanged in structure from v1 §15–§18.** Two domain-specific additions:

- **§15 addition:** LLM API key(s) for `NLProfileExtractor`/`ExplanationGenerator` follow the exact same secrets-management rule as everything else in v1 §15 — env vars/secrets manager only, never hard-coded, never logged.
- **§16 addition (Demo Mode seed data):** replace v1's "Education support request" scenario with a scheme-matching scenario built on **clearly-labeled sample scheme data** (U13) — e.g. a sample manufacturing-business scheme with realistic but explicitly non-official eligibility rules, finance terms, document list, and partner, so the demo can run the *real* pipeline (extraction → graph → rules → explanation → pathway) end-to-end without waiting on real scheme sourcing.
- **§18 addition (testing):** add explicit test cases for the Rule Engine's auditability guarantee — e.g., assert that `results.rule_engine_trace` is always present and non-empty for any `outcome_type` other than a hard system failure; assert the `ExplanationGenerator`'s output never claims eligibility on a rule the trace marked failed (a direct regression test for the pitch's core safety claim).

---

## 19. Priority Matrix (updated)

**P0 — must work for the demo** *(v1's P0 list, with the core item now concrete)*

- Landing → Demo mode → Dashboard
- Dashboard → "Check my eligibility" flow
- 4-step form (About you / Your request / Review / Result) with validation
- **Real pipeline execution:** NLProfileExtractor → KnowledgeGraphMatcher → RuleEngine → ExplanationGenerator → PathwayAssembler, running against at least one seeded sample scheme end-to-end
- Result screen showing all four pillars together: eligibility explanation, financial pathway, document readiness, partner routing
- Request saved to History; notification linked to result
- Session-expired / empty-history / no-search-results / processing-failure recovery states (unchanged from v1)

**P1 — improves credibility**

- Login/registration polish, Profile, Settings, History search/filter, responsive nav, accessibility (all unchanged from v1)
- Multilingual explanation output (U15) — at least a second language beyond English
- Document-readiness updates persisting across sessions (already in scope structurally, §12/§13)

**P2 — only if backed by real requirements / confirmed by the team**

- Real, verified scheme data replacing sample data (U13) — **note: this is P2 only in the sense of "not required to demo the pipeline," but it is the single highest-value real-world upgrade and should be prioritized the moment the team has sourced data**
- OCR/document upload (U16, explicitly future scope per the pitch itself)
- Live/official scheme APIs (explicitly future scope per the pitch)
- Nationwide scheme coverage beyond the 3–5 MVP schemes (explicitly future scope per the pitch)
- Multiple roles/workspaces, admin functionality, advanced notification channels (unchanged from v1, still unconfirmed — U6/U8/U10)
- Real partner-application submission ("Apply now") — unchanged from v1, still gated on U7

---

## 20. Devin Implementation Plan (delta from v1 — Phase 2 and Phase 4 change materially)

**Phase 1 (Project setup), 3 (Backend shell), 5 (Frontend), 6 (Integration), 7 (Auth/Demo), 8 (History/Notifications/etc.), 9 (Testing), 10 (UX polish), 11 (Production cleanup): unchanged from v1 §20.**

### Phase 2 — Database *(updated)*

- **Files:** Postgres migrations for all v1 tables **plus** `applicant_profiles`, `schemes`, `scheme_eligibility_rules`, `scheme_finance`, `scheme_documents`, `document_readiness`, `scheme_partners`, and the updated `results` columns (§12); Neo4j schema/constraints for the `Scheme`/`EligibilityRule`/`Finance`/`Document`/`Partner` graph.
- **Tasks:** write a **single seed script** that writes sample scheme data to *both* Postgres and Neo4j together (never independently — §12's sync rule), flagged `is_verified_official = false`; seed the updated demo scenario (§15/16 addition above).
- **Expected output:** migrated Postgres + Neo4j, both queryable and in sync for the seeded sample scheme(s).
- **Tests:** seed idempotency; a query proving Postgres `schemes` and Neo4j `Scheme` nodes agree on IDs/names for every seeded scheme.
- **Completion criteria:** all tables/graph nodes exist; at least one fully-formed sample Scheme DNA record (eligibility + finance + documents + partner) exists in both stores.

### Phase 4 — Core SmartSetu (SamarthSetu) logic *(updated — no longer a placeholder)*

- **Files:** `NLProfileExtractor`, `KnowledgeGraphMatcher`, `RuleEngine`, `ExplanationGenerator`, `PathwayAssembler`, orchestrated by `SchemeMatchingService` (§14).
- **Tasks:** implement each module against its defined interface; wire `POST /api/requests/:id/run` to the real pipeline; implement `PATCH /api/requests/:id/document-readiness`.
- **Expected output:** a real, non-placeholder eligibility result for the seeded sample scheme — extraction → graph shortlist → rule verification → explanation → pathway, all real.
- **Tests:** unit tests per module (especially `RuleEngine` — must be exhaustively tested since it's the auditability guarantee); integration test of the full pipeline against the seeded scheme, asserting a correct pass and a correct fail case (i.e., test with a profile that should be eligible and one that shouldn't).
- **Completion criteria:** the P0 acceptance journey (§21) runs against **real pipeline logic**, not a stub — this is the actual bar v1 left open, now closed structurally (content still depends on U13's real scheme data for production quality).

---

## 21. Definition of Done (updated)

All of v1 §21's items apply unchanged, **plus**:

- [ ] The core pipeline (`NLProfileExtractor → KnowledgeGraphMatcher → RuleEngine → ExplanationGenerator → PathwayAssembler`) runs end-to-end against at least one seeded scheme — no placeholder engine remains in the P0 path
- [ ] Every result with `outcome_type` other than a system failure includes a non-empty `rule_engine_trace`
- [ ] No explanation text asserts eligibility the rule engine did not confirm (spot-checked in testing, §18)
- [ ] All sample/seeded scheme data is labeled `is_verified_official = false` and never presented in the UI as officially verified
- [ ] Result screen shows all four pillars together (eligibility + financial pathway + document readiness + partner routing) for every completed request

---

## 22. Open Decisions (updated — adds domain-specific items to v1's list)

v1's items 1–13 are updated as follows: **#1 (U1) and #2 (U2) are resolved**, removed from the open list. All others (U3–U12) remain open exactly as in v1.

**New open decisions:**

14. **U13 — What are the real 3–5 MVP schemes, and what is their actual sourced eligibility/finance/document/partner data?** This is now the single highest-priority open decision in the whole project — everything else in this document is ready to receive that data the moment it exists.
15. **U14 — Which LLM/NLP provider** will `NLProfileExtractor`/`ExplanationGenerator` actually call?
16. **U15 — Which languages** must multilingual interaction actually support for the MVP demo?
17. **U16 — Confirm OCR/document upload is genuinely out of scope for MVP** (pitch says future scope; confirm the team agrees before Devin builds the self-report-only version).
18. **U17 — Real partner/institution directory** per scheme, once U13 is resolved.
19. **Rule combination logic** — confirm whether real scheme eligibility ever needs OR-groups (e.g., "category A OR category B") beyond the AND-only assumption in `scheme_eligibility_rules` (§12).

---

# DEVIN HANDOFF SUMMARY (v2 — supersedes v1's)

**What's new vs. the previous handoff:** the core domain is now confirmed. Build the real pipeline, not a placeholder.

**Product:** SamarthSetu AI — AI-driven scheme matching for marginalized entrepreneurs. Tagline: "From Eligibility to Access." USP to reflect in UI copy where natural: *"One profile → one intelligent pathway to access."*

**Non-negotiable architecture rule (test this explicitly):** the Rule Engine, not the LLM and not the Neo4j graph query, is the sole authority on eligibility. The LLM's only jobs are (1) extracting a structured profile from free text and (2) explaining a result the rule engine already computed. Every `results` row for a real outcome must carry a `rule_engine_trace`.

**Pipeline to build (Phase 4):**
`NLProfileExtractor → KnowledgeGraphMatcher (Neo4j) → RuleEngine (Postgres, authoritative) → ExplanationGenerator (LLM) → PathwayAssembler`

**Stack (confirmed by the source pitch, not an assumption this time):** React (frontend), Python + FastAPI (backend/API), PostgreSQL (structured data — schemes, rules, finance, documents, partners, requests, users), Neo4j (knowledge graph for candidate matching).

**Data you don't have yet and must get from the team before this is production-real (U13):** the actual 3–5 MVP schemes — their real eligibility rules, financial terms, required documents, and routing partners, sourced from verified official information. Until then, seed clearly-labeled sample data (`is_verified_official = false`) so the full pipeline is demonstrably real and working, just not yet populated with sourced content.

**UX shell:** unchanged from the original UX spec — reuse the full screen set, navigation, design system, component tree, copy rules, and accessibility requirements from v1 of this blueprint (§6–§11, §15–§18 there) exactly as written. Only the Result screen's content changes: it must show eligibility + financial pathway + document readiness + partner routing together, every time.

**P0 acceptance gate:** Landing → Try SamarthSetu → Demo → Dashboard → "Check my eligibility" → complete 4 steps → Processing → Result showing a real (even if sample-data) rule-engine-verified match with explanation, financial pathway, document readiness, and partner routing → visible in History. Under 90 seconds, no developer explanation, per the original tester-timing target.

**Before calling any part of this "done," resolve or clearly re-flag every item in §22 — especially U13, which is the one thing this document cannot supply on its own.**