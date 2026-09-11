# SamarthSetu AI — Final UX/UI Design and Developer Handoff Specification

**Product promise:** From Eligibility to Access  
**USP:** One profile → one intelligent pathway to access  
**Primary action:** Check My Eligibility

---

## 1. Scope and product truth

SamarthSetu AI is an explainable scheme-matching product for marginalized entrepreneurs. It takes a user's situation and applicant profile, checks relevant scheme criteria, explains the strongest match, shows the supported financial pathway, indicates document readiness, and routes the user toward the next appropriate destination.

The confirmed product pipeline is:

```text
User Situation
  ↓
Applicant Profile
  ↓
Scheme Knowledge Graph
  ↓
Deterministic Rule Engine
  ↓
Explainable AI
  ↓
Financial Pathway
  ↓
Document Readiness
  ↓
Partner / Application Routing
  ↓
Next Action
```

### Product boundaries

The interface must not imply that SamarthSetu:

- is an official government portal unless that is true;
- guarantees approval or funding;
- uses AI to make the eligibility decision;
- verifies documents if the MVP only records self-reported readiness;
- submits an application unless submission is actually implemented;
- has live government or partner integrations when the prototype uses seeded data.

The rule engine is the decision source. AI explains structured outputs in simple language. The UI must make this distinction visible without exposing technical implementation details to ordinary users.

---

## 2. Design philosophy

SamarthSetu should feel like a guided bridge, not a generic chatbot, a directory, or an enterprise admin dashboard.

### Experience principles

1. **Situation before scheme** — Start with the person and their need, not a catalogue of scheme names.
2. **One dominant action** — Keep “Check My Eligibility” visually and verbally obvious.
3. **Show the intelligence** — Let the user see the progression from profile to rules to match to next step.
4. **Explain, do not mystify** — Use “We understood your situation” instead of technical AI labels.
5. **Separate decision from explanation** — Structured rules determine the result; AI explains it.
6. **Reveal complexity progressively** — Normal users see a clear answer; jury members can expand technical detail.
7. **Never dead-end** — A no-match or failure state still explains what happened and what can be done.
8. **Trust through control** — Let users review and edit extracted information before checking eligibility.
9. **Financial clarity** — Explain assistance, contribution, and financing structure as a pathway, not an intimidating table.
10. **Honest prototype behavior** — Clearly label demo data and simulated or unsupported actions.

---

## 3. First-time tester mental model

Within the first 30 seconds, the tester should understand:

> SamarthSetu helps entrepreneurs find financial schemes that fit their situation and understand what to do next.

The intended mental sequence is:

```text
“What is this?”
→ A system that helps me find schemes I may qualify for.

“What do I do?”
→ Tell SamarthSetu about my situation.

“What will I get?”
→ A personalized result with eligibility, financial assistance,
  documents, and a next destination.
```

### Target timeline

- **0–5 seconds:** Understand the product category and value.
- **5–15 seconds:** Identify “Check My Eligibility” as the starting point.
- **15–30 seconds:** Understand what information is needed and why.
- **30–60 seconds:** Complete the guided profile.
- **60–90 seconds:** See the best match and understand the first reason.
- **90–120 seconds:** Explore financial pathway, documents, and next step.

---

## 4. Personas

### Primary persona — First-time entrepreneur

A small or early-stage entrepreneur who knows they need financial support but does not know which scheme, criteria, documents, or application channel applies to them.

Needs:

- simple language;
- confidence that the result is relevant;
- visibility into why a scheme matched;
- a clear list of what to prepare next.

Fears:

- choosing the wrong scheme;
- missing a requirement;
- being asked for confusing information;
- assuming a result means approval.

### Secondary persona — Jury / evaluator

A technically aware reviewer who wants to see that the system connects applicant data, structured scheme rules, explainability, finance, documents, and routing in a credible pipeline.

Needs:

- an optional “How SamarthSetu works” explanation;
- expandable rule evidence;
- visible distinction between deterministic checks and AI explanation;
- a complete journey rather than a static slideshow.

### Tertiary persona — Project team / operator

The team member who seeds scheme data, reviews requests, or demonstrates the prototype.

Needs:

- predictable seeded scenarios;
- clear demo labels;
- request statuses that can be understood quickly;
- no hidden state or unexplained buttons.

---

## 5. Information architecture and screen map

### Public experience

1. **Landing** — Explain the product and start the journey.
2. **How it works** — Show the four-stage user-facing pipeline.
3. **Login** — Existing-user access.
4. **Registration** — Minimal account creation if required.
5. **Demo access** — Enter a clearly labeled sample entrepreneur journey.

### Core journey

