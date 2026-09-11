# SamarthSetu AI — From Eligibility to Access

AI-assisted scheme matching and access pathway prototype for first-time and
underserved entrepreneurs.

> **One profile → one intelligent pathway to access.**

**The rule engine checks the fit. AI explains the fit.**
AI never decides eligibility — the deterministic Rule Engine is the authority.

---

## Quick start (localhost)

Requires only **Python 3.9+**. No Node.js, no PostgreSQL, no Docker.

### Windows

```bat
start.bat
```

### macOS / Linux

```bash
./start.sh          # or: bash start.sh
```

Then open **http://localhost:8000/app/**

- **UI:** http://localhost:8000/app/
- **API health:** http://localhost:8000/api/health
- **API docs (Swagger):** http://localhost:8000/docs

The first run creates a virtualenv and installs 4 packages (fastapi, uvicorn,
pydantic, python-dotenv) — about 30 seconds. Subsequent starts are instant.

### Manual start (equivalent)

```bash
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows
# .venv/bin/pip install -r requirements.txt       # macOS/Linux
.venv/Scripts/python -m uvicorn app.main:app --port 8000
```

---

## What this prototype does

A first-time user can, in under 2 minutes:

1. **Tell us about yourself** — 3 guided steps (About you → Your business →
   Funding need), plus an optional natural-language box
   ("Tell us about your situation in your own words").
2. **We understood your situation** — AI extracts structured fields from free
   text; every field is editable and labelled (Entered by you / Extracted /
   Confirmed / Not provided). Confirmed structured data is the source of truth.
3. **Review** — full profile review with disclaimer before checking.
4. **Check eligibility** — meaningful processing stages (no fake percentages).
5. **Your Best Match** — Eligible / Not currently eligible / Needs more
   information, with 3–5 human-readable reasons.
6. **Detailed eligibility** — per-criterion table (your value vs required vs
   result), driven entirely by scheme data.
7. **How you compare across schemes** — side-by-side table of every assessed
   scheme: qualifies or not, exactly why (with the failed criteria), a match
   score, and a link to each scheme's official portal.
8. **Financial pathway** — funding need → scheme assistance → contribution →
   financing structure → next financial action, with loan/grant/subsidy
   clearly distinguished. Values are computed from scheme data only.
9. **Your eligibility overview** — an at-a-glance graph (match score per
   scheme, colour-coded by status) plus assessment summary counts.
10. **Document readiness** — the user marks each document ready themselves
   ("3 / 5 ready · marked as ready by you"). Choices are saved, reused in the
   next check, and reflected in history — never auto-set, never "verified".
11. **Your next step** — where to go, why, what to take, and the action.
12. **History** — every check is saved and reopenable.

