---
name: health-score-review
description: >
  Structured health review for one account or a portfolio cohort — health signal
  breakdown, trend analysis, risk classification, and recommended actions. Use
  for weekly account reviews, portfolio triage, or when a health alert fires.
  Applies your configured health model components and thresholds.
argument-hint: "[account name | --portfolio] [--triage | --deep]"
version: "1.0.0"
---

# /health-score-review

Review account health using your configured health model — signal by signal,
not just a color verdict.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to load:
- Health model components and weights (e.g., usage 40%, engagement 20%, support 20%, NPS 20%)
- Red threshold and Yellow threshold
- Churn signal definitions
- Escalation matrix — what triggers escalation and to whom

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores are heuristics — never frame as churn predictions), G4 (no escalation triage without a named escalation path in config), G5 (confidentiality check before distributing portfolio-level health data), G7 (flag any stale health data with source date and staleness indicator).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

**Single account review:** Default. Produce a full health breakdown for one account.

`--triage`: Portfolio triage — rapid scan of all accounts in the book; surface
Yellow and Red accounts only; no deep analysis per account. Returns a prioritized
list with top risk factor per account.

`--deep`: Full account analysis — health signal breakdown, trend direction over
30/60/90 days, root cause hypothesis, and recommended intervention.

`--portfolio`: Alias for `--triage`.

---

## Data gathering

### Single account

Pull from connected integrations per configured profile:
- CS Platform: current health score, component breakdown, lifecycle stage, CTAs
- Product data / CRM: usage metrics (DAU, feature adoption, last login)
- Support: open tickets, P1/P2 history, ticket velocity
- Call recording: engagement frequency, last call date, attendees
- NPS: most recent score and date

Fallback if nothing connected:
> "I need health signal data for this account. Share what you have — a CS Platform
> export, recent usage numbers, last call date, or NPS score. Even partial data
> produces a more useful review than a blank sheet."

### Portfolio triage

Pull account list from CRM or CS Platform. For each account: current health
score (or last known), days since last contact, renewal date.

If CRM is not connected:
> "For portfolio triage, paste your account list with current health status,
> ARR, and renewal dates. I'll prioritize from there."

---

## Single account health review

---

**Health Review — [Account Name]**
*[Date] · [CS motion] · [Segment]*

---

### Health summary

| Component | Weight | Signal | Direction | Score contribution |
|-----------|--------|--------|-----------|-------------------|
| [Component 1: e.g., Product usage] | [configured %] | [current value] | [↑↓→ vs 30-day] | [Red/Yellow/Green for this component] |
| [Component 2: e.g., Engagement] | [configured %] | [last contact: N days] | [↑↓→] | |
| [Component 3: e.g., Support] | [configured %] | [N open tickets / P1: Y/N] | [↑↓→] | |
| [Component 4: e.g., NPS] | [configured %] | [score / date] | [↑↓→] | |
| [Additional configured component] | | | | |

**Overall health:** [Red / Yellow / Green]
*Threshold applied: Red = [configured], Yellow = [configured]*

If no CS Platform configured and components are not defined: use the manual
signal prompts from the practice profile (what signals make you worried).
Classify as [At Risk / Watch / Healthy] based on signals present.

---

### Signal narrative

3-5 sentences interpreting the component breakdown. Do not just restate the table.

> "The account's product usage component is the primary concern — weekly active
> users dropped 22% over 30 days, which puts this below the configured Yellow
> threshold. Engagement is holding: the last call was [N] days ago, within the
> [configured threshold] for [high-touch/tech-touch]. Support load increased
> (3 open tickets vs. 1 last month), but none are P1/P2. NPS is from [N] months
> ago — stale enough to flag for update."

Language always shows components and evidence — not a verdict like "this account
is likely to churn."

---

### Churn signals present

From configured churn signal definitions:

| Signal | Present | Evidence | Weight |
|--------|---------|----------|--------|
| Executive sponsor departure | [Yes / No / Unknown] | [context] | High |
| Product usage drop >20% | [Yes / No] | [% change] | High |
| Open escalation or P1 ticket | [Yes / No] | [ticket details] | High |
| NPS detractor + no recovery | [Yes / No] | [score + date] | Medium |
| Missed QBR or no-show pattern | [Yes / No] | [last attended: date] | Medium |
| Competitor evaluation underway | [Yes / No / Unknown] | [source] | High |
| No contact in >[threshold] days | [Yes / No] | [last contact: date] | Medium |

Flag each present signal as `[review]` with the specific evidence.

---

### Risk classification

Based on configured thresholds and signals present:

**Classification:** [Red — immediate intervention / Yellow — monitor and engage /
Green — healthy / Unknown — data insufficient]

