# Rev-Ops Plugin Scope Review

**Status:** [PROPOSED]  
**Date:** 2026-05-18  
**Scope:** All 35 SKILL.md files across the rev-ops plugin  
**Review basis:** Stated intent — Sales-CS bridge / OCV-driven / value chain tracing /
CS operating as a revenue center with expansion and renewal pipeline ownership

---

## The Intended Scope — Revised Framing

Two things are true simultaneously:

**1. The bridge mandate.** The plugin instruments the Sales→CS interface: ensuring
sales is selling what CS can deliver, and that CS is delivering what was sold — with
the OCV catalog as the shared reference connecting both sides of that contract. This
is the Revenue Observability layer.

**2. The revenue center mandate.** CS is not a cost center. A CS org that wants to
be treated as a revenue center must behave like one — which means owning expansion and
renewal pipeline, forecasting those pipelines, carrying quota, managing their own deal
desk for expansion motions, and reporting on attainment. The rev-ops plugin serves both
the Sales-CS bridge *and* the CS revenue function directly.

This is an important distinction from a traditional RevOps lens. Conventional RevOps
tools serve the Sales org. This plugin serves CS as a *revenue-producing function* that
operates its own version of the Sales motion (expansion, renewal) while also being the
downstream recipient of the Sales-to-CS handoff. Most of the skills previously flagged
as overscoped are actually required infrastructure for this dual mandate — blockers
if absent, not nice-to-haves.

The plugin is also explicitly **functionally focused, not role-based.** A skill belongs
here if the function it performs is required for revenue orchestration in the
Sales+CS system — regardless of which role (RevOps analyst, CS leader, CRO, CS ops)
happens to execute it.

---

## Revised Assessment: On-Target, Requires Scoping, and True Removals

With the revenue center mandate factored in, the categorization changes substantially.

| Category | Count |
|---|---|
| On-Target — Core bridge | 12 |
| On-Target — CS revenue function (formerly "overscoped") | 16 |
| Requires scoping adjustment | 6 |
| Remove | 1 |

---

## On-Target: Core Bridge Skills (12)

These 12 skills are the plugin's Sales→CS instrumentation layer. Unchanged from
initial assessment.

| Skill | What It Instruments |
|---|---|
| `sales-cs-handoff-quality-scoring` | Deal close → CS onboarding transition. D1–D5 five-dimension scoring. Core instrument. |
| `deal-to-outcome-tracing` | OCV completeness at close; L0–L3 rubric at 30/60/90/180-day checkpoints. |
| `outcome-to-value-tracking` | Portfolio-level L0–L3 mapping per OCV entry. Surfaces systemic L0 persistence. |
| `outcome-statement-builder` | Builds the OCV catalog via Seven-Stage Value Chain. |
| `csql-tracking` | CS→Sales expansion handoff lifecycle. Closes the expansion loop. |
| `early-churn-downgrade-signal-detection` | Three-tier churn model starting at deal close. |
| `cross-system-reconciliation` | Data authority hierarchy; CRM/CS platform discrepancy resolution. |
| `closed-won-to-cs-capacity-modeling` | Converts sales forecast to CS resource demand. |
| `revenue-brief-generation` | Synthesizes handoff + outcome + churn into a unified signal. |
| `revenue-leakage-scanning` | Catches structural deal gaps at close that CS will inherit. |
| `cold-start-interview` | Plugin setup. Registers OCV catalog path, planning parameters, connector status. |
| `unit-of-growth-calculator` | CS capacity calculation engine. AE-anchored and CS-anchored models. |

---

## On-Target: CS Revenue Function Skills (16)

These skills were initially flagged as overscoped under a traditional RevOps lens. Under
the CS-as-revenue-center framing, they are **required infrastructure** — in many cases
blockers that prevent the CS org from operating as a revenue function without them.

### CRM Data Quality Cluster (3 skills)

`crm-hygiene-audit`, `data-decay-tracking`, `duplicate-detection`

**Why they're required:** Garbage in, garbage out. A CS org forecasting expansion and
renewal pipeline against a CRM with stale contacts, data decay, and duplicate accounts
cannot produce reliable forecasts. These skills are the precondition for every other
revenue function skill to produce trustworthy outputs. They are blockers — not
maintenance overhead.

**CS application context:** CS ops teams are increasingly the primary CRM data stewards
for the accounts they own. These tools serve CS ops directly, not just a central
RevOps analyst function.

### Forecasting and Pipeline Cluster (4 skills)

