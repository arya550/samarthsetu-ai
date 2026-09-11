/* ==========================================================================
   SamarthSetu AI — single-page app (no build step required)
   ========================================================================== */

/* ------------------------------------------------------------------ API */
const API = {
  async req(path, opts = {}) {
    const res = await fetch(`/api${path}`, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) {
      let detail = `Request failed (${res.status})`;
      try { const body = await res.json(); if (body.detail) detail = body.detail; } catch { /* ignore */ }
      throw new Error(detail);
    }
    return res.json();
  },
  demoStart: () => API.req("/demo/start", { method: "POST" }),
  extract: (description) => API.req("/profile/extract", { method: "POST", body: JSON.stringify({ description }) }),
  check: (payload) => API.req("/eligibility/check", { method: "POST", body: JSON.stringify(payload) }),
  schemes: () => API.req("/schemes"),
  result: (id) => API.req(`/results/${id}`),
  history: () => API.req("/history"),
  clearHistory: () => API.req("/history", { method: "DELETE" }),
  updateDocStates: (document_states) => API.req("/documents", { method: "PATCH", body: JSON.stringify({ document_states }) }),
};

/* --------------------------------------------------------------- constants */
const FIELD_LABELS = {
  name: "Name", age: "Age", location: "Location", category: "Category / community",
  income: "Annual income", business_type: "Business type", business_stage: "Business stage",
  sector: "Sector", business_status: "Business status", funding_need: "Funding need",
  funding_purpose: "Funding purpose", financing_type: "Financing preference",
};
const VALUE_LABELS = {
  general: "General", sc: "SC (Scheduled Caste)", st: "ST (Scheduled Tribe)", obc: "OBC",
  minority: "Minority", women: "Woman entrepreneur",
  early_stage: "Early-stage", existing: "Existing business", idea_stage: "Idea stage",
  food_processing: "Food processing", manufacturing: "Manufacturing", services: "Services",
  retail: "Retail / shop", trading: "Trading", agriculture: "Agriculture / farm", technology: "Technology",
  equipment: "Equipment / machinery", working_capital: "Working capital", setup: "Business setup",
  expansion: "Expansion", marketing: "Marketing",
  loan: "Loan", grant: "Grant", subsidy: "Subsidy", mixed: "Loan + subsidy mix", any: "No preference",
  registered: "Registered", not_registered: "Not yet registered",
};
const CATEGORY_OPTS = [["general", "General"], ["sc", "SC"], ["st", "ST"], ["obc", "OBC"], ["minority", "Minority"], ["women", "Woman entrepreneur"]];
const BTYPE_OPTS = [["food_processing", "Food processing"], ["manufacturing", "Manufacturing"], ["services", "Services"], ["retail", "Retail / shop"], ["trading", "Trading"], ["agriculture", "Agriculture"], ["technology", "Technology"]];
const STAGE_OPTS = [["early_stage", "Early-stage (starting)"], ["existing", "Existing business"]];
const SECTOR_OPTS = BTYPE_OPTS;
const BSTATUS_OPTS = [["not_registered", "Not yet registered"], ["registered", "Registered"]];
const PURPOSE_OPTS = [["equipment", "Equipment / machinery"], ["working_capital", "Working capital"], ["setup", "Business setup"], ["expansion", "Expansion"], ["marketing", "Marketing"]];
const FIN_OPTS = [["loan", "Loan"], ["grant", "Grant"], ["subsidy", "Subsidy"], ["mixed", "Loan + subsidy mix"], ["any", "No preference"]];
const PROFILE_FIELDS = ["name", "age", "location", "category", "income", "business_type", "business_stage", "sector", "business_status", "funding_need", "funding_purpose", "financing_type"];
const STATUS_LABEL = { eligible: "Eligible", not_currently_eligible: "Not currently eligible", needs_more_information: "Needs more information", no_match: "No match" };
const STATUS_CHIP = { eligible: "chip-green", not_currently_eligible: "chip-red", needs_more_information: "chip-amber", no_match: "chip-gray" };

/* ------------------------------------------------------------------ state */
const state = {
  profile: null,
  sources: {},        // field -> 'entered' | 'extracted' | 'confirmed'
  nlDescription: "",
  demo: false,
  lastResultId: null,
  step: 1,
};
try {
  const saved = JSON.parse(sessionStorage.getItem("ss_state") || "null");
  if (saved) Object.assign(state, saved);
} catch { /* fresh start */ }
function persist() { sessionStorage.setItem("ss_state", JSON.stringify(state)); }

/* ------------------------------------------------------------- utilities */
const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const has = (v) => v !== null && v !== undefined && v !== "";

function money(amount) {
  if (!has(amount)) return "—";
  const n = Number(amount);
  if (Number.isNaN(n)) return esc(amount);
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2).replace(/\.?0+$/, "")} crore`;
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(2).replace(/\.?0+$/, "")} lakh`;
  return `₹${n.toLocaleString("en-IN")}`;
}
function label(field, value) {
  if (!has(value)) return "Not provided";
  if (["funding_need", "income"].includes(field)) return money(value);
  return esc(VALUE_LABELS[value] ?? value);
}
function timeAgo(iso) {
  if (!iso) return "";
  const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return "just now";
  if (s < 3600) return `${Math.floor(s / 60)} min ago`;
  if (s < 86400) return `${Math.floor(s / 3600)} hr ago`;
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short" });
}
function toast(msg) {
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = msg;
  $("#toastHost").appendChild(el);
  setTimeout(() => el.remove(), 3200);
}
function sourceChip(field) {
  const s = state.sources[field];
  if (!has(state.profile?.[field])) return `<span class="chip chip-gray">Not provided</span>`;
  if (s === "extracted") return `<span class="chip chip-violet">Extracted</span>`;
  if (s === "confirmed") return `<span class="chip chip-green">Confirmed</span>`;
  return `<span class="chip chip-blue">Entered by you</span>`;
}

/* --------------------------------------------------------- notifications */
const NOTIF_KEY = "ss_notifications";
function getNotifs() { try { return JSON.parse(localStorage.getItem(NOTIF_KEY) || "[]"); } catch { return []; } }
function pushNotif(title, resultId) {
  const list = getNotifs();
  list.unshift({ id: Date.now(), title, resultId, read: false, at: new Date().toISOString() });
  localStorage.setItem(NOTIF_KEY, JSON.stringify(list.slice(0, 30)));
  renderBell();
}
function markAllRead() {
  localStorage.setItem(NOTIF_KEY, JSON.stringify(getNotifs().map((n) => ({ ...n, read: true }))));
  renderBell();
}
function unreadCount() { return getNotifs().filter((n) => !n.read).length; }
function renderBell() {
  const n = unreadCount();
  $("#bellCount").textContent = n;
  $("#bellCount").classList.toggle("hidden", n === 0);
  const items = getNotifs();
  $("#notifPanel").innerHTML = `
    <div class="notif-head"><b>Notifications</b><button id="notifClear">Mark all read</button></div>
    ${items.length === 0
      ? `<div class="notif-empty">Nothing yet. Run an eligibility check to see updates here.</div>`
      : items.map((it) => `
        <div class="notif-item" data-result="${esc(it.resultId || "")}">
          ${esc(it.title)}
          <span class="when">${esc(timeAgo(it.at))}</span>
        </div>`).join("")}`;
}
document.addEventListener("click", (e) => {
  const panel = $("#notifPanel");
  if (!panel.classList.contains("hidden") && !e.target.closest(".bell-wrap")) panel.classList.add("hidden");
  const item = e.target.closest(".notif-item[data-result]");
  if (item && item.dataset.result) { location.hash = `#/result/${item.dataset.result}`; panel.classList.add("hidden"); }
  if (e.target.id === "notifClear") markAllRead();
});
$("#bellBtn").addEventListener("click", () => $("#notifPanel").classList.toggle("hidden"));