**Escalation trigger:** [Does this account meet the configured escalation threshold?]
If yes: "Route per matrix — [escalation route from config] within [SLA]."
If no: "Below escalation threshold. CSM-managed watch."

---

### Trend analysis

If historical data is available (CS Platform or prior account-research sessions):

| Metric | 90 days ago | 60 days ago | 30 days ago | Today | Trend |
|--------|------------|------------|------------|-------|-------|
| [Health score or primary metric] | | | | | [↑↓→ and rate] |
| [Usage metric] | | | | | |

If trend data is unavailable: "Trend analysis not available — no historical signal
data retrieved this session. Point-in-time assessment only."

**Trend interpretation:** Is the account stable, improving, or declining? Name
the direction and the rate of change. A slow decline is different from a sudden
drop.

---

### Recommended interventions

Calibrate to the risk classification and configured CS motion.

**Red account:**
1. [Specific action with timeline] — e.g., "Escalate to [route from matrix] within [SLA]"
2. [Specific outreach action] — e.g., "Request executive sponsor check-in within 48h"
3. [Recovery action] — e.g., "Run risk-flag to prepare structured memo: `/csm:risk-flag [account]`"

**Yellow account:**
1. [Specific monitoring action] — e.g., "Proactive check-in call within 7 days focused on [specific signal]"
2. [Prevention action] — e.g., "Engage champion on usage drop — ask what changed"
3. [Escalation prep] — e.g., "If [specific trigger] occurs, escalate per matrix"

**Green account:**
1. [Growth action] — e.g., "Schedule QBR if >90 days since last one"
2. [Expansion awareness] — internal note only, tagged `[early signal — not yet qualified]`

Do not produce generic interventions like "monitor closely" or "improve
engagement." Every recommendation is specific — who, what, when.

---

## Portfolio triage (`--triage`)

Return a ranked list — highest risk first.

---

**Portfolio Health Triage**
*[Date] · [N accounts reviewed]*

---

**Red accounts — immediate action:**

| Account | ARR | Renewal | Top risk signal | Recommended action |
|---------|-----|---------|----------------|-------------------|
| [Account] | $[ARR] | [Date] | [1-line signal] | [Specific action] |

**Yellow accounts — watch:**

| Account | ARR | Renewal | Top risk signal | Recommended action |
|---------|-----|---------|----------------|-------------------|
| [Account] | $[ARR] | [Date] | [1-line signal] | [Specific action] |

**Accounts approaching renewal (<90 days):**

| Account | ARR | Renewal | Health | Risk signal |
|---------|-----|---------|--------|------------|
| [Account] | $[ARR] | [Date] | [R/Y/G] | [Signal] |

**Summary:**
- [N] Red accounts · [N] Yellow accounts · [N] approaching renewal
- Total ARR at risk: $[sum of Red + Yellow + <90 day]
- Highest priority: [account name] — [reason]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live — health score + components | CRM ✓ live — usage + engagement | user provided | conversation context only]
> - **Health model applied:** [Components and weights from config | user-defined signals | no formal model — signals only]
> - **Data as of:** [timestamp per source]
> - **Staleness flags:** [NPS from [N] months ago — stale | usage data confirmed live | engagement from last call [date]]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]

---

## Output

Health review report — format driven by `--single` (default) or `--triage` flag.
Single-account mode produces a structured markdown brief with signal inventory,
score justification, and recommended actions. Portfolio triage produces a ranked
table with risk tier, primary driver, and next action per account.

## Guardrails

**Health scores are heuristics, not verdicts.** The output shows component signals
and the account's position relative to configured thresholds. It does not say "this
account will churn." That inference is the CSM's judgment.

**No escalation without context.** When the skill recommends escalation, it names
the route (person, channel, SLA) from the configured escalation matrix. A flag
without a path does not help.

**No silent data gaps.** If a component is missing (NPS not available, usage data
stale, no CS Platform connected), the reviewer note names the gap and the health
classification is adjusted accordingly ("classification is based on partial signal
data — [component] unavailable").

**Churn signals require evidence.** A signal is marked present only if there is
direct evidence. Absence of data is "Unknown," not "No."

**Portfolio triage contains account-level data.** Distribution of the triage
report outside the CS team requires a destination check — ARR values and health
classifications are confidential.

---

## After the review

- Red account: "Want a structured risk memo? `/csm:risk-flag [account]`"
- Approaching renewal + Yellow/Red: "Run renewal readiness: `/csm:renewal-readiness [account]`"
- Executive sponsor signal: "Check stakeholder map: `/csm:stakeholder-map [account] --sponsor-risk`"
- Portfolio triage complete: "Want deep reviews on the top 3 Red accounts? Name them and I'll run `/csm:health-score-review --deep` on each."