`pipeline-coverage-analysis`, `pipeline-velocity-tracking`, `forecast-variance-analysis`,
`scenario-modeling`

**Why they're required:** A CS org carrying expansion and renewal quota must be able
to visualize and forecast its own pipeline — exactly as Sales does for new logo. If CS
cannot see pipeline coverage against renewal and expansion targets, cannot track velocity
through expansion stages, cannot explain forecast variance to leadership, and cannot
model scenarios for the upcoming quarter, it cannot operate as a revenue center. These
skills apply to the CS-owned pipeline (renewals, upsells, cross-sells) in the same way
they apply to the Sales-owned pipeline.

**CS application context:** The pipeline in these skills is the CS pipeline — renewal
book of business plus expansion opportunities. `pipeline-coverage-analysis` asks whether
there is enough renewal and expansion pipeline to hit the CS revenue target. The skills
need to be contextualized to the CS revenue motion in their configuration and output
framing, but the underlying functions are identical.

### Planning and Incentive Cluster (5 skills, minus 1)

`annual-planning-workflow`, `comp-simulation`, `quota-sensitivity-analysis`,
`mid-year-replan-triggering` ✓

`territory-optimization` ✗ — see Removals section below.

**Why they're required (for quota-carrying CS orgs):** A CS org that carries quota —
expansion quota, renewal quota, or both — requires exactly the same planning
infrastructure that Sales requires. `comp-simulation` models CS comp plan payout at
various attainment levels. `quota-sensitivity-analysis` stress-tests whether CS quotas
are achievable given the book of business. `annual-planning-workflow` sets the CS
revenue targets for the year. `mid-year-replan-triggering` fires when CS is drifting
off its expansion or retention plan and a replan is warranted. None of these are
optional for an org that's going to report on revenue contribution.

**Important qualifier:** These skills apply only to CS orgs with formal quota-carrying
structures. For CS orgs in a pure post-sales service model, these skills are not yet
relevant. The plugin's cold-start interview should detect the CS touch model and
suppress these skills in non-quota-carrying configurations. This is a
**configuration-gated capability**, not a universally active one.

### Deal Desk and Commercial Terms Cluster (3 skills)

`deal-desk-workflow-management`, `non-standard-terms-detection`,
`change-communication-packaging`

**Why they're required:** Deal desk has two distinct application contexts in this plugin:

1. **Bridge function:** Reviewing commercial structure at the Sales→CS handoff gate.
   CS needs to know what non-standard terms were agreed, what discount depth was
   accepted, and whether the deal desk approved any provisions that affect CS delivery
   scope.

2. **Expansion motion:** CS-initiated expansion deals go through the same approval
   chain as Sales deals. An AE-equivalent CS rep handling a six-figure upsell needs
   deal desk tooling for their own expansion pipeline — discount approval routing,
   non-standard term detection, and approval packaging.

**`change-communication-packaging`:** Applicable to CS. When comp, quota, or book
assignments change for CSM roles, this skill packages those communications. The
territory-change aspect does not apply (territory-optimization is removed), but quota
changes, CS role restructuring, and comp plan updates are legitimate use cases.

### Remaining Sales Ops: `next-best-action-recommendation` (1 skill)

**Why it's required:** For expansion sales running inside CS — a CSM identifying an
upsell opportunity, staging it through an expansion pipeline, and managing it toward
close — this skill surfaces deal rescue and progression interventions when the
opportunity is stalling. It applies to the CS-owned expansion motion in the same way
it applies to new logo Sales. The pipeline it operates on is the CS expansion
pipeline.

---

## Skills Requiring Scoping Adjustment (6)

These skills have genuine value but need framing adjustments to make their dual
application contexts explicit — bridge function and CS revenue function both — so
users understand when to reach for them.

### `gtm-unified-metrics-pulse`
Section 1 (pipeline → forecast → closed/won) needs to be extended to include the CS
pipeline alongside the Sales pipeline. As written, it reports only Sales metrics.
**Fix:** Make Section 1 a revenue-system view — new logo pipeline + expansion pipeline
+ renewal pipeline — explicitly including CS-owned ARR. Sections 2–5 are already
correctly scoped.

### `deal-health-scoring`
Five-dimension scoring currently reads as Sales deal qualification. Dimension 5 (CS
pre-close engagement) is the bridge. The other four dimensions apply equally to
expansion deals in the CS pipeline. **Fix:** Clarify in framing that this skill applies
to both new-logo pipeline (Sales) and expansion pipeline (CS). The output interpretation
differs by deal type — a CS-originated expansion deal scores differently than a Sales
new-logo deal — but the scoring model is the same.