/* ----------------------------------------------------------------- theme */
const THEME_KEY = "ss_theme";
function applyTheme(t) { document.documentElement.dataset.theme = t; $("#themeIcon").textContent = t === "dark" ? "☀️" : "🌙"; localStorage.setItem(THEME_KEY, t); }
applyTheme(localStorage.getItem(THEME_KEY) || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
$("#themeBtn").addEventListener("click", () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));

/* ---------------------------------------------------------------- router */
const routes = {
  "": renderLanding, landing: renderLanding, how: renderHow,
  dashboard: renderDashboard, check: renderCheck, understanding: renderUnderstanding,
  review: renderReview, processing: renderProcessing,
  result: renderResult, history: renderHistory, schemes: renderSchemes, settings: renderSettings,
};
function navigate() {
  const hash = location.hash.replace(/^#\//, "");
  const [name, param] = hash.split("/");
  const view = routes[name] || renderNotFound;
  document.querySelectorAll("[data-nav]").forEach((a) => a.classList.toggle("active", a.dataset.nav === name));
  $("#demoBadge").classList.toggle("hidden", !state.demo);
  window.scrollTo(0, 0);
  view(param);
}
addEventListener("hashchange", navigate);

/* ------------------------------------------------------------- landing */
function renderLanding() {
  $("#main").innerHTML = `
    <section class="hero">
      <div class="kicker"><span class="chip chip-blue">AI-assisted scheme matching · Prototype</span></div>
      <h1>Find the financial support that fits your situation.</h1>
      <p class="sub">Tell us about yourself once. SamarthSetu checks which scheme you actually qualify for, explains why, and shows you the pathway to access.</p>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="#/check">Check My Eligibility</a>
        <a class="btn btn-secondary btn-lg" href="#/how">See How It Works</a>
        <button class="btn btn-outline btn-lg" id="tryDemo">Try Demo</button>
      </div>
      <div class="trust-line">🛡️ The rule engine checks eligibility. AI explains the result.</div>
    </section>

    <div class="flow-cards">
      <div class="card flow-card"><div class="fc-icon">📝</div><b>One profile</b><p>Three short steps — about you, your business, your funding need.</p></div>
      <div class="card flow-card"><div class="fc-icon">⚖️</div><b>Deterministic check</b><p>A rule engine evaluates your profile against scheme criteria. No guesswork.</p></div>
      <div class="card flow-card"><div class="fc-icon">💡</div><b>Explained result</b><p>Plain-language reasons for why you match — or what's missing.</p></div>
      <div class="card flow-card"><div class="fc-icon">🧭</div><b>Pathway to access</b><p>Financial pathway, document readiness and your concrete next step.</p></div>
    </div>

    <div class="card section-gap card-quiet">
      <div class="callout info">
        <span aria-hidden="true">ℹ️</span>
        <span><strong>Prototype notice:</strong> all scheme data in this demo is labelled
        <em>Demo Data / Prototype Data</em>. Results are eligibility assessments based on the information
        you provide — not approvals or funding guarantees, and no application is submitted.</span>
      </div>
    </div>`;
  $("#tryDemo").addEventListener("click", tryDemo);
}

function renderHow() {
  $("#main").innerHTML = `
    <h1>How SamarthSetu works</h1>
    <p class="mb-2">One profile → one intelligent pathway to access.</p>
    <div class="card">
      <div class="hiw-steps">
        <div class="hiw-step"><div class="n">1</div><div><b>You describe your situation</b><p>Three short steps, or one sentence in your own words — "I'm starting a food business and need ₹5 lakh for equipment."</p></div></div>
        <div class="hiw-step"><div class="n">2</div><div><b>We build your applicant profile</b><p>Everything is shown back to you, field by field, and you confirm it. Confirmed information is the final source of truth.</p></div></div>
        <div class="hiw-step"><div class="n">3</div><div><b>The rule engine checks eligibility</b><p>Deterministic rules from each scheme's data decide eligibility. The engine — not AI — is the authority.</p></div></div>
        <div class="hiw-step"><div class="n">4</div><div><b>AI explains the result</b><p>You get plain-language reasons, a detailed criteria table, and nothing hidden.</p></div></div>
        <div class="hiw-step"><div class="n">5</div><div><b>You see the pathway</b><p>Financial structure, document readiness, and exactly where to go next.</p></div></div>
      </div>
    </div>
    <div class="btn-row mt-2">
      <a class="btn btn-primary" href="#/check">Check My Eligibility</a>
      <button class="btn btn-outline" id="tryDemo2">Try Demo instead</button>
    </div>`;
  $("#tryDemo2").addEventListener("click", tryDemo);
}

/* ----------------------------------------------------------------- demo */
async function tryDemo() {
  try {
    const res = await API.demoStart();
    state.profile = res.applicant;
    state.sources = Object.fromEntries(PROFILE_FIELDS.map((f) => [f, "entered"]));
    state.nlDescription = res.applicant.natural_language_description || "";
    state.demo = true;
    state.lastResultId = null;
    persist();
    toast("Demo applicant loaded: Aarav Patel");
    location.hash = "#/review";
    if (location.hash === "#/review") navigate();
  } catch (err) { toast(`Could not load demo: ${err.message}`); }
}

/* ------------------------------------------------------------ dashboard */
async function renderDashboard() {
  $("#main").innerHTML = `<div class="spinner"></div><p class="text-center muted">Loading your dashboard…</p>`;
  let latest = null, history = [];
  try {
    const h = await API.history();
    history = h.results || [];
    if (history[0]?.result_id) latest = await API.result(history[0].result_id);
  } catch { /* show empty dashboard below */ }

  const docs = latest?.documents;
  $("#main").innerHTML = `
    <div class="dash-hero">
      <div>
        <h1>${state.demo ? "Demo dashboard" : "Welcome"}</h1>
        <p>${state.profile?.name ? `Applicant: <b>${esc(state.profile.name)}</b>${state.demo ? " · Demo Applicant" : ""}` : "Check which scheme fits your situation."}</p>
      </div>
      <a class="btn btn-primary" href="#/check">Check My Eligibility</a>
    </div>

    <div class="dash-cards">
      <div class="card">
        <div class="section-title"><h2>Current pathway / result</h2></div>
        ${latest ? `
          <div class="mini-item" style="cursor:pointer" onclick="location.hash='#/result/${esc(latest.result_id)}'">
            <div><b>${esc(latest.scheme.name)}</b><span class="when">${esc(timeAgo(latest.metadata?.evaluated_at))}</span></div>
            <span class="chip ${STATUS_CHIP[latest.status]}">${STATUS_LABEL[latest.status]}</span>
          </div>
          <p class="mt-1 muted" style="font-size:.9rem">${esc(latest.summary || "")}</p>`
        : `<div class="empty"><span class="big">🧭</span>No eligibility check yet.<br>Your result and financial pathway will appear here.</div>`}
      </div>

      <div class="card">
        <div class="section-title"><h2>Document readiness</h2></div>
        ${docs && docs.total_count ? `
          <div class="flex-between"><b>${docs.ready_count} / ${docs.total_count} ready</b><span class="chip chip-gray">self-marked</span></div>
          <div class="progress-track"><div class="progress-fill" style="width:${(docs.ready_count / docs.total_count) * 100}%"></div></div>
          <p class="faint" style="font-size:.8rem">From your latest check: ${esc(latest.scheme.name)}</p>`
        : `<div class="empty"><span class="big">📄</span>Run a check to see which documents you already have ready.</div>`}
      </div>

      <div class="card">
        <div class="section-title"><h2>Previous pathways</h2></div>
        ${history.length ? `<div class="mini-list">${history.slice(0, 4).map((h) => `
          <div class="mini-item" style="cursor:pointer" onclick="location.hash='#/result/${esc(h.result_id)}'">
            <div><b>${esc(h.scheme_name)}</b><span class="when">${esc(timeAgo(h.evaluated_at))}</span></div>
            <span class="chip ${STATUS_CHIP[h.status]}">${STATUS_LABEL[h.status]}</span>
          </div>`).join("")}</div>
          <a href="#/history" class="btn btn-ghost btn-sm mt-1">View all history →</a>`
        : `<div class="empty"><span class="big">🕘</span>Previous eligibility checks will be listed here.</div>`}
      </div>

      <div class="card">
        <div class="section-title"><h2>Notifications</h2></div>
        ${(() => { const n = getNotifs(); return n.length ? n.slice(0, 3).map((it) => `
          <div class="mini-item" ${it.resultId ? `style="cursor:pointer" onclick="location.hash='#/result/${esc(it.resultId)}'"` : ""}>
            <div><b style="font-weight:500">${esc(it.title)}</b><span class="when">${esc(timeAgo(it.at))}</span></div>
          </div>`).join("") : `<div class="empty"><span class="big">🔔</span>No notifications yet.</div>`; })()}
      </div>
    </div>`;
}

/* ------------------------------------------------- guided profile (steps) */
const STEPS = ["About You", "Your Business", "Funding Need"];
function stepperHTML(active) {
  return `<div class="stepper">${STEPS.map((s, i) => `
    <div class="step ${i + 1 === active ? "active" : i + 1 < active ? "done" : ""}">
      <span class="dot">${i + 1 < active ? "✓" : i + 1}</span> ${s}
    </div>${i < STEPS.length - 1 ? '<div class="step-line"></div>' : ""}`).join("")}</div>`;
}
function field(name, opts = {}) {
  const v = state.profile?.[name] ?? "";
  return `<div class="field">
    <label for="f_${name}">${FIELD_LABELS[name]}${opts.required ? ' <span class="req">*</span>' : ""}</label>
    ${opts.choices
      ? `<div class="choice-grid" data-choice="${name}">${opts.choices.map(([val, lab]) =>
          `<button type="button" class="choice ${String(v) === String(val) ? "selected" : ""}" data-value="${val}">${lab}</button>`).join("")}</div>`
      : `<input id="f_${name}" type="${opts.type || "text"}" value="${esc(v)}" placeholder="${esc(opts.placeholder || "")}" ${opts.min ? `min="${opts.min}"` : ""}>`}
    ${opts.hint ? `<div class="hint">${opts.hint}</div>` : ""}
  </div>`;
}
function bindChoices(root) {
  root.querySelectorAll("[data-choice]").forEach((grid) => {
    grid.addEventListener("click", (e) => {
      const btn = e.target.closest(".choice");
      if (!btn) return;
      grid.querySelectorAll(".choice").forEach((c) => c.classList.remove("selected"));
      btn.classList.add("selected");
      state.profile = state.profile || {};
      state.profile[grid.dataset.choice] = btn.dataset.value;
      state.sources[grid.dataset.choice] = "entered";
      persist();
    });
  });
}
function readInputs(root, fields) {
  state.profile = state.profile || {};
  fields.forEach((f) => {
    const el = $(`#f_${f}`, root);
    if (!el) return;
    let val = el.value.trim();
    if (["age", "income", "funding_need"].includes(f)) val = val === "" ? null : Number(val);
    state.profile[f] = val === null || val === "" ? null : val;
    if (has(state.profile[f])) state.sources[f] = "entered";
  });
  persist();
}

function renderCheck() {
  const step = state.step || 1;
  const p = state.profile || {};
  $("#main").innerHTML = `
    <h1>${STEPS[step - 1]}</h1>
    <p class="mb-2">Simple steps — you'll review everything before we check eligibility.</p>
    <div class="card">
      ${stepperHTML(step)}
      <div class="form-grid">
        ${step === 1 ? `
          ${field("name", { placeholder: "Your full name" })}
          <div class="form-grid-2">
            ${field("age", { type: "number", min: "18", placeholder: "e.g. 28" })}
            ${field("location", { placeholder: "City / district" })}
          </div>
          <div class="form-grid-2">
            ${field("category", { choices: CATEGORY_OPTS })}
            ${field("income", { type: "number", placeholder: "Annual income in ₹ (optional)" })}
          </div>` : ""}
        ${step === 2 ? `
          ${field("business_type", { choices: BTYPE_OPTS })}
          ${field("business_stage", { choices: STAGE_OPTS })}
          <div class="form-grid-2">
            ${field("sector", { choices: SECTOR_OPTS })}
            ${field("business_status", { choices: BSTATUS_OPTS })}
          </div>` : ""}
        ${step === 3 ? `
          <div class="form-grid-2">
            ${field("funding_need", { type: "number", placeholder: "Amount in ₹ (e.g. 500000)" })}
            ${field("financing_type", { choices: FIN_OPTS })}
          </div>
          ${field("funding_purpose", { choices: PURPOSE_OPTS })}
          <div class="field">
            <label for="f_nl">Tell us about your situation in your own words <span class="faint">(optional)</span></label>
            <textarea id="f_nl" placeholder='e.g. "I am starting a small food-processing business in Ahmedabad and need around five lakh rupees for equipment."'>${esc(state.nlDescription || p.natural_language_description || "")}</textarea>
            <div class="hint">We'll extract what we understand and show it to you to confirm — nothing is assumed without your review.</div>
          </div>` : ""}
      </div>
      <div class="btn-row mt-2" style="justify-content:space-between">
        ${step > 1 ? '<button class="btn btn-ghost" id="stepBack">← Back</button>' : '<a class="btn btn-ghost" href="#/dashboard">← Dashboard</a>'}
        <button class="btn btn-primary" id="stepNext">${step < 3 ? "Continue →" : "Continue to Review →"}</button>
      </div>
    </div>`;

  bindChoices($("#main"));
  $("#stepNext").addEventListener("click", () => {
    readInputs($("#main"), { 1: ["name", "age", "location", "income"], 2: ["sector"], 3: ["funding_need"] }[step] || []);
    if (step === 3) { state.nlDescription = $("#f_nl").value.trim(); persist(); }
    if (step < 3) { state.step = step + 1; persist(); renderCheck(); }
    else location.hash = "#/understanding";
  });
  const back = $("#stepBack");
  if (back) back.addEventListener("click", () => { state.step = step - 1; persist(); renderCheck(); });
}

/* ----------------------------------------------- AI profile understanding */
function renderUnderstanding() {
  const doExtract = state.nlDescription && !state.understandingDone;
  if (doExtract) {
    $("#main").innerHTML = `<div class="spinner"></div><p class="text-center muted">Understanding your situation…</p>`;
    API.extract(state.nlDescription)
      .then(({ profile }) => {
        state.profile = state.profile || {};
        Object.entries(profile).forEach(([k, v]) => {
          if (has(v) && !has(state.profile[k])) { state.profile[k] = v; state.sources[k] = "extracted"; }
        });
        state.profile.natural_language_description = state.nlDescription;
        state.understandingDone = true;
        persist();
        renderUnderstanding();
      })
      .catch((err) => { state.understandingDone = true; persist(); toast(`Extraction failed (${err.message}) — showing your entered details.`); renderUnderstanding(); });
    return;
  }

  const p = state.profile || {};
  const rows = PROFILE_FIELDS.map((f) => `
    <div class="field" data-field="${f}">
      <div class="pf-head">
        <span class="pf-label">${FIELD_LABELS[f]}</span>${sourceChip(f)}
      </div>
      <input id="u_${f}" type="text" value="${esc(p[f] ?? "")}" placeholder="Not provided — click to add">
    </div>`).join("");

  $("#main").innerHTML = `
    <h1>We understood your situation</h1>
    <p class="mb-2">Review each field — edit anything that's off. <b>Confirmed information is the final source of truth</b> for the eligibility check.</p>
    ${state.nlDescription ? `<div class="card card-quiet mb-2"><div class="callout info"><span>💬</span><span>"${esc(state.nlDescription)}"</span></div></div>` : ""}
    <div class="card">
      <div class="profile-fields two-col">${rows}</div>
      <div class="btn-row mt-2" style="justify-content:space-between">
        <a class="btn btn-ghost" href="#/check">← Edit steps</a>
        <button class="btn btn-primary" id="confirmBtn">Confirm & Continue →</button>
      </div>
    </div>`;

  $("#main").querySelectorAll("[data-field] input").forEach((inp) => {
    inp.addEventListener("change", () => {
      const f = inp.dataset ? inp.closest("[data-field]").dataset.field : null;
      const field = inp.closest("[data-field]").dataset.field;
      let val = inp.value.trim();
      if (["age", "income", "funding_need"].includes(field)) val = val === "" ? null : Number(val);
      state.profile[field] = val || null;
      state.sources[field] = has(val) ? "confirmed" : state.sources[field];
      persist();
      inp.closest("[data-field]").querySelector(".pf-head").innerHTML =
        `<span class="pf-label">${FIELD_LABELS[field]}</span>${sourceChip(field)}`;
    });
  });
  $("#confirmBtn").addEventListener("click", () => location.hash = "#/review");
}

/* ----------------------------------------------------------------- review */
function renderReview() {
  const p = state.profile;
  if (!p) { location.hash = "#/check"; return; }
  const rows = PROFILE_FIELDS
    .filter((f) => f !== "sector" || has(p.sector))
    .map((f) => `<div class="review-row"><div class="k">${FIELD_LABELS[f]}</div><div class="v ${has(p[f]) ? "" : "faint"}">${has(p[f]) ? label(f, p[f]) : "Not provided"}</div></div>`)
    .join("");
  $("#main").innerHTML = `
    <h1>Review Your Information</h1>
    <p class="mb-2">This is what the rule engine will use. Anything missing can be skipped, but more details mean a sharper result.</p>
    ${state.demo ? `<div class="mb-1"><span class="chip chip-amber">Demo Applicant — Aarav Patel, Ahmedabad, food processing, ₹5 lakh need</span></div>` : ""}
    <div class="card">
      <div class="review-grid">${rows}</div>
      <div class="callout mt-2">⚠️ This result is an eligibility assessment based on the information provided. It is not an approval or funding guarantee.</div>
      <div class="btn-row mt-2" style="justify-content:space-between">
        <a class="btn btn-ghost" href="#/check">← Edit information</a>
        <button class="btn btn-primary btn-lg" id="runCheck">Check My Eligibility</button>
      </div>
    </div>`;
  $("#runCheck").addEventListener("click", () => {
    state.understandingDone = false;
    persist();
    location.hash = "#/processing";
  });
}

/* ------------------------------------------------------------- processing */
const STAGES = [
  "Building your applicant profile",
  "Finding relevant schemes",
  "Checking eligibility rules",
  "Preparing your explanation",
  "Building your pathway",
];
function renderProcessing() {
  if (!state.profile) { location.hash = "#/check"; return; }
  $("#main").innerHTML = `
    <div class="text-center mt-3"><h1>Checking your eligibility</h1><p>Running the deterministic rule engine against ${esc("5 prototype schemes")}…</p></div>
    <div class="process-list">
      ${STAGES.map((s, i) => `<div class="process-item" data-stage="${i}"><span class="p-icon"></span>${s}</div>`).join("")}
    </div>`;

  const checkPromise = API.check({
    applicant: state.profile,
    profile_sources: state.sources,
    document_states: getUserDocStates(),
  }).then((result) => {
    state.lastResultId = result.result_id;
    persist();
    pushNotif(`Eligibility checked — ${result.scheme.name}: ${STATUS_LABEL[result.status]}`, result.result_id);
    return result;
  });

  let stage = 0;
  const timer = setInterval(() => {
    const items = document.querySelectorAll(".process-item");
    if (stage > 0 && items[stage - 1]) { items[stage - 1].classList.remove("active"); items[stage - 1].classList.add("done"); }
    if (stage < items.length) { items[stage].classList.add("active"); stage++; }
    else clearInterval(timer);
  }, 420);

  let minTime = new Promise((r) => setTimeout(r, STAGES.length * 420 + 300));
  Promise.all([checkPromise, minTime])
    .then(([result]) => { clearInterval(timer); location.hash = `#/result/${result.result_id}`; })
    .catch((err) => {
      clearInterval(timer);
      $("#main").innerHTML = `
        <div class="card error-state">
          <span class="big">😵</span>
          <h2>Something went wrong</h2>
          <p class="mt-1">${esc(err.message)}</p>
          <p class="faint mt-1">The rule engine or the API may be unavailable. Nothing was saved.</p>
          <div class="btn-row mt-2" style="justify-content:center">
            <button class="btn btn-primary" id="retryBtn">Retry</button>
            <a class="btn btn-secondary" href="#/review">Review information</a>
          </div>
        </div>`;
      $("#retryBtn").addEventListener("click", renderProcessing);
    });
}

/* ----------------------------------------------------------------- result */
/* Document readiness is chosen by the user: one global set, synced to the
   backend, applied to saved results and reused in every eligibility check.
   Marks are never set automatically. */
const DOC_STATES_KEY = "ss_doc_states";
function getUserDocStates() {
  try { return JSON.parse(localStorage.getItem(DOC_STATES_KEY) || "{}"); } catch { return {}; }
}
function setUserDocState(name, ready) {
  const states = getUserDocStates();
  if (ready) states[name] = true; else delete states[name];
  localStorage.setItem(DOC_STATES_KEY, JSON.stringify(states));
  API.updateDocStates(states).catch(() => { /* offline — local copy still authoritative for this browser */ });
}
function migrateLegacyDocMarks() {
  let merged = null;
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const key = localStorage.key(i);
    if (key && key.startsWith("ss_docs_")) {
      try {
        const legacy = JSON.parse(localStorage.getItem(key) || "{}");
        if (Object.keys(legacy).length) merged = Object.assign(merged || {}, legacy);
      } catch { /* ignore malformed legacy entry */ }
      localStorage.removeItem(key);
    }
  }
  if (merged) {
    localStorage.setItem(DOC_STATES_KEY, JSON.stringify(Object.assign({}, merged, getUserDocStates())));
  }
}
migrateLegacyDocMarks();
function renderResult(id) {
  $("#main").innerHTML = `<div class="spinner"></div><p class="text-center muted">Loading result…</p>`;
  API.result(id).then((r) => paintResult(r)).catch((err) => {
    $("#main").innerHTML = `
      <div class="card error-state">
        <span class="big">🔍</span><h2>Result not found</h2>
        <p class="mt-1">${esc(err.message)}</p>
        <div class="btn-row mt-2" style="justify-content:center">
          <a class="btn btn-primary" href="#/dashboard">Back to dashboard</a>
          <a class="btn btn-secondary" href="#/check">New check</a>
        </div>
      </div>`;
  });
}