Alternative flows are handled: no match (shows failed conditions + "modify &
retry"), missing information (shows exactly which fields), and errors
(explains the problem + retry — never a blank screen).

---

## Try the demo

From the landing page, click **Try Demo**. It loads the ready-made demo
applicant:

- **Aarav Patel** — Ahmedabad, 28
- Small food-processing business, early-stage
- Funding need: ₹5,00,000 for equipment

The demo uses the **same eligibility pipeline** as manual users (labelled
**Demo Applicant** in the UI).

---

## Architecture

```
React-style SPA (no-build vanilla JS, served by FastAPI)
        ↓  fetch /api/*
FastAPI backend
        ↓
Scheme Matching Service (orchestrator)
 ├─ NLP Profile Extractor      (deterministic; optional LLM key)
 ├─ Knowledge Graph Matcher    (in-memory graph → candidate schemes)
 ├─ Deterministic Rule Engine  (authority for eligibility)
 ├─ Explanation Generator      (converts rule results to human language)
 ├─ Comparison Builder         (cross-scheme comparison table + overview graph data)
 └─ Pathway Assembler          (finance + documents + next step)
        ↓
In-memory store + JSON persistence (backend/data/results.json)
```

Why no-build frontend? The whole demo runs on any machine with Python alone —
important for localhost testing and SIH presentation reliability.

### API

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/profile/extract` | Extract profile fields from natural language |
| POST | `/api/eligibility/check` | Full pipeline: match → rules → explain → pathway |
| GET  | `/api/schemes` | List real schemes (with authority + official portal links) |
| GET  | `/api/schemes/{id}` | Scheme detail |
| GET  | `/api/results/{id}` | Reopen a saved result |
| GET/PATCH | `/api/documents` | The user's own document readiness marks (self-marked, never verified) |
| GET  | `/api/history` | Previous eligibility checks |
| DELETE | `/api/history` | Clear history |
| POST | `/api/demo/start` | Load the demo applicant |
| GET  | `/api/knowledge-graph` | Graph view used for candidate discovery |
| GET  | `/api/health` | Health check |

### Project layout

```
├── start.bat / start.sh        # one-command launchers
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app: API + static frontend
│   │   ├── store.py            # 5 real schemes (verified summaries), demo applicant, results
│   │   ├── utils.py            # money/date formatting helpers
│   │   ├── rules/rule_engine.py
│   │   ├── services/           # extractor, matcher, explainer, comparison, pathway, orchestrator
│   │   └── api/                # health, profile, core routes
│   └── requirements.txt        # fastapi, uvicorn, pydantic, python-dotenv
└── frontend/
    ├── index.html              # SPA entry (served at /app/)
    └── static/                 # css + js served at /static/
```

---

## Scheme data — real schemes, prototype summaries

The catalogue contains **five real government schemes**, each with identity,
eligibility rules, finance, documents, partner and an official-source link:

| Scheme | What it offers | Official portal |
|---|---|---|
| **PMEGP** (Ministry of MSME / KVIC) | Bank loan + 15–35% margin-money subsidy, new micro units, project cost up to ₹50 lakh (manufacturing) / ₹20 lakh (service) | kviconline.gov.in/pmegpeportal |
| **PMFME** (Ministry of Food Processing Industries) | 35% credit-linked subsidy capped at ₹10 lakh for micro food-processing units | pmfme.mofpi.gov.in |
| **PM MUDRA / PMMY** (Dept. of Financial Services) | Collateral-free loans ₹50k → ₹20 lakh (Shishu/Kishore/Tarun/Tarun Plus), non-farm micro enterprises | mudra.org.in |
| **Stand-Up India** (Dept. of Financial Services / SIDBI) | Bank loans ₹10 lakh–₹1 crore for SC/ST & women greenfield entrepreneurs | standupmitra.in |
| **PM SVANidhi** (Ministry of Housing & Urban Affairs) | Collateral-free ₹10k/₹20k/₹50k tranches + 7% interest subsidy for street vendors | pmsvanidhi.mohua.gov.in |

Facts are summarised from official scheme documents and portals and labelled
**"Prototype Data — real schemes, summarised from official sources"** in the
UI. They must be verified on the official portals before applying; this
prototype is not affiliated with any government agency.

The Rule Engine evaluates structured conditions from this data only
(`age >=`, `stage in`, `funding_need between`, `category in`, …). Eligibility
logic lives **only** in the backend — never in the frontend.

## Honest-product rules (enforced in the UI)

- No claims of guaranteed approval/funding, government ownership, live
  government integration, verified documents, or actual submission.
- Documents are "marked as ready", not "verified".
- Routing shows: *"Prototype routing — external application handoff is not
  connected in this demo."*
- Disclaimer before every check: *"This result is an eligibility assessment
  based on the information provided. It is not an approval or funding
  guarantee."*

## Optional: LLM-assisted extraction

Set `OPENAI_API_KEY` in `backend/.env` to enable LLM extraction/explanation.
Leave it empty and the offline deterministic extractor is used — the demo
works with zero external services either way.

## Notes

- Prototype/demo data only — not affiliated with any government agency.
- Results persist to `backend/data/results.json`; delete it to reset history.