### `deal-classification`
New ARR / Expansion / Renewal / Reactivation. Already the right taxonomy for the CS
revenue function. **Fix:** Add explicit documentation that Expansion and Renewal
classifications route to CS-owned pipeline tracking and CS deal desk, not Sales.
The classification is the routing mechanism.

### `discount-threshold-monitoring`
The discount threshold approval chain applies to both Sales and CS expansion deals.
**Fix:** Extend the configuration to support separate threshold levels for CS-originated
expansion deals vs. Sales new-logo deals. The approval routing chain may differ — a CS
leader approving an expansion discount vs. an AE manager approving a new logo discount.

### `growth-model-vs-actuals-tracking`
The three growth vectors (new logo, expansion NRR, retention GRR) correctly span both
sides of the revenue system. **Fix:** Clarify in framing that Vector 2 (expansion NRR)
and Vector 3 (retention GRR) are CS ownership signals — CS is accountable for these
numbers in the same way Sales is accountable for Vector 1.

### `field-completion-monitoring`
The `ocv_entry_referenced` and `cs_handoff_owner_assigned` gate fields are on-target.
**Fix:** Add CS-side stage gate monitoring for the expansion motion — an expansion deal
moving through the CS pipeline should require equivalent field completion (e.g., OCV
entry referenced for the expansion scope, commercial terms documented, renewal contract
confirmed) at the relevant CS deal stages.

---

## Remove (1 skill)

### `territory-optimization`
This is the only skill with no application context in the CS revenue center model. CS
portfolio assignment is an account-coverage and capacity-matching problem, not a
geographic or segment territory optimization problem. The logic — minimizing travel
distance, maximizing segment density, balancing quota by territory — does not transfer.
CS book-of-business allocation belongs to the capacity modeling layer
(`closed-won-to-cs-capacity-modeling` and `unit-of-growth-calculator`), not a territory
optimizer.

**Recommendation:** Remove. No CS application context exists for this skill as designed.

---

## Path Mismatch (Open Technical Issue)

28 skills reference `reference/revops-domain-model.md` but the file lives at
`shared/revops-domain-model.md`. Correct relative path from
`rev-ops/skills/<skill-name>/SKILL.md` is `../../../shared/revops-domain-model.md`.
This is a read-time failure at runtime — any skill that attempts to load the domain
model will fail silently or error. Needs a fix pass across all 28 affected skills.

---

## Configuration-Gated Capabilities

Several skill clusters are relevant only for CS orgs that have reached the revenue
center operating model. The cold-start interview should detect org type and suppress
or surface these accordingly:

| Capability cluster | Gate condition |
|---|---|
| Forecasting & pipeline | CS org tracks expansion/renewal pipeline formally |
| Planning & incentive | CS org carries quota (expansion, renewal, or both) |
| Deal desk (expansion) | CS org closes expansion deals with commercial terms |
| Comp simulation / quota sensitivity | CS org has formal quota-carrying CSM roles |

For a CS org still operating in pure post-sales service mode, the bridge skills (core
12) are what matter. The revenue function skills activate as the org matures into
quota-carrying, pipeline-owning operation.

---

## Summary

The plugin's scope is correct. The original review applied a traditional RevOps lens
that treated these skills as Sales operations infrastructure. The correct lens is CS
operating as a revenue center with its own pipeline, its own quota, its own deal desk,
and its own planning cycle — plus the Sales→CS bridge that connects the two revenue
functions.

The single removal (`territory-optimization`) reflects a genuine mismatch between the
skill's design assumptions (geographic/segment territory optimization) and the CS
portfolio assignment model. Everything else has a legitimate application context in
either the bridge function, the CS revenue function, or both.

The 6 scoping adjustments are about making the dual-context application explicit in
each skill's framing — so a CS leader reaching for `pipeline-coverage-analysis` knows
it applies to their renewal and expansion book, not just the Sales pipeline.

**Action items:**
1. Remove `territory-optimization`
2. Apply the 6 scoping adjustments described above
3. Fix the path mismatch across 28 skills (`reference/` → `../../../shared/`)
4. Update `cold-start-interview` to detect CS operating model maturity and gate
   the revenue function skill clusters accordingly

---

*Reviewed against: Revenue-Orchestration-Playbook-Part-1-Framing-v1.0.md,
revops-domain-model.md (v1.0, 2026-05-18), full read of all 35 SKILL.md files,
user clarification on CS-as-revenue-center mandate (2026-05-18).*