function paintResult(r) {
  const st = r.status;
  const docs = r.documents || { items: [], ready_count: 0, total_count: 0 };
  const userStates = getUserDocStates();
  const fp = r.financial_pathway || {};

  const statusIcon = { eligible: "✅", not_currently_eligible: "🚫", needs_more_information: "⏳", no_match: "🤷" }[st];

  const checksTable = (r.eligibility_checks || []).length ? `
    <div class="table-wrap"><table class="checks">
      <thead><tr><th>Criterion</th><th>Your value</th><th>Required</th><th>Result</th></tr></thead>
      <tbody>
        ${r.eligibility_checks.map((c) => `
          <tr>
            <td><b>${esc(c.criterion)}</b>${c.why_it_matters ? `<div class="why">${esc(c.why_it_matters)}</div>` : ""}</td>
            <td>${esc(c.your_value)}</td>
            <td>${esc(c.required)}</td>
            <td class="${c.result === "Passed" ? "res-pass" : c.result === "Failed" ? "res-fail" : "res-unknown"}">
              ${c.result === "Passed" ? "✓ Passed" : c.result === "Failed" ? "✗ Failed" : "? Unknown"}
            </td>
          </tr>`).join("")}
      </tbody>
    </table></div>`
    : `<div class="empty">No criteria were checkable for this profile.</div>`;

  const whyHTML = (r.why_match || []).length ? `
    <div class="why-list">
      ${(r.why_match || []).map((w) => `<div class="why-item"><span class="tick">${st === "eligible" ? "✓" : "•"}</span><span>${esc(w)}</span></div>`).join("")}
    </div>`
    : `<div class="empty">No reasons available for this result.</div>`;

  const componentsHTML = (fp.components || []).length ? `
    <div class="pathway-flow mt-1">
      ${fp.components.map((c) => `
        <div class="pf-box k-${c.kind}">
          <b>${esc(c.label)}</b>
          <div class="val">${esc(c.display)}</div>
          <div class="note">${esc(c.basis)}</div>
        </div>
        <div class="pf-arrow">↓</div>`).join("")}
    </div>` : "";

  // the user's own choice wins over whatever was stored with the result
  const docItems = (docs.items || []).map((d) => ({
    ...d,
    ready: Object.prototype.hasOwnProperty.call(userStates, d.name) ? !!userStates[d.name] : !!d.ready,
  }));
  const readyCount = docItems.filter((d) => d.ready).length;
  const nextStep = r.next_step || {};

  $("#main").innerHTML = `
    <div class="result-head">
      <span class="chip chip-blue">Result ID ${esc(r.result_id.slice(0, 8))}…</span>
      <span class="chip chip-amber">${esc(r.metadata?.data_label || "Demo Data / Prototype Data")}</span>
      <h1 class="mt-1">Your Best Match</h1>
      <h2 class="muted" style="font-weight:600">${esc(r.scheme.name)}</h2>
      <div class="result-status st-${esc(st)}">${statusIcon} ${STATUS_LABEL[st]}</div>
      <p style="max-width:640px;margin:0 auto">${esc(r.summary || "")}</p>
      ${state.demo ? `<div class="mt-1"><span class="chip chip-amber">Demo Applicant</span></div>` : ""}
    </div>

    <div class="card section-gap">
      <div class="section-title"><h2>Why this matches you</h2><span class="sub">AI explanation of the rule engine's decision</span></div>
      ${whyHTML}
      <div class="callout info mt-2">🛡️ ${esc(r.trust_statement || "The rule engine checks the fit. AI explains the fit.")}</div>
    </div>

    <details class="card section-gap" ${st !== "eligible" ? "open" : ""}>
      <summary style="cursor:pointer;font-weight:700"><h2 style="display:inline">Detailed eligibility</h2> <span class="sub muted">— every criterion from the scheme's rules</span></summary>
      <div class="mt-2">${checksTable}</div>
    </details>

    ${comparisonTable(r)}

    ${(fp.assistance || componentsHTML) ? `
    <div class="card section-gap">
      <div class="section-title"><h2>Financial pathway</h2><span class="sub">${fp.calculated ? "calculated from your funding need" : ""}</span></div>
      <div class="pathway-flow">
        <div class="pf-box"><b>Your funding need</b><div class="val">${esc(fp.funding_need_display || money(fp.funding_need))}</div><div class="note">as entered in your profile</div></div>
        <div class="pf-arrow">↓</div>
        ${componentsHTML}
      </div>
      ${fp.assistance ? `<p class="mt-2"><b>Scheme assistance:</b> ${esc(fp.assistance)}</p>` : ""}
      ${fp.contribution ? `<p><b>Contribution:</b> ${esc(fp.contribution)}</p>` : ""}
      ${fp.structure ? `<p class="faint" style="font-size:.85rem">${esc(fp.structure)}</p>` : ""}
      ${fp.next_financial_action ? `<div class="callout info mt-2">👉 ${esc(fp.next_financial_action)}</div>` : ""}
    </div>` : ""}

    ${overviewGraphHTML(r)}

    ${docItems.length ? `
    <div class="card section-gap">
      <div class="flex-between">
        <div class="section-title" style="margin:0"><h2>Document readiness</h2></div>
        <b>${readyCount} / ${docItems.length} ready</b>
      </div>
      <div class="progress-track"><div class="progress-fill" style="width:${docItems.length ? (readyCount / docItems.length) * 100 : 0}%"></div></div>
      <div class="doc-list mt-1">
        ${docItems.map((d) => `
          <div class="doc-item ${d.ready ? "ready" : ""}" data-doc="${esc(d.name)}">
            <button class="doc-check" aria-label="Toggle ${esc(d.name)}">✓</button>
            <div class="doc-body"><b>${esc(d.name)}</b><span class="note">${d.ready ? "Marked as ready by you" : "Not yet marked"}${d.required ? " · required" : " · optional"}</span></div>
          </div>`).join("")}
      </div>
      <p class="faint mt-1" style="font-size:.8rem">Readiness is self-marked in this prototype — not verified.</p>
    </div>` : ""}

    ${nextStep.destination ? `
    <div class="card section-gap">
      <h2>Your Next Step</h2>
      <div class="next-grid mt-2">
        <div class="next-box"><b>Where to go</b><div style="font-weight:700;font-size:1.05rem">${esc(nextStep.destination)}</div>
          <p class="mt-1" style="font-size:.9rem">${esc(nextStep.channel || "")}</p></div>
        <div class="next-box"><b>Why there</b><p style="font-size:.92rem;color:var(--text)">${esc(nextStep.why || "")}</p></div>
        <div class="next-box"><b>What to take</b>
          <div class="take-list">${(nextStep.what_to_take || []).map((t) => `<div class="take-item"><span>📄</span>${esc(t)}</div>`).join("")}</div></div>
        <div class="next-box"><b>Action</b><button class="btn btn-primary btn-block mt-1" id="visitChannel">${esc(nextStep.action || "Visit Application Channel")}</button>
          <p class="faint mt-1" style="font-size:.78rem">${esc(nextStep.routing_note || "")}</p></div>
      </div>
    </div>` : ""}

    ${(r.other_schemes || []).length ? `
    <div class="card section-gap">
      <div class="section-title"><h2>Other schemes assessed</h2><span class="sub">same rule engine, same profile</span></div>
      <div class="mini-list">
        ${r.other_schemes.map((o) => `
          <div class="other-item">
            <div><b>${esc(o.name)}</b><span class="gap">${esc(o.gap_note || "")}</span></div>
            <span class="chip ${STATUS_CHIP[o.status]}">${STATUS_LABEL[o.status]}</span>
          </div>`).join("")}
      </div>
    </div>` : ""}

    <div class="card section-gap card-quiet">
      <div class="btn-row" style="justify-content:space-between">
        <a class="btn btn-secondary" href="#/review">← Review / modify profile</a>
        <div class="btn-row">
          <a class="btn btn-ghost" href="#/history">View history</a>
          <button class="btn btn-outline" id="downloadPathway">⬇ Download my pathway</button>
          <a class="btn btn-primary" href="#/dashboard">Back to dashboard</a>
        </div>
      </div>
      <p class="faint mt-2" style="font-size:.8rem">${esc(r.disclaimer || "")}</p>
    </div>`;

  // document toggles — chosen by the user, saved globally and synced to the backend
  document.querySelectorAll(".doc-item").forEach((item) => {
    const name = item.dataset.doc;
    item.querySelector(".doc-check").addEventListener("click", () => {
      const nowReady = !item.classList.contains("ready");
      item.classList.toggle("ready", nowReady);
      setUserDocState(name, nowReady);
      item.querySelector(".note").textContent = nowReady ? "Marked as ready by you" : "Not yet marked";
      paintResultDocsCount(document.querySelectorAll(".doc-item.ready").length, docItems.length);
    });
  });
  const visit = $("#visitChannel");
  if (visit) visit.addEventListener("click", () => toast("Prototype routing — external application handoff is not connected in this demo."));
  const downloadBtn = $("#downloadPathway");
  if (downloadBtn) downloadBtn.addEventListener("click", () => downloadPathway(r));
}