6. **Dashboard** — Orient the user and make the next action obvious.
7. **Check Eligibility: introduction** — Explain inputs, process, and output.
8. **Step 1: About you** — Age, location, category/community.
9. **Step 2: Your business** — Business type and stage.
10. **Step 3: Your funding need** — Amount and intended use.
11. **Optional: Tell us in your own words** — Natural-language context.
12. **Understanding confirmation** — Review structured attributes extracted from text.
13. **Review your information** — Confirm the complete profile.
14. **Eligibility processing** — Show honest pipeline progress.
15. **Result: Your best match** — Immediate outcome and status.
16. **Why this match** — Rule-based explanation.
17. **Financial pathway** — Assistance, contribution, and financing structure.
18. **Document readiness** — Current checklist and missing items.
19. **Next step / routing** — Partner, institution, department, or supported channel.

### Supporting experience

20. **History** — Saved pathways and previous results.
21. **Request detail** — Timeline and saved result.
22. **Notifications** — Result and request updates.
23. **Profile** — Applicant information.
24. **Settings** — Account, accessibility, and preferences.
25. **Technical credibility layer** — Optional “How SamarthSetu works” explanation.

### Alternative states

- Incomplete profile
- Needs more information
- No confirmed match
- Processing failure
- Session expired
- Empty history
- Search with no results
- Demo data warning

---

## 6. Global navigation

### Desktop

Sidebar order:

1. **Dashboard**
2. **Check Eligibility** — primary highlighted destination
3. **History**
4. **Notifications** with unread count

Secondary:

5. **Profile**
6. **Settings**

Persistent footer:

- **Demo data** badge when applicable
- User menu
- Sign out

### Mobile

Bottom navigation:

- Home
- Check
- History
- More

The “Check” item is the visually strongest item. Notifications, Profile, and Settings appear under More. Do not use a floating button that covers form content.

### Navigation rules

- Use icon plus text for important destinations.
- Use active background, icon treatment, and text—not color alone.
- Preserve the user's position when moving between result sections.
- Show a breadcrumb or compact journey label inside the core flow: `Profile → Review → Result`.
- Avoid Analytics, Reports, Marketplace, or other destinations unless explicitly supported.

---

## 7. Landing page

### Above-the-fold copy

**SamarthSetu AI**  
**From Eligibility to Access**

# Find the financial support that fits your situation.

Tell SamarthSetu about yourself and your business. We’ll help you understand which scheme matches your profile, what support it may offer, what documents you need, and where to go next.

Primary CTA: **Check My Eligibility**  
Secondary CTA: **See How It Works**  
Small tertiary action: **Try Demo**

Trust note:

> Eligibility is checked using structured scheme rules. AI helps explain your result—it does not decide your eligibility.

If using a sample workspace, show a visible badge: **Demo data — not official applicant data**.

### Landing wireframe

```text
┌────────────────────────────────────────────────────────────┐
│ SamarthSetu AI       How it works       Sign in   [Try Demo]│
├────────────────────────────────────────────────────────────┤
│                                                            │
│  From Eligibility to Access                                │
│  Find the financial support that fits your situation.      │
│                                                            │
│  Tell us about yourself and your business. Get a clear     │
│  result showing your match, support, documents, and next   │
│  step.                                                     │
│                                                            │
│  [ Check My Eligibility ]   See How It Works               │
│                                                            │
│  01 Tell us  →  02 Check your fit  →  03 Understand match  │
│  →  04 Know your next step                                │
└────────────────────────────────────────────────────────────┘
```

### Four-step story

**01 — Tell us about you**  
Your business, income, location, category, and financing need.

**02 — We check your fit**  
SamarthSetu compares your profile with structured scheme criteria.

**03 — Understand your match**  
See which scheme fits and why the result appeared.

**04 — Know your next step**  
Review financial support, documents, and the right destination.

### Lower landing sections

1. **The problem** — Financial support can be difficult to navigate when criteria and channels are spread across different places.
2. **The SamarthSetu pathway** — Profile → eligibility → explanation → finance → documents → routing.
3. **Result preview** — A real-looking but clearly labeled demo result, not fake official evidence.
4. **Trust and transparency** — Rule-based eligibility, explainable output, user review, and demo-data disclosure.
5. **How SamarthSetu works** — Technical credibility in plain language.
6. **Final CTA** — “See what fits your situation.”

Do not place Neo4j, NLP, PostgreSQL, or Rule Engine terminology in the hero. Put them in the optional technical section.

---

## 8. Demo mode and authentication

### Recommended entry path

Landing → **Try Demo** → Demo confirmation → Dashboard or guided profile.

Confirmation copy:

# Explore a sample SamarthSetu pathway

You’ll use a pre-filled entrepreneur profile to see how SamarthSetu moves from eligibility to access.

**Demo data — not official applicant data.**

Primary CTA: **Start Demo**  
Secondary: **Enter my own information**

### Demo requirements

