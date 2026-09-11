# 🎤 Jury Demo Script — SamarthSetu AI (2 minutes)

> **One profile → one intelligent pathway to access.**
> Run `start.bat` first, open **http://localhost:8000/app/**, full-screen the browser.

---

## ⏱ 0:00–0:20 — Landing (the 30-second pitch)

**Say:** "Entrepreneurs don't lack schemes — they lack *their* scheme. SamarthSetu answers: which scheme fits me, why, what money, what documents, what next."

**Click:** nothing yet — point at the trust line under the buttons:

> 🛡️ *The rule engine checks eligibility. AI explains the result.*

---

## ⏱ 0:20–0:35 — Load the demo

**Click:** **Try Demo**

The ready-made applicant loads instantly — **Aarav Patel**, 28, Ahmedabad, food-processing, ₹5,00,000 for equipment — and lands on **Review Your Information**.

**Say:** "Demo applicant, clearly labelled — and it runs the exact same pipeline as a real user."

---

## ⏱ 0:35–0:50 — Review → Check

**Point:** the full profile on one screen + the disclaimer:

> *This result is an eligibility assessment… not an approval or funding guarantee.*

**Click:** **Check My Eligibility**

**Say while stages tick by:** "Five honest stages — profile, candidate schemes via the knowledge graph, the deterministic rule engine, AI explanation, pathway. No fake progress percentages."

---

## ⏱ 0:50–1:20 — The result (the core)

**Point, top to bottom:**

1. **Your Best Match — PMFME (PM Formalisation of Micro Food Processing Enterprises) — ✅ Eligible** — "a *real* government scheme, matched to his exact business"
2. **Why this matches you** — 5 plain-language reasons *(AI explains the rule engine's decision — it never decides it)*
3. **Detailed eligibility** — click to expand the table: *your value vs required vs ✓/✗, straight from the scheme's rules*
4. **How you compare across schemes** — one table, all 5 real schemes: **who qualifies, who doesn't and exactly why** (Stand-Up India: needs SC/ST/woman category; PM SVANidhi: needs street-vending), each row linked to its **official portal**
5. **Financial pathway** — funding need → **35% subsidy ₹1.75L** → **margin ₹50k** → **loan ₹2.75L** → total ₹5L. "Every rupee calculated from scheme data — nothing invented."
6. **Your eligibility overview** — the at-a-glance bar graph: match scores across all schemes (3 green, 2 red) + the assessment summary counts. "One graph, his whole situation."

**Click:** the ✓ next to **Bank Account Details** in **Document readiness** → counter updates.

**Say:** "Readiness is chosen by the user, saved, and reused next check — *marked*, never *verified*."

---

## ⏱ 1:20–1:40 — Next step + intelligence

**Point:** **Your Next Step** — where to go (DIC), why, what to take, and the honest note: *"Prototype routing — external handoff not connected."*

**Click:** **Check Eligibility** → step 3 → paste into the "your own words" box:

```
I am starting a small food business and need around five lakh rupees for equipment.
```

**Click:** **Extract with AI** → the "We understood your situation" screen shows the extracted fields — *each editable, nothing assumed without review*.

**Say:** "Words in, structured profile out — then the user confirms."

---

## ⏱ 1:40–2:00 — Close on robustness

**Click:** **⬇ Download my pathway** (bottom of the result) — a clean printable document opens and offers to save/print as PDF — **including the comparison table and overview**. "The applicant walks in with everything on one page."

**Click:** **History** — every check saved and reopenable.

**Say:** "Alternative flows are built in: no match shows exactly which criteria failed; missing info says which fields; errors never leave a blank screen. The catalogue is five **real government schemes** — PMEGP, PMFME, PM MUDRA, Stand-Up India, PM SVANidhi — summarised from official sources, labelled as prototype data, each linked to its official portal. Rule engine decides, AI explains — **from eligibility to access**."

---

## 🛡️ Q&A cheat sheet

| Likely question | Answer |
|---|---|
| Does AI decide eligibility? | No — deterministic rule engine over scheme data; AI only explains. |
| Are the schemes real? | Yes — 5 real government schemes (PMEGP, PMFME, MUDRA, Stand-Up India, PM SVANidhi), facts summarised from official guidelines and linked to official portals; labelled as prototype summaries to be verified before applying. |
| Real document verification? | No — user self-marks; UI says "marked, not verified". |
| Does it submit applications? | No — routing is explicitly marked as a prototype handoff. |
| Tech stack? | FastAPI + deterministic rule engine + in-memory store (JSON persistence), no-build vanilla JS SPA — runs on any laptop with Python only. |
| Try a failing case? | Set funding need to ₹1 crore → "Not currently eligible" with the failed criterion shown in the comparison table too. |
| How does the best match get chosen? | All schemes are evaluated by the same rule engine; eligible schemes with the highest share of satisfied conditions win — schemes purpose-built for the applicant (category/sector targeting) break ties. |

## ⚠️ Pre-demo checklist
- [ ] `start.bat` run, http://localhost:8000/app/ loads
- [ ] Browser zoomed to 100%+, window full-screen
- [ ] Demo flow clicked once beforehand (results in History are fine — they show persistence)
- [ ] If asked for fresh state: Settings → Reset current profile, History → Clear history