function paintResultDocsCount(ready, total) {
  const counter = document.querySelector(".flex-between b");
  if (counter && total) counter.textContent = `${ready} / ${total} ready`;
}

/* ------------------------------------------------- scheme comparison */
function comparisonTable(r) {
  const cmp = r.scheme_comparison || {};
  const rows = cmp.rows || [];
  if (!rows.length) return "";
  const bestCode = r.scheme?.code;
  return `
    <div class="card section-gap">
      <div class="section-title"><h2>How you compare across schemes</h2><span class="sub">same profile, same rule engine — side by side</span></div>
      <div class="cmp-scroll">
        <table class="cmp-table">
          <thead><tr><th>Scheme</th><th>Eligible?</th><th>Why / why not</th><th>Match</th><th>Official source</th></tr></thead>
          <tbody>
            ${rows.map((row) => `
              <tr class="${row.code === bestCode ? "cmp-best" : ""}">
                <td class="cmp-scheme">
                  <b>${esc(row.name)}</b>
                  <span class="cmp-auth">${esc(row.authority || "")}</span>
                  ${row.best_for ? `<span class="cmp-auth">Best for: ${esc(row.best_for)}</span>` : ""}
                </td>
                <td><span class="chip ${STATUS_CHIP[row.status]}">${STATUS_LABEL[row.status] ?? row.status}</span></td>
                <td class="cmp-why">
                  <span class="why-kind ${esc(row.why_kind)}">${row.why_kind === "qualified" ? "Qualifies" : row.why_kind === "missing_info" ? "Needs info" : "Does not qualify"}</span>
                  <div>${esc(row.why)}</div>
                  ${(row.top_gaps || []).length ? `<ul class="cmp-gaps">${row.top_gaps.map((g) => `<li>${esc(g.criterion)}: your ${esc(g.your_value)} vs required ${esc(g.required)}</li>`).join("")}</ul>` : ""}
                </td>
                <td class="cmp-score">${row.match_score}%</td>
                <td>${row.official_url ? `<a class="cmp-link" href="${esc(row.official_url)}" target="_blank" rel="noopener">Official portal ↗</a>` : `<span class="muted" style="font-size:.78rem">—</span>`}</td>
              </tr>`).join("")}
          </tbody>
        </table>
      </div>
      <p class="cmp-note">${esc(cmp.note || "")}</p>
    </div>`;
}