- Demo mode must use the real profile → rules → result → pathway screens.
- Do not use a fake slideshow that skips the product pipeline.
- Use a coherent sample persona.
- Keep a persistent **Demo data** label in the header.
- Avoid “Test User”, “Sample 123”, or lorem ipsum.

Suggested sample persona, subject to the actual seeded data:

- Name: **Aarav Patel**
- Location: **Ahmedabad, Gujarat**
- Business: **Small food-processing enterprise**
- Stage: **Early-stage business**
- Funding need: **₹5,00,000**
- Purpose: **Equipment and initial working capital**

Do not present the suggested persona as an official applicant or a guaranteed eligible case. The displayed scheme and values must come from the seeded scheme data.

### Login and registration

Keep authentication secondary to the demo journey. If authentication is required, provide:

- **Continue with Demo** or **Try Demo first**;
- minimal registration fields;
- a clear reason for each required field;
- no forced profile completion before the user understands the product.

---

## 9. Dashboard

The dashboard answers one question:

# What do you want to do?

### Layout

```text
┌─────────────────────────────────────────────────────────────┐
│ Good afternoon, Aarav                         Demo data     │
│ Turn your profile into a clear funding pathway.             │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Start with your situation                               │ │
│ │ Check which financial schemes fit your profile.          │ │
│ │ [ Check My Eligibility ]                                │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Your latest pathway                                         │
│ [Scheme name from seed data]   Eligible / Needs review      │
│ [View result]                                               │
│                                                             │
│ Recent pathways                 What needs attention?       │
│ 1 result ready                 2 documents still needed     │
│ [View history]                  [View checklist]             │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard hierarchy

1. Primary CTA: **Check My Eligibility**
2. Current result or unfinished profile
3. Document readiness summary
4. Previous pathways
5. Notifications
6. Profile and account controls

Avoid meaningless statistics. Useful summaries include:

- “1 pathway ready to review”;
- “2 documents still needed”;
- “Profile 80% complete” only if calculated from real fields;
- “Last checked today”.

### Dashboard microcopy

For a new user:

**Your next step is simple**  
Tell us about your situation and we’ll show you what may fit.

For an unfinished profile:

**You’re halfway there**  
Complete two more sections before we check your eligibility.

For a result-ready user:

**Your pathway is ready**  
Review your match, required documents, and next destination.

---

## 10. Profile collection flow

Never use one giant form. Use a guided, saveable flow with a clear reason for the information.

### Intro screen

# Let’s understand your situation

We’ll use a few details about you, your business, and your funding need to check relevant schemes.

You can review and edit everything before we check your eligibility.

Primary CTA: **Start My Profile**

Trust note: **We only use the information needed for this pathway.**

### Step 1 — About you

Heading: **About you**  
Helper: **These details help us check basic eligibility conditions.**

Fields, only if required by the actual rules:

- Age
- Location/state/district
- Category/community
- Income or household-income range

Microcopy:

- “Why we ask: some schemes use age, location, category, or income conditions.”
- Use selectable ranges where exact values are not needed.
- Never ask for sensitive identity information without a clear purpose.

CTA: **Continue to your business**

### Step 2 — Your business

Heading: **Your business**  
Helper: **Tell us where your business is today.**

Fields:

- Business type
- Business stage
- Existing/new business status
- Sector/category, if required by scheme criteria

Possible options:

- Planning to start
- Recently started
- Operating business
- Expanding an existing business

CTA: **Continue to your funding need**

### Step 3 — Your funding need

Heading: **Your funding need**  
Helper: **This helps us understand which financial pathways may be relevant.**

Fields:

- Amount required
- Purpose of funding
- Preferred or supported financing type, if applicable

Use examples:

- Equipment
- Working capital
- Business setup
- Expansion
- Other supported purpose

CTA: **Continue to review**

### Optional natural-language input

Heading: **Tell us in your own words**  
Helper: **Optional — add context that the structured questions did not capture.**

Placeholder:

> “I run a small business in Gujarat and need funding to buy equipment…”

CTA: **Understand my situation**

Do not force the text field when structured fields are sufficient. The natural-language path must never silently override structured user input.

---

## 11. AI understanding and review

After natural-language input, show an intermediate confirmation screen.

# We understood your situation

We turned your message into a few details that can be checked. Please review them before continuing.

Example attributes:

- Age: 32
- Location: Gujarat
- Business: Small manufacturing
- Stage: New business
- Funding need: ₹5,00,000
- Purpose: Equipment
- Category: [value if provided]

Each attribute must have an **Edit** action. Unknown values must say **Not provided**, not be guessed.

Status copy:

**Some details still need your confirmation.**

Primary CTA: **Confirm and continue**  
Secondary: **Edit information**

### Explainability rule

The AI extraction layer may suggest structured values, but the user remains the source of truth. Store and display whether an attribute was:

- entered directly by the user;
- extracted from the user's text;
- confirmed or edited by the user;
- unknown / not provided.

Do not expose internal labels such as `NLProfileExtractor completed successfully`.

---

## 12. Review step

# Review your information

Before we check your eligibility, make sure everything looks right.

Show four editable profile groups:

1. **About you**
2. **Your business**
3. **Your funding need**
4. **Additional context**

Each group has:

- concise values;
- **Edit** link;
- missing-value indicator if relevant.

### What happens next

After you continue, SamarthSetu will:

1. compare your profile with structured scheme rules;
2. explain the strongest match in plain language;
3. show the supported financial pathway;
4. list document readiness and your next destination.

Primary CTA: **Check My Eligibility**

Supporting copy:

> This result is based on the information you confirm and the scheme rules available in this prototype. It is not an approval or funding guarantee.

---

## 13. Processing experience

The processing screen should make the intelligence visible without falsely claiming backend work.

# Checking your pathway

```text
✓ Understanding your profile
✓ Finding relevant schemes
● Checking eligibility rules
○ Preparing your financial pathway
○ Checking document requirements
○ Finding your next step
```

### State behavior

- Mark a stage complete only when the corresponding backend stage has completed.
- If the prototype runs synchronously, use a short intentional loading transition with truthful labels.
- If a stage is unavailable in the MVP, omit it or label it accurately rather than simulating it.
- Provide a visible recovery path if processing fails.

Supporting message:

**Your profile is being compared with structured scheme criteria. AI will help explain the result after the eligibility check.**

Do not show a fake percentage such as “87% complete” unless the percentage represents a real process.

---

## 14. Result hero experience

This is the most important screen in the product.

The first viewport must immediately show:

# Your best match

### [Actual scheme name from scheme data]

Status badge:

- **Eligible**
- **Not currently eligible**
- **Needs more information**

One-sentence summary:

**This scheme matches your current profile based on the criteria checked.**

If the rule result is not eligible:

**We could not confirm eligibility from the information provided. Here are the conditions that affected the result.**

If information is missing:

**We need a little more information before we can confirm a match.**

Primary CTA changes with state:

- Eligible: **View Your Pathway**
- Needs information: **Complete My Profile**
- Not eligible: **See What Affected the Result**

Never hide the outcome beneath generic metric cards.

### Result screen layout

```text
┌─────────────────────────────────────────────────────────────┐
│ Your best match                                             │
│ [Scheme name]                                               │
│ ✓ Eligible                                                  │
│ This scheme matches your current profile.                   │
│                                                             │
│ [ View Your Pathway ]                                       │
│                                                             │
│ Why this match?                                             │
│ ✓ Age requirement met                                       │
│ ✓ Location requirement met                                 │
│ ✓ Business stage matches                                    │
│                                                             │
│ Financial pathway                                           │
│ ₹X assistance / supported structure                          │
│                                                             │
│ Document readiness                                          │
│ 3 of 5 ready                                                │
│                                                             │
│ Your next step                                              │
│ [Partner / destination]  [View Next Steps]                 │
└─────────────────────────────────────────────────────────────┘
```

### Result sections in order

1. Your Match
2. Why this match?
3. Financial Pathway
4. Document Readiness
5. Your Next Step
6. Technical details / eligibility checks
7. Request metadata and timeline

---

## 15. Eligibility explanation

Heading: **Why this match?**

Intro:

**This result comes from structured eligibility rules. SamarthSetu AI explains the checks in plain language.**

Show positive and negative rule outcomes:

```text
✓ Age requirement met
✓ Income requirement met
✓ Business stage matches
✓ Location requirement met
✓ Funding need falls within supported range
```

For a failed rule:

```text
! Income condition not confirmed
The information provided is above the supported range for this scheme.
```

For missing information:

```text
? Business registration status needed
Add this information to confirm the result.
```

### Progressive disclosure

Default view: 3–5 human-readable reasons.  
Expandable link: **View eligibility checks**

Expanded view may show:

- criterion name;
- user value used;
- required condition;
- outcome;
- source or scheme version if available.

Do not show raw JSON, database IDs, graph nodes, or rule-engine logs to normal users. Those can be exposed in a separate jury/developer panel only if useful.

### AI boundary message

Use this persistent but compact explanation near the result:

> **How this works:** Structured scheme rules determine the eligibility result. AI helps explain the result clearly; it does not make the decision.

---

## 16. Financial pathway

Heading: **Your financial pathway**

Explain the structure as a sequence, not a dense table.

```text
Your funding need
₹5,00,000
      ↓
