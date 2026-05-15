---
name: capacity-planner
description: >
  Assess CSM capacity and coverage across the book — current load vs. target
  ratios, coverage gaps by segment and motion, headcount recommendations, and
  account redistribution options. Use for quarterly planning cycles, headcount
  requests, CSM departure coverage, or when Red-tier concentration suggests
  a coverage problem rather than a product or relationship problem. Produces
  a capacity assessment with specific redistribution or hiring recommendations.
argument-hint: "[--current | --headcount | --redistribution | --departure <csm-name>]"
version: "1.0.0"
---

# /cs-ops:capacity-planner

Know whether CSMs have too much on their plate — and what to do about it.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Target CSM-to-account ratios per segment and motion
- Total CSM headcount and motion breakdown
- Segment definitions and assignment method
- CS motion type per segment

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G4 (verify a named capacity alert escalation path is configured before surfacing over/under-allocation flags).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--current`: Current capacity state — actual vs. target ratios per CSM,
load distribution, overloaded and underloaded CSMs. **Default.**

`--headcount`: Headcount requirement analysis — how many CSMs are needed
based on current ARR, segment mix, and target ratios. Suitable for hiring
requests or board presentations.

`--redistribution`: Account redistribution plan — which accounts should move
between CSMs to balance load without hiring. Produces a specific redistribution
recommendation.

`--departure <csm-name>`: Coverage plan for a CSM departure or leave —
how to redistribute their accounts, which accounts need immediate attention.

---

## Data gathering

Pull from connected integrations:
- CRM: account list with ARR, segment, CSM owner
- CS Platform: health scores per account, lifecycle stage, active CTAs
- CS-Ops config: target ratios per segment, headcount, motion assignments

If nothing is connected:
> "For capacity planning, I need: total accounts, ARR, segment, health tier,
> and CSM owner for each account. Share a roster export and I'll run the analysis."

Minimum required: account count per CSM, segment classification per account,
and configured target ratios.

---

## Current capacity assessment (`--current`)

---

**CSM Capacity Assessment**
*[Date] · [N] CSMs · [N] accounts · $[total ARR] · INTERNAL*

---

### Portfolio capacity summary

| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Total accounts | [N] | — | — |
| Total CSMs | [N] | — | — |
| Avg accounts per CSM | [N] | [configured target] | [✅ / ⚠️ Over / ⚠️ Under] |
| Avg ARR per CSM | $[amount] | — | — |
| CSMs at or over capacity | [N] ([%]) | 0 | [⚠️ Flag if > 0] |
| Accounts with no CSM | [N] ($[ARR]) | 0 | [⚠️ Flag if > 0] |

---

### CSM-level capacity view

| CSM | Motion | Accounts | Target | Over/Under | ARR managed | Red accounts | Yellow accounts |
|-----|--------|----------|--------|-----------|-------------|-------------|----------------|
| [CSM 1] | [High-touch] | [N] | [N] | [+N / -N] | $[amount] | [N] | [N] |
| [CSM 2] | | | | | | | |
| [Unassigned] | — | [N] | 0 | +[N] | $[amount] | [N] | [N] |

**Capacity flags:**

For each CSM carrying more than the configured target:
> "**[CSM name]** is carrying [N] accounts vs. the [target]-account target for
> [motion] CSMs — [+N] over capacity. Their Red account count is [N],
> which is [above / at / below] the expected proportion for an over-capacity CSM.
> This load should be relieved before the next renewal cycle." `[review]`

For each CSM carrying fewer than 80% of target:
> "**[CSM name]** is at [N] accounts ([%] of target). They have available
> capacity to absorb [N] additional accounts without exceeding the target ratio."

---

### Capacity by segment

| Segment | Accounts | CSMs assigned | Actual ratio | Target ratio | Status |
|---------|----------|--------------|-------------|-------------|--------|
| [Enterprise] | [N] | [N] | 1:[N] | 1:[target] | [✅ / ⚠️ Over / ⚠️ Under] |
| [Mid-market] | [N] | [N] | 1:[N] | 1:[target] | |
| [SMB] | [N] | [N] | 1:[N] | 1:[target] | |

**Segment interpretation:**
[1-2 sentences on the most significant segment capacity finding — where the
gap is worst, and what it implies for health outcomes in that segment.]

---

### Headcount requirement analysis (`--headcount`)

---

**Headcount Requirement Analysis**
*[Date] · For planning / hiring request use*

**Baseline inputs:**
- Current ARR: $[total]
- Current accounts: [N]
- Target ratios: [Enterprise 1:[N] / Mid-market 1:[N] / SMB 1:[N]]
- ARR growth assumption: [If provided by user / Not provided — analysis uses current ARR only]

**Required CSM headcount at current ARR:**

| Segment | Accounts | Target ratio | CSMs required | CSMs current | Gap |
|---------|----------|-------------|--------------|-------------|-----|
| [Enterprise] | [N] | 1:[N] | [N needed] | [N have] | [+N hire / -N over] |
| [Mid-market] | [N] | 1:[N] | [N needed] | [N have] | |
| [SMB] | [N] | 1:[N] | [N needed] | [N have] | |
| **Total** | [N] | — | [N needed] | [N have] | [Net gap: +N / -N] |

**Scenario: [N]% ARR growth (if growth assumption provided):**

| Segment | Projected accounts | CSMs required | Current | Additional hires needed |
|---------|-------------------|--------------|---------|------------------------|
| [Enterprise] | [N projected] | [N] | [N] | [N] |

**Headcount recommendation:**

> "[N] additional CSMs are needed to bring coverage to target ratios at current
> ARR. Prioritize hiring for [segment] — this segment has the largest gap and
> the highest ARR concentration. If headcount cannot be approved, redistribution
> within the current team will bring [segment] to [N] accounts per CSM — still
> above target, but lower than the current [N]." `[review — confirm with CS lead]`

**Cost context:**
[If CSM fully-loaded cost is configured or provided: "At [cost] per CSM,
[N] additional hires represent $[amount] in annualized cost." Otherwise omit.]

---

### Account redistribution plan (`--redistribution`)

---

**Account Redistribution Plan**
*[Date] · For load balancing without hiring*

**Redistribution principles:**
- Do not redistribute Red accounts to CSMs who are already at or over capacity
- Prioritize moving accounts closest to renewal to CSMs with available bandwidth
- Do not move high-ARR accounts without a warm handoff plan
- Redistribution requires CSM + customer notification — account moves are not silent

**Proposed moves:**

| Account | ARR | Health | From CSM | To CSM | Rationale |
|---------|-----|--------|---------|--------|-----------|
| [Account] | $[amount] | [🟢/🟡/🔴] | [CSM 1] | [CSM 2] | [CSM 1 is +[N] over; CSM 2 has [N] slots] |

**Post-redistribution ratios:**

| CSM | Accounts before | Accounts after | Target | Status |
|-----|----------------|----------------|--------|--------|
| [CSM 1] | [N] | [N] | [N] | [✅ / still ⚠️] |
| [CSM 2] | [N] | [N] | [N] | |

**Handoff requirements:**
For each account to be moved:
- [Account]: [Account health and relationship notes for receiving CSM. Any
  active plays or open escalations that must transfer cleanly.]

---

### CSM departure coverage (`--departure <csm-name>`)

---

**Departure Coverage Plan — [CSM name]**
*[Date] · [N] accounts · $[ARR] · Urgency: [immediate / planned]*

**Portfolio being redistributed:**

| Account | ARR | Health | Renewal | Active play/CTA | Priority |
|---------|-----|--------|---------|----------------|---------|
| [Account] | $[amount] | 🔴 | [date] | [Yes/No] | [Immediate / Standard] |

**Immediate priority accounts (Red or renewal <60 days):**
[List — these accounts need assignment within 24 hours of departure]

**Standard priority accounts:**
[List — assign within one week]

**Proposed redistribution:**

| To CSM | Accounts assigned | Post-addition total | Target | Status |
|--------|-----------------|-------------------|--------|--------|
| [CSM 2] | [account list] | [N] | [N] | [✅ / ⚠️] |

**Departure checklist:**
1. [ ] Immediate-priority accounts assigned within 24 hours
2. [ ] Warm introductions sent for high-ARR accounts (>$[configured threshold])
3. [ ] Active escalations transferred per escalation matrix — new owner named
4. [ ] Open QBRs and renewal conversations flagged for incoming CSM
5. [ ] Account notes and success plans accessible to receiving CSMs
6. [ ] CRM CSM owner field updated for all transferred accounts

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CS Platform ✓ live | user-provided roster | conversation context only]
> - **Ratios applied:** [Configured target ratios from cs-ops CLAUDE.md | User-provided this session]
> - **Unassigned accounts:** [N accounts with no CSM owner — excluded from per-CSM ratios; included in headcount requirement]
> - **Data as of:** [timestamp per source]
> - **Redistribution plan:** Review with CS lead before executing — account moves affect customer relationships and require warm handoffs for accounts above $[configured ARR threshold].
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]

---

## Output

Mode-specific capacity assessment — format driven by `--current` (default), `--plan`,
or `--model` flag. Each mode produces a structured markdown report with: current state
summary, utilisation metrics, identified gaps or risks, and recommended actions.
See **Current capacity assessment** section for field-level detail.

## Guardrails

**Capacity ratios are targets, not hard limits.** A CSM carrying 10% over
target is not necessarily failing — context matters. Flag the deviation;
do not declare the situation broken without surfacing relationship and health
context.

**Red accounts are not movable without a plan.** Never recommend moving
a Red account to a new CSM without a warm handoff and continuity plan.
A cold handoff during a recovery situation worsens churn risk.

**Headcount recommendations require business context.** The headcount
analysis produces a coverage-based number. Hiring decisions involve cost,
pipeline, and strategic priority — flag that the recommendation should be
reviewed alongside these factors.

**Unassigned accounts are a coverage gap.** Any account without a CSM
owner is flying blind. Surface the full list and flag it — do not include
unassigned accounts in CSM-level averages without noting the exclusion.

**Departure plans require urgency calibration.** Distinguish planned
departures (2-4 weeks lead time) from immediate departures. A same-day
departure with a Red account approaching renewal is a different priority
from a planned departure with 30 days notice.

---

## After the assessment

- "Coverage gaps confirmed — run segment analysis: `/cs-ops:segment-analyzer`"
- "Headcount case ready — produce metrics dashboard for leadership: `/cs-ops:metric-dashboard`"
- "Departure plan complete — document the process: `/cs-ops:process-doc --csm-handoff`"
- "Data missing from CRM (no CSM owner on accounts) — fix it: `/cs-ops:data-quality-check`"