/* ------------------------------------------------- overview graph */
function overviewGraphHTML(r) {
  const ov = r.overview_graph || {};
  if (!ov.has_data) return "";
  const scores = ov.match_scores || [];
  const W = 460, H = 230, PAD_L = 36, PAD_B = 42, PAD_T = 22, PAD_R = 10;
  const chartW = W - PAD_L - PAD_R, chartH = H - PAD_T - PAD_B;
  const n = scores.length || 1;
  const slot = chartW / n;
  const barW = Math.min(58, slot * 0.62);
  const bars = scores.map((s, i) => {
    const h = Math.max(2, (Math.min(100, Math.max(0, s.score)) / 100) * chartH);
    const x = PAD_L + slot * i + (slot - barW) / 2;
    const y = PAD_T + chartH - h;
    const cls = s.status === "eligible" ? "st-green" : s.status === "needs_more_information" ? "st-amber" : "st-red";
    const short = esc((s.code || s.name.split("—")[0].split("(")[0].trim()).slice(0, 9));
    return `
      <g class="ov-bar ${cls}">
        <title>${esc(s.name)} — ${s.score}% match</title>
        <rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barW.toFixed(1)}" height="${h.toFixed(1)}" rx="5"></rect>
        <text class="ov-val" x="${(x + barW / 2).toFixed(1)}" y="${(y - 6).toFixed(1)}" text-anchor="middle">${s.score}%</text>
        <text class="ov-lbl" x="${(x + barW / 2).toFixed(1)}" y="${PAD_T + chartH + 17}" text-anchor="middle">${short}</text>
      </g>`;
  }).join("");
  const gridLines = [0, 25, 50, 75, 100].map((v) => {
    const y = PAD_T + chartH - (v / 100) * chartH;
    return `<line class="ov-grid" x1="${PAD_L}" y1="${y}" x2="${W - PAD_R}" y2="${y}"></line><text class="ov-tick" x="${PAD_L - 6}" y="${y + 3}" text-anchor="end">${v}</text>`;
  }).join("");
  const counts = ov.status_counts || {};
  const best = ov.best_match || {};
  return `
    <div class="card section-gap">
      <div class="section-title"><h2>Your eligibility overview</h2><span class="sub">everything assessed, at a glance</span></div>
      <div class="ov-wrap">
        <div class="ov-panel">
          <h3>Match score by scheme</h3>
          <div class="ov-sub">share of required conditions you satisfy — higher is better</div>
          <div class="ov-svg-wrap">
            <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Match scores across schemes">
              ${gridLines}
              <line class="ov-axis" x1="${PAD_L}" y1="${PAD_T}" x2="${PAD_L}" y2="${PAD_T + chartH}"></line>
              <line class="ov-axis" x1="${PAD_L}" y1="${PAD_T + chartH}" x2="${W - PAD_R}" y2="${PAD_T + chartH}"></line>
              ${bars}
            </svg>
          </div>
          <div class="ov-legend"><span class="lg-pass">Eligible</span><span class="lg-miss">Needs info</span><span class="lg-fail">Not eligible</span></div>
        </div>
        <div class="ov-panel">
          <h3>Assessment summary</h3>
          <div class="ov-sub">all schemes evaluated against your profile</div>
          <div class="ov-stats">
            <div class="ov-stat st-green"><b>${counts.eligible ?? 0}</b><span>Eligible</span></div>
            <div class="ov-stat st-amber"><b>${counts.needs_more_information ?? 0}</b><span>Needs info</span></div>
            <div class="ov-stat st-red"><b>${counts.not_currently_eligible ?? 0}</b><span>Not eligible</span></div>
          </div>
          ${best.name ? `<div class="ov-best"><b>Best match: ${esc(best.name)}</b><span class="ov-auth">${esc(best.authority || "")}</span></div>` : ""}
          <p class="ov-note">${esc(ov.note || "")}</p>
        </div>
      </div>
    </div>`;
}