Scheme assistance
₹X / applicable assistance
      ↓
Applicant contribution
₹X / applicable requirement
      ↓
Financing structure
Loan / subsidy / grant / mixed
      ↓
Next financial step
Review the supported pathway and destination
```

### Financial language rules

- Display only values supported by the scheme data.
- Use “applicable assistance” when the amount depends on a calculation not yet available.
- Explain whether a value is a loan, subsidy, grant, contribution, or combined structure.
- Never call an estimate a confirmed amount.
- Include “subject to scheme rules and final authority review” when appropriate.

Example copy:

**What this could mean:**  
This pathway may combine scheme assistance with an applicant contribution. Review the detailed conditions before taking the next step.

Primary CTA: **See financial details**

---

## 17. Document readiness

Heading: **Your document readiness**

Summary:

**3 of 5 items ready**

List:

```text
✓ Identity document
✓ Address proof
✓ Business plan
○ Income proof
○ Registration document
```

Use actual document names from the scheme data. Do not invent universal requirements.

Summary copy:

**2 documents still needed**

Primary CTA: **See missing documents**

MVP honesty note:

> This checklist reflects the information currently recorded in your profile. It does not mean the documents have been officially verified.

If the MVP only uses self-reporting, use terms such as:

- “marked as ready”;
- “not yet added”;
- “based on your current checklist”.

Avoid:

- “verified”;
- “approved document”;
- “document accepted”.

---

## 18. Partner and application routing

Heading: **Your next step**

Copy:

**Continue through:**  
[Actual partner, institution, department, or supported channel]

**Why you’re being routed here:**  
A short explanation tied to the matched scheme and the next supported action.

Primary CTA: **View Next Steps**

Secondary CTA: **Save this pathway** only if saving is implemented.

Use **Apply Now** only when the system truly supports application submission. Otherwise use:

- View Next Steps
- Open Partner Details
- See Application Channel
- Prepare for Application

Routing card contents:

- destination name;
- destination type;
- reason for routing;
- what the user should take with them;
- official link only if verified and supported;
- disclosure if the prototype does not perform the handoff.

---

## 19. No-match and needs-more-information experiences

### No confirmed match

# We couldn’t confirm a match yet

**Here’s what affected the result.**

Show the relevant failed or missing conditions, for example:

- business stage does not match;
- funding purpose is outside the supported range;
- required location information is missing;
- income condition could not be confirmed.

Then:

### What could improve your pathway?

- Complete missing profile information.
- Review the closest available scheme, if the data supports one.
- Adjust the funding purpose only if it accurately reflects the user's need.

Primary CTA: **Review My Information**  
Secondary CTA: **Explore Closest Match** only if a real ranking exists.

Never show only “No scheme found.”

### Needs more information

# We need a little more information

Tell the user exactly which fields are missing and why they matter.

Primary CTA: **Complete My Profile**

### Closest match

If the system supports ranked results, show:

- best match;
- closest alternative;
- reason the alternative was not selected.

If ranking is not implemented, do not display a fabricated “match score”.

---

## 20. History and request detail

### History page

Heading: **Your pathways**

Each row shows:

- date checked;
- scheme name;
- eligibility status;
- pathway status;
- next available action.

Filters:

- All
- Eligible
- Needs more information
- Not currently eligible
- Documents pending

Search placeholder: **Search schemes or pathways**

Empty state:

# Your pathways will appear here

Check your eligibility to create your first personalized pathway.

CTA: **Check My Eligibility**

### Request detail

Use a timeline:

```text
Profile confirmed       ✓
Eligibility checked     ✓
Result explained        ✓
Documents reviewed      ○
Next step               ○
```

Show the saved result, not just a technical request ID. Keep metadata available in a secondary details area.

---

## 21. Notifications

Useful notifications:

- **Your eligibility result is ready**
- **Your pathway needs more information**
- **You have documents still to prepare**
- **Your saved pathway was updated**

Each notification must contain:

- what changed;
- when it changed;
- related scheme/request;
- link to the relevant screen;
- unread/read state that is not color-only.

Avoid notifications that merely create activity noise.

---

## 22. Profile and settings

### Profile

Show:

- name;
- contact details if supported;
- location;
- applicant attributes;
- business profile summary;
- profile completeness only if calculated from real fields.

Primary action: **Edit Profile**

### Settings

Keep secondary:

- accessibility preferences;
- notification preferences;
- account/session controls;
- privacy/data explanation;
- demo reset if relevant to the prototype.

Do not bury the eligibility journey in settings or make settings a primary navigation item.

---

## 23. Technical credibility layer

Provide an optional section accessible from the landing page, footer, or result details:

# How SamarthSetu works

```text
Applicant Profile
      ↓
Scheme Knowledge Graph
      ↓
Deterministic Rule Engine
      ↓
AI Explanation
      ↓
Financial Pathway
      ↓
Documents
      ↓
Partner Routing
```

Plain-language explanations:

- **Applicant Profile** — Organizes the user's situation into information that can be checked.
- **Scheme Knowledge Graph** — Connects profiles, scheme conditions, support types, documents, and destinations.
- **Rule Engine** — Checks eligibility using structured conditions.
- **AI Explanation** — Turns the result into understandable language.
- **Financial Pathway** — Shows how the supported assistance is structured.
- **Documents** — Identifies readiness and missing preparation items.
- **Partner Routing** — Points toward the next supported channel.

Important distinction:

**The rule engine checks the fit. AI explains the fit.**

This section is for technical credibility and should not interrupt the primary user flow.

---

## 24. Component hierarchy

```text
SamarthSetuApp
├── PublicShell
│   ├── BrandHeader
│   ├── LandingHero
│   ├── JourneySteps
│   ├── TrustNote
│   └── TechnicalCredibilitySection
├── AuthShell
│   ├── LoginForm
│   ├── RegistrationForm
│   └── DemoEntry
└── AppShell
    ├── Sidebar / MobileNavigation
    ├── TopBar
    │   ├── Breadcrumbs / JourneyLabel
    │   ├── DemoDataBadge
    │   ├── NotificationButton
    │   └── UserMenu
    └── RouteContent
        ├── Dashboard
        │   ├── WelcomeHeader
        │   ├── PrimaryActionPanel
        │   ├── LatestPathway
        │   ├── DocumentReadinessSummary
        │   └── ActivitySummary
        ├── EligibilityFlow
        │   ├── FlowIntro
        │   ├── StepIndicator
        │   ├── AboutYouStep
        │   ├── BusinessStep
        │   ├── FundingNeedStep
        │   ├── FreeTextStep
        │   ├── UnderstandingConfirmation
        │   ├── ReviewStep
        │   └── ProcessingState
        ├── ResultExperience
        │   ├── ResultHero
        │   ├── EligibilityStatus
        │   ├── MatchReasonList
        │   ├── EligibilityChecksDisclosure
        │   ├── FinancialPathway
        │   ├── DocumentReadiness
        │   ├── RoutingCard
        │   └── RequestTimeline
        ├── History
        ├── Notifications
        ├── Profile
        └── Settings