/* ------------------------------------------------- download my pathway */
function downloadPathway(r) {
  const st = r.status;
  const docs = r.documents || { items: [] };
  const userStates = getUserDocStates();
  const docItems = (docs.items || []).map((d) => ({
    ...d,
    ready: Object.prototype.hasOwnProperty.call(userStates, d.name) ? !!userStates[d.name] : !!d.ready,
  }));
  const readyCount = docItems.filter((d) => d.ready).length;
  const fp = r.financial_pathway || {};
  const nextStep = r.next_step || {};
  const snap = r.applicant_snapshot || {};
  const when = (r.metadata?.evaluated_at || "").replace("T", " ").slice(0, 16);

  const profileRows = [
    ["Name", snap.name], ["Age", snap.age], ["Location", snap.location],
    ["Category / community", VALUE_LABELS[snap.category] ?? snap.category],
    ["Annual income", has(snap.income) ? money(snap.income) : null],
    ["Business type", VALUE_LABELS[snap.business_type] ?? snap.business_type],
    ["Business stage", VALUE_LABELS[snap.business_stage] ?? snap.business_stage],
    ["Sector", VALUE_LABELS[snap.sector] ?? snap.sector],
    ["Business status", VALUE_LABELS[snap.business_status] ?? snap.business_status],
    ["Funding need", has(snap.funding_need) ? money(snap.funding_need) : null],
    ["Funding purpose", VALUE_LABELS[snap.funding_purpose] ?? snap.funding_purpose],
    ["Financing preference", VALUE_LABELS[snap.financing_type] ?? snap.financing_type],
  ]
    .filter(([, v]) => has(v))
    .map(([k, v]) => `<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`)
    .join("");

  const checkRows = (r.eligibility_checks || []).map((c) => `
    <tr>
      <td><b>${esc(c.criterion || c.field)}</b><div class="why-it">${esc(c.why_it_matters || "")}</div></td>
      <td>${esc(c.your_value)}</td>
      <td>${esc(c.required)}</td>
      <td class="${/passed/i.test(c.result) ? "pass" : "fail"}">${esc(c.result)}</td>
    </tr>`).join("");

  const components = (fp.components || []).map((c) => `
    <tr>
      <td><b>${esc(c.label)}</b><div class="why-it">${esc(c.kind === "calculated_total" ? "calculated" : c.kind)}</div></td>
      <td>${esc(c.display)}</td>
      <td>${esc(c.basis)}</td>
    </tr>`).join("");

  const docRows = docItems.map((d) => `
    <tr>
      <td>${d.ready ? `<span class="tick">✓</span>` : `<span class="untick">○</span>`} ${esc(d.name)}</td>
      <td>${d.required ? "Required" : "Optional"}</td>
      <td class="${d.ready ? "pass" : "dim"}">${d.ready ? "Marked as ready by you" : "Not yet marked"}</td>
    </tr>`).join("");

  const otherRows = (r.other_schemes || []).map((o) => `
    <tr><td><b>${esc(o.name)}</b></td><td>${esc(o.gap_note || "")}</td>
    <td class="${o.status === "eligible" ? "pass" : "dim"}">${esc(STATUS_LABEL[o.status] ?? o.status)}</td></tr>`).join("");

  const cmpRowsSrc = (r.scheme_comparison?.rows || []);
  const compRows = cmpRowsSrc.map((row) => `
    <tr>
      <td><b>${row.code === r.scheme?.code ? "✓ " : ""}${esc(row.name)}</b><div class="why-it">${esc(row.authority || "")}</div></td>
      <td class="${row.status === "eligible" ? "pass" : row.status === "not_currently_eligible" ? "fail" : "dim"}">${esc(STATUS_LABEL[row.status] ?? row.status)}</td>
      <td>${esc(row.why || "")}</td>
      <td>${row.match_score}%</td>
    </tr>`).join("");
  const ovG = r.overview_graph || {};
  const ovCounts = ovG.status_counts || {};
  const ovRows = ovG.has_data ? `
    <tr><th>Eligible schemes</th><td class="pass"><b>${ovCounts.eligible ?? 0}</b></td></tr>
    <tr><th>Need more information</th><td class="dim"><b>${ovCounts.needs_more_information ?? 0}</b></td></tr>
    <tr><th>Not currently eligible</th><td class="fail"><b>${ovCounts.not_currently_eligible ?? 0}</b></td></tr>
    ${ovG.best_match?.name ? `<tr><th>Best match</th><td><b>${esc(ovG.best_match.name)}</b><div class="why-it">${esc(ovG.best_match.authority || "")}</div></td></tr>` : ""}` : "";

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>SamarthSetu AI — Your Pathway (${esc(r.scheme.name)})</title>
<style>
  :root { --ink:#111827; --muted:#6b7280; --line:#e5e7eb; --brand:#1d4ed8; --green:#047857; --red:#b91c1c; }
  * { box-sizing:border-box; }
  body { font:14px/1.55 Georgia,'Times New Roman',serif; color:var(--ink); margin:0; padding:36px 44px; max-width:860px; }
  h1 { font-size:22px; margin:0 0 2px; }
  h2 { font-size:15px; margin:26px 0 8px; padding-bottom:4px; border-bottom:2px solid var(--ink); text-transform:uppercase; letter-spacing:.06em; }
  .brand { color:var(--brand); font-family:Arial,Helvetica,sans-serif; font-weight:bold; }
  .tag { color:var(--muted); font-size:12px; margin:0 0 14px; }
  .status { display:inline-block; font-family:Arial,Helvetica,sans-serif; font-weight:bold; font-size:13px; padding:3px 10px; border:2px solid; margin:6px 0 2px; }
  .st-eligible { color:var(--green); } .st-not { color:var(--red); } .st-other { color:#92400e; }
  table { width:100%; border-collapse:collapse; margin:8px 0; font-size:13px; }
  th, td { border:1px solid var(--line); padding:6px 9px; text-align:left; vertical-align:top; }
  tr th:first-child, td:first-child { width:30%; }
  thead th { background:#f3f4f6; font-family:Arial,Helvetica,sans-serif; font-size:11px; text-transform:uppercase; letter-spacing:.05em; }
  .why-it { color:var(--muted); font-size:11.5px; }
  .pass { color:var(--green); font-weight:bold; } .fail { color:var(--red); font-weight:bold; } .dim { color:var(--muted); }
  .tick { color:var(--green); font-weight:bold; } .untick { color:var(--muted); }
  .summary { font-size:14.5px; margin:10px 0 0; }
  .box { border:1.5px solid var(--ink); padding:10px 14px; margin:10px 0; }
  .callout { background:#eef2ff; border-left:4px solid var(--brand); padding:8px 12px; margin:10px 0; font-size:13px; }
  .fine { color:var(--muted); font-size:11.5px; }
  footer { margin-top:30px; padding-top:10px; border-top:1px solid var(--line); font-size:11px; color:var(--muted); }
  @media print { body { padding:0; } .noprint { display:none; } }
</style>
</head>
<body>
  <h1><span class="brand">SamarthSetu AI</span> — Your Pathway to Access</h1>
  <p class="tag">From Eligibility to Access · Result ${esc(r.result_id.slice(0, 8))} · evaluated ${esc(when)} UTC</p>

  <h2>Your Best Match</h2>
  <p style="margin:0"><b>${esc(r.scheme.name)}</b> <span class="fine">(${esc(r.scheme.code ?? "—")})</span></p>
  <span class="status ${st === "eligible" ? "st-eligible" : st === "not_currently_eligible" ? "st-not" : "st-other"}">${esc(STATUS_LABEL[st] ?? st)}</span>
  <p class="summary">${esc(r.summary || "")}</p>

  <h2>Applicant information</h2>
  <table><tbody>${profileRows}</tbody></table>

  ${(r.why_match || []).length ? `
  <h2>Why this matches you</h2>
  <ul style="margin:6px 0; padding-left:20px">${r.why_match.map((w) => `<li>${esc(w)}</li>`).join("")}</ul>` : ""}

  ${checkRows ? `
  <h2>Detailed eligibility</h2>
  <table>
    <thead><tr><th>Criterion</th><th>Your value</th><th>Required</th><th>Result</th></tr></thead>
    <tbody>${checkRows}</tbody>
  </table>` : ""}

  ${components ? `
  <h2>Financial pathway</h2>
  <table>
    <thead><tr><th>Component</th><th>Amount</th><th>Basis</th></tr></thead>
    <tbody>${components}</tbody>
  </table>
  ${fp.assistance ? `<p class="box"><b>Scheme assistance:</b> ${esc(fp.assistance)}${fp.contribution ? `<br/><b>Contribution:</b> ${esc(fp.contribution)}` : ""}</p>` : ""}
  ${fp.next_financial_action ? `<div class="callout">👉 ${esc(fp.next_financial_action)}</div>` : ""}` : ""}

  ${docRows ? `
  <h2>Document readiness — ${readyCount} / ${docItems.length} ready</h2>
  <table><tbody>${docRows}</tbody></table>
  <p class="fine">Readiness is self-marked by the applicant — not verified by any authority.</p>` : ""}

  ${nextStep.destination ? `
  <h2>Your next step</h2>
  <table>
    <tbody>
      <tr><th>Where to go</th><td><b>${esc(nextStep.destination)}</b><div class="why-it">${esc(nextStep.channel || "")}</div></td></tr>
      <tr><th>Why</th><td>${esc(nextStep.why || "")}</td></tr>
      <tr><th>What to take</th><td>${(nextStep.what_to_take || []).map(esc).join(" · ")}</td></tr>
      <tr><th>Action</th><td>${esc(nextStep.action || "Visit Application Channel")}</td></tr>
    </tbody>
  </table>` : ""}

  ${otherRows ? `
  <h2>Other schemes assessed</h2>
  <table><tbody>${otherRows}</tbody></table>` : ""}

  ${compRows ? `
  <h2>How you compare across schemes</h2>
  <table>
    <thead><tr><th>Scheme</th><th>Eligible?</th><th>Why / why not</th><th>Match</th></tr></thead>
    <tbody>${compRows}</tbody>
  </table>` : ""}

  ${ovRows ? `
  <h2>Eligibility overview</h2>
  <table><tbody>${ovRows}</tbody></table>` : ""}

  <div class="callout">🛡️ ${esc(r.trust_statement || "The rule engine checks the fit. AI explains the fit.")}</div>
  <footer>
    ${esc(r.disclaimer || "This result is an eligibility assessment based on the information provided. It is not an approval or funding guarantee.")}<br/>
    Scheme details are prototype summaries of real government schemes from official sources — always verify on the official portals. Not affiliated with any government agency; no application is submitted through this document.
  </footer>
  <p class="noprint fine" style="margin-top:18px">Tip: use your browser's Print dialog (Ctrl/Cmd + P) to save this as a PDF.</p>
  <script>window.onload = function () { setTimeout(function () { window.print(); }, 300); };</script>
</body>
</html>`;

  const blob = new Blob([html], { type: "text/html;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const stamp = (r.metadata?.evaluated_at || "").slice(0, 10);
  a.href = url;
  a.download = `samarthsetu-pathway-${r.scheme.code || r.result_id.slice(0, 8)}-${stamp}.html`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  toast("Pathway downloaded — open it and print to save as PDF.");
}

/* ---------------------------------------------------------------- history */
async function renderHistory() {
  $("#main").innerHTML = `<div class="spinner"></div><p class="text-center muted">Loading history…</p>`;
  try {
    const { results } = await API.history();
    $("#main").innerHTML = `
      <div class="flex-between mb-2">
        <div><h1>History</h1><p>Previous eligibility checks — click to reopen a full result.</p></div>
        ${results.length ? `<button class="btn btn-ghost btn-sm" id="clearHistory">Clear history</button>` : ""}
      </div>
      ${results.length === 0
        ? `<div class="card"><div class="empty"><span class="big">🕘</span>No eligibility checks yet.<br><a class="btn btn-primary mt-2" href="#/check">Check My Eligibility</a></div></div>`
        : `<div class="mini-list">${results.map((h) => `
            <div class="history-item" onclick="location.hash='#/result/${esc(h.result_id)}'">
              <div class="history-main">
                <b>${esc(h.scheme_name)}</b>
                <span class="when">${esc(timeAgo(h.evaluated_at))}${h.applicant_name ? ` · ${esc(h.applicant_name)}` : ""}</span>
                <span class="gap muted" style="font-size:.85rem;display:block">${esc((h.summary || "").slice(0, 110))}${(h.summary || "").length > 110 ? "…" : ""}</span>
              </div>
              <span class="chip ${STATUS_CHIP[h.status]}">${STATUS_LABEL[h.status]}</span>
            </div>`).join("")}</div>`}`;
    const clear = $("#clearHistory");
    if (clear) clear.addEventListener("click", async () => {
      await API.clearHistory();
      toast("History cleared");
      renderHistory();
    });
  } catch (err) {
    $("#main").innerHTML = `<div class="card error-state"><span class="big">⚠️</span><h2>Could not load history</h2><p class="mt-1">${esc(err.message)}</p><a class="btn btn-primary mt-2" href="#/dashboard">Back to dashboard</a></div>`;
  }
}

/* ---------------------------------------------------------------- schemes */
async function renderSchemes() {
  $("#main").innerHTML = `<div class="spinner"></div><p class="text-center muted">Loading schemes…</p>`;
  try {
    const { schemes, data_label } = await API.schemes();
    $("#main").innerHTML = `
      <div class="flex-between mb-2">
        <div><h1>Scheme catalogue</h1><p>${schemes.length} real government schemes in the knowledge graph — the rule engine evaluates each one against your profile.</p></div>
        <span class="chip chip-amber">${esc(data_label)}</span>
      </div>
      ${schemes.map((s) => `
        <div class="scheme-card">
          <div class="flex-between">
            <h3>${esc(s.name)}</h3><span class="chip chip-gray mono">${esc(s.code)}</span>
          </div>
          ${s.headline ? `<p class="desc" style="font-weight:600">${esc(s.headline)}</p>` : ""}
          <p class="desc">${esc(s.description)}</p>
          <div class="scheme-meta">
            <span class="chip chip-blue">${s.rule_count} eligibility rules</span>
            <span class="chip chip-violet">${s.required_documents.length} required documents</span>
            <span class="chip chip-green">Partner: ${esc(s.partner)}</span>
            ${s.authority ? `<span class="chip chip-blue">${esc(s.authority)}</span>` : ""}
            ${s.official_reference?.url ? `<a class="cmp-link" href="${esc(s.official_reference.url)}" target="_blank" rel="noopener">Official portal ↗</a>` : ""}
            <span class="chip chip-amber">${esc(s.data_label)}</span>
          </div>
        </div>`).join("")}
      <div class="callout info mt-2">⚖️ Eligibility is always decided by the deterministic rule engine using each scheme's seeded rules — never by AI.</div>`;
  } catch (err) {
    $("#main").innerHTML = `<div class="card error-state"><span class="big">⚠️</span><h2>Could not load schemes</h2><p class="mt-1">${esc(err.message)}</p></div>`;
  }
}

/* --------------------------------------------------------------- settings */
function renderSettings() {
  $("#main").innerHTML = `
    <h1>Settings & About</h1>
    <p class="mb-2">Prototype controls — nothing here affects a real application.</p>
    <div class="card">
      <div class="section-title"><h2>Appearance</h2></div>
      <div class="btn-row">
        <button class="btn btn-secondary" id="setTheme">Toggle light / dark</button>
      </div>
    </div>
    <div class="card section-gap">
      <div class="section-title"><h2>Session data</h2></div>
      <p class="mb-1">Your current profile lives only in this browser session. Saved results live in the prototype's local data file.</p>
      <div class="btn-row">
        <button class="btn btn-secondary" id="resetSession">Reset current profile</button>
        <button class="btn btn-ghost" id="clearNotifs">Clear notifications</button>
      </div>
    </div>
    <div class="card section-gap">
      <div class="section-title"><h2>About this prototype</h2></div>
      <p><b>SamarthSetu AI</b> — From Eligibility to Access.</p>
      <p class="mt-1">One profile → one intelligent pathway to access. The catalogue covers five real government schemes (PMEGP, PMFME, PM MUDRA, Stand-Up India, PM SVANidhi) summarised from official sources. Eligibility is decided by a deterministic rule engine over this structured data; AI only explains the result. This prototype is not affiliated with any government agency — no live integrations, no application submission, no guaranteed funding. Always verify details on the official scheme portals.</p>
      <div class="btn-row mt-2">
        <a class="btn btn-outline btn-sm" href="/docs" target="_blank" rel="noopener">API docs</a>
        <a class="btn btn-outline btn-sm" href="#/schemes">View scheme catalogue</a>
      </div>
    </div>`;
  $("#setTheme").addEventListener("click", () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
  $("#resetSession").addEventListener("click", () => {
    state.profile = null; state.sources = {}; state.demo = false; state.step = 1; state.lastResultId = null; state.nlDescription = "";
    persist(); toast("Profile reset"); location.hash = "#/dashboard"; navigate();
  });
  $("#clearNotifs").addEventListener("click", () => { localStorage.setItem(NOTIF_KEY, "[]"); renderBell(); toast("Notifications cleared"); });
}

/* ------------------------------------------------------------------- 404 */
function renderNotFound() {
  $("#main").innerHTML = `<div class="card error-state"><span class="big">🧭</span><h2>Page not found</h2><a class="btn btn-primary mt-2" href="#/dashboard">Back to dashboard</a></div>`;
}

/* ------------------------------------------------------------------- boot */
if (!getNotifs().length) {
  localStorage.setItem(NOTIF_KEY, JSON.stringify([{
    id: 1, title: "Welcome to SamarthSetu AI — try the demo to see a full pathway in under a minute.",
    resultId: "", read: false, at: new Date().toISOString(),
  }]));
}
renderBell();
navigate();