```

### Reusable components

- Button
- Input, Select, RadioGroup, Checkbox
- FieldGroup
- StepIndicator
- ProfileSummaryCard
- StatusBadge
- RuleCheckRow
- FinancialPathwayStep
- DocumentChecklist
- RoutingCard
- Timeline
- DisclosurePanel
- Toast
- Alert
- EmptyState
- LoadingState
- ErrorState
- DemoDataBanner

Every status component must accept text, icon, and semantic state. Color alone is never sufficient.

---

## 25. Design system

### Visual character

Trustworthy + intelligent + modern + accessible. The product should feel civic and human without copying a government portal, and professional without looking like a generic banking dashboard.

### Color tokens

- `ink-900`: `#17212B` — primary text
- `ink-700`: `#344563` — headings and strong secondary text
- `slate-600`: `#52606D` — supporting text
- `canvas`: `#F7F9FB` — page background
- `surface`: `#FFFFFF` — panels
- `blue-700`: `#145DA0` — primary action
- `blue-900`: `#0E3A5D` — deep emphasis
- `blue-050`: `#EAF3FA` — information background
- `saffron-600`: `#D9822B` — guided attention, used sparingly
- `green-700`: `#1F7A53` — eligible/success
- `amber-700`: `#9A6700` — needs information
- `red-700`: `#B42318` — error/not eligible warning
- `border`: `#D9E2EC` — dividers and field borders

Use semantic labels plus icons:

- Eligible: check icon + “Eligible”
- Needs information: question/alert icon + “Needs more information”
- Not currently eligible: information icon + explanatory text
- Processing: progress indicator + “Checking”

### Typography

Recommended:

- Display/headings: Manrope, Segoe UI, sans-serif
- Body: Inter, Segoe UI, sans-serif

Scale:

- Page title: 32/40, 700
- Hero title: 44/52 desktop, 34/42 mobile, 750
- Section title: 22/30, 700
- Panel title: 17/24, 650
- Body: 15/24
- Small/helper: 13/20
- Button: 14/20, 650

### Spacing and shape

- 4px base unit
- 20px mobile page padding
- 32px desktop page padding
- 24px panel padding
- 16px field gaps
- 32px section gaps
- 8px controls, 10px panels
- 1px borders
- restrained shadows only for overlays
- visible 3px focus ring

### Buttons

Primary:

- “Check My Eligibility”
- “View Your Pathway”
- “View Next Steps”

Secondary:

- “See How It Works”
- “Review My Information”
- “Edit”
- “Back”

Avoid generic “Submit”, “Execute”, “Process”, and “Apply Now” unless technically accurate.

### Motion

Use only purposeful transitions:

- step-to-step form movement;
- status update;
- result reveal;
- disclosure expansion.

Respect reduced-motion preferences. Do not use decorative particle effects, excessive gradients, or fake AI animations.

---

## 26. Empty, loading, success, and error states

### Empty history

**Your pathways will appear here**  
Check your eligibility to create your first personalized pathway.

CTA: **Check My Eligibility**

### Incomplete profile

**Complete your profile to check your eligibility**  
We still need: [field/section].

CTA: **Continue My Profile**

### AI extraction uncertainty

**We couldn’t confidently understand part of your message.**  
Review the highlighted details before continuing.

CTA: **Review Details**

### Processing failure

**We couldn’t complete the pathway check.**  
Your confirmed information is still available. Try again or return to your profile.

CTA: **Try Again**  
Secondary: **Review My Profile**

Only say information is saved if the implementation actually persists it.

### Session expired

**Your session has ended**  
Sign in again to continue.

CTA: **Sign In**

### Result success

**Your pathway is ready**  
Review your match, financial support, documents, and next destination.

### No search results

**No pathways match your search**  
Try another scheme name or clear the filters.

CTA: **Clear Filters**

---

## 27. Accessibility requirements

- WCAG AA contrast for text and interactive controls.
- Semantic heading hierarchy.
- Visible keyboard focus state.
- Labels for every input; never rely on placeholder text alone.
- Error messages adjacent to the field and summarized above the form.
- Live-region announcement for processing, success, and failure states.
- Progress indicators with text labels such as “Step 2 of 4”.
- No status communicated by color alone.
- Touch targets of at least 44px where possible.
- Responsive layout at desktop, tablet, and mobile widths.
- Support browser zoom to 200% without hiding the main CTA.
- Respect reduced-motion settings.
- Do not use unexplained icons as primary controls.
- Ensure expanded rule explanations are keyboard accessible.

---

## 28. Responsive behavior

### Desktop

- Two-column result layout where the primary result and next action remain visible together.
- Fixed sidebar.
- Profile form uses a focused content column, not edge-to-edge fields.
- Financial pathway may use a horizontal sequence.

### Tablet

- Collapsible sidebar.
- Stack financial pathway steps when horizontal space becomes constrained.
- Keep the primary CTA visible near the bottom of the active section.

### Mobile

- Single-column journey.
- Step indicator becomes compact text plus progress line.
- Stack result sections in the intended order.
- Use a vertical financial pathway.
- Keep “Check My Eligibility” or the current primary CTA full-width.
- Do not shrink dense tables; convert them to labeled rows or stacked cards.
- Keep Demo data and trust notes readable rather than hiding them in tooltips.

---

## 29. Copy system

### Core phrases

- From Eligibility to Access
- Check My Eligibility
- Tell us about your situation
- We understood your situation
- Review your information
- Checking your pathway
- Your best match
- Why this match?
- Your financial pathway
- Your document readiness
- Your next step
- View Your Pathway
- View Next Steps

### Avoid

- Submit Data
- Execute Request
- AI Decision Complete
- Scheme Confidence: 94%
- Apply Now, unless supported
- Government Approved, unless true
- Document Verified, unless true
- No scheme found
- We guarantee your eligibility
- Powered by a complex AI engine

### Trust microcopy

**Rule-based result**  
Eligibility is checked using structured scheme criteria.

**AI explanation**  
AI helps explain the result in simple language. It does not decide eligibility.

**Demo disclosure**  
Demo data — not official applicant data.

**Document disclosure**  
Based on your current checklist; documents are not officially verified here.

**Routing disclosure**  
This prototype shows the next supported destination. It does not submit an application unless explicitly stated.

---

## 30. Curiosity and discovery strategy

Use genuine progressive discovery:

### After profile

**Let’s see what fits your situation.**

### During processing

**We’re checking your profile against structured scheme criteria.**

### After result

**Why did this scheme match?**

### After explanation

**What could this mean financially?**

### After financial pathway

**What do I need to prepare?**

### After document readiness

**Where do I go next?**

Each question should be answered by the next visible section. Do not use hidden surprises, fake scores, or manipulative countdowns.

---

## 31. Final user-flow diagram

```text
LANDING
  │
  ├── See How It Works ──→ Product story / technical credibility
  │
  └── Check My Eligibility / Try Demo
          │
          ▼
      DEMO / LOGIN
          │
          ▼
       DASHBOARD
          │
          ▼
   CHECK ELIGIBILITY INTRO
          │
          ▼
       ABOUT YOU
          │
          ▼
      YOUR BUSINESS
          │
          ▼
    YOUR FUNDING NEED
          │
          ├── Optional free-text context
          │          │
          │          ▼
          │   UNDERSTANDING CONFIRMATION
          │
          ▼
    REVIEW INFORMATION
          │
          ▼
  CHECK MY ELIGIBILITY
          │
          ▼
    PROCESSING PIPELINE
          │
          ├── Failure → Recovery / Try again
          │
          ├── Missing information → Complete profile
          │
          ▼
       RESULT
          │
          ├── Eligible → Why match → Financial pathway
          │                         → Documents → Routing
          │
          ├── Needs information → Complete missing fields
          │
          └── No confirmed match → What affected result
                                     → Closest supported path, if real
          │
          ▼
       NEXT ACTION
          │
          ▼
       HISTORY / NOTIFICATIONS
```

---

## 32. Developer handoff notes

### Route structure

Suggested routes:

```text
/
/how-it-works
/login
/register
/demo
/app
/app/check-eligibility
/app/check-eligibility/about-you
/app/check-eligibility/business
/app/check-eligibility/funding
/app/check-eligibility/understanding
/app/check-eligibility/review
/app/check-eligibility/processing
/app/result/:id
/app/result/:id/why
/app/result/:id/financial-pathway
/app/result/:id/documents
/app/result/:id/next-step
/app/history
/app/history/:id
/app/notifications
/app/profile
/app/settings
```

### State model

The frontend should represent these explicit states:

```text
idle
collecting_profile
extracting_profile
awaiting_confirmation
review_ready
processing_profile
checking_rules
building_explanation
building_pathway
result_ready
needs_information
not_currently_eligible
no_match
failed
```

Do not infer a success state merely because an HTTP request returned 200. Use the backend response status and result payload.

### Result payload concepts

The UI should be able to render, where supported:

- applicant profile;
- confirmed/extracted attribute provenance;
- matched scheme;
- eligibility status;
- rule outcomes;
- explainable reasons;
- financial pathway values and types;
- document checklist and readiness status;
- routing destination;
- next action;
- processing/request status;
- timestamps and history metadata.

### Data honesty rules

- Unknown value → “Not provided” or “Needs information”.
- Unsupported value → omit the section rather than fabricate it.
- Missing route → “Next destination not available in this prototype.”
- Unverified document → “Marked as ready” rather than “Verified”.
- Non-submitted application → “View next steps” rather than “Application submitted”.

### P0 implementation order

1. Landing page and Demo entry
2. Dashboard with primary CTA
3. Guided profile flow
4. Natural-language understanding confirmation, if supported
5. Review screen
6. Honest processing state
7. Result hero and eligibility reasons
8. Financial pathway
9. Document readiness
10. Next-step routing
11. History and saved result

### P1

- Login and registration polish
- Notifications
- Profile and settings
- Search/filter
- Responsive refinements
- Expanded technical credibility layer

### P2

- Additional roles
- Rich analytics
- Multiple partner integrations
- Live application submission
- Advanced document verification

Do not polish P2 before the core journey is understandable and complete.

---

## 33. UX acceptance criteria

The design is successful only if:

- a new tester understands SamarthSetu within seconds;
- “Check My Eligibility” is the obvious first action;
- the user understands why each requested field matters;
- the profile is divided into short, understandable steps;
- natural-language extraction is reviewable and editable;
- unknown values are not guessed;
- the review step appears before rule evaluation;
- the processing experience reflects actual backend stages honestly;
- the first result viewport clearly shows the scheme and status;
- eligibility is visibly separate from AI explanation;
- the tester can answer why the match occurred;
- the financial pathway is understandable without reading a dense table;
- document readiness is clearly distinguished from document verification;
- the tester knows where to go next;
- no-match results explain what affected the outcome;
- Demo mode is easy and clearly labeled;
- history contains meaningful saved pathways;
- notifications link to relevant results;
- no page has dead-end buttons;
- no unsupported government, partner, approval, or verification claims are made;
- keyboard, mobile, contrast, and reduced-motion behavior are considered;
- the complete journey works without developer narration.

### Five-minute usability test

Ask a person who has not seen the project to:

1. Explain what SamarthSetu does.
2. Start the eligibility check.
3. Explain why a profile field is being requested.
4. Correct one extracted value.
5. Find the best match.
6. Explain why the scheme matched.
7. Find the financial support information.
8. Identify missing documents.
9. Identify where to go next.

Success means the tester completes the core journey without being told which button to press or what a result means.

---

## 34. Final design decision

SamarthSetu must make this transformation visible:

```text
I tell SamarthSetu about myself.
          ↓
It understands my profile.
          ↓
It checks my eligibility using structured rules.
          ↓
It explains my match in simple language.
          ↓
It shows what financial support may be available.
          ↓
It tells me what documents I need to prepare.
          ↓
It tells me where to go next.
```

The product is not a generic AI chatbot, a scheme directory, or a dashboard full of disconnected cards. It is one guided, explainable pathway from a user's situation to a credible next action.
