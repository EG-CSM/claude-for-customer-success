---
name: milestone-tracker
description: >
  Track milestone progress across one account or your full onboarding book of business.
  Reads milestone framework, at-risk signals, and escalation thresholds from your
  onboarding profile. Pulls current milestone status from your PM connector (Asana,
  Linear, Jira, or Monday) if configured, or from CSM input. Use --status (default)
  for a current-state view of one account's milestones, --portfolio for a milestone
  health summary across all active onboarding accounts, or --flag to surface all
  accounts with at-risk or overdue milestones and recommended actions.
argument-hint: "[<account-name-or-ID>] [--status | --portfolio | --flag]"
version: "1.0.0"
deployment_target: plugin
---

<!-- Status: [PROPOSED] -->

# /onboarding:milestone-tracker

Milestone health tracking — single account or portfolio view.

---

## Pre-flight

Read both configuration files before running any milestone tracking:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- Milestone framework (M1–M5 day targets, completion criteria, at-risk signals —
  required for date calculations and risk assessment)
- Escalation matrix (thresholds for escalating at-risk milestones — who gets notified
  and when)
- Onboarding model (affects which milestones are CSM-led vs. customer-led vs. partner-led)
- Duration targets by segment (anchors the expected M5 date for portfolio comparison)

If milestone framework is `[PLACEHOLDER]`:
> "Milestone targets aren't configured. Run
> `/onboarding:cold-start-interview --section milestones` before running milestone
> tracking — without configured targets, risk assessment will use generic defaults
> that may not match your actual onboarding model."

Proceed with generic defaults if confirmed.

---

## Trigger Precision

**Use when:**
- Checking the current milestone status and pace for one or more onboarding accounts (`--status`)
- Generating a portfolio heat map of milestone health across all active accounts (`--portfolio`)
- Triaging at-risk accounts and producing prioritized intervention actions (`--flag`)

**Do NOT use for:**
- Diagnosing a specific active blocker (use `/onboarding:blocker-review --diagnose`)
- Time-to-value analysis with segment-normalized benchmarking (use `/onboarding:ttv-analysis`)
- Generating the onboarding plan or updating milestone targets (use `/onboarding:onboarding-plan`)

## Typical Activation
- "Where are we on milestones for [Account]?"
- "Show me the portfolio heat map for all active accounts"
- "Which accounts are at risk this week?"
- CSM runs `/onboarding:milestone-tracker [account] --status` to check a single account's milestone progress
- CSM runs `/onboarding:milestone-tracker --portfolio` to generate a portfolio-wide milestone heat map
- CSM runs `/onboarding:milestone-tracker --flag` to surface at-risk accounts for intervention

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of milestone tracking request is this?
   - **Single-Account Status**: One named account, CSM wants current milestone state before a touchpoint or review. Optimize for recency and actionable next-step.
   - **Portfolio Health Scan**: Cross-account milestone view for book-of-business management or 1:1 prep. Requires segment normalization and consistent structure.
   - **At-Risk Triage**: Surface accounts needing intervention — overdue or signal-triggered. Score by signal severity first, then date proximity.
   - **Escalation-Ready Brief**: Specific account has breached escalation thresholds — output feeds an escalation workflow. Pair flag with root cause and escalation matrix routing.

2. **CONSTRAINTS**: What limits the solution space?
   - G7: All milestone data must carry a source timestamp and staleness indicator — PM connector data >24h old is flagged, manual input is labeled as such.
   - G5: TtV projections and internal planning targets appear only in internal sections and reviewer notes — never in customer-facing output.
   - G4: Escalation recommendations route through the configured escalation matrix with named owner, channel, and SLA — no generic "escalate to your manager."
   - G2: Portfolio output is internal-only by default — apply confidentiality check before any distribution beyond the CSM.
   - G1: Overdue is a flag, not a verdict — do not present an overdue milestone as a failure without CSM context on agreed deferrals or dependencies.
   - Contract start date is the anchor for all date calculations — if missing, all milestone dates for that account are `[unverified]`. Never silently estimate.

3. **EXPERT CHECK**: What would a veteran onboarding manager verify first?
   - Are behavioral at-risk signals (no login, missing attendees, credentials not received) assessed independently of date math? A milestone with 15 days remaining but a confirmed signal is more urgent than one 2 days overdue with no signal.
   - Is milestone pace normalized to segment-specific duration targets from config? Enterprise M3 at Day 30 is on track; SMB M3 at Day 30 may be overdue.
   - When PM connector data conflicts with CSM-reported status, is the discrepancy surfaced rather than silently resolved? The conflict itself is a signal.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting stale PM data without a timestamp or staleness flag — the CSM acts on outdated milestone completion status.
   - Sorting at-risk triage by days-overdue alone, missing accounts with behavioral signals that haven't breached date thresholds yet.
   - Recommending generic actions ("follow up with the customer") instead of pulling specific escalation steps from the configured matrix.
   - Comparing SMB and enterprise accounts on the same absolute day thresholds without normalizing to segment duration targets.
   - Running date calculations when contract start date is missing or estimated — every downstream milestone target becomes unverified.
   - Escalating from portfolio view alone without running single-account status first for full context.

**After execution**, verify:
- Does the output match the requested mode (--status / --portfolio / --flag) and the actual need?
- Are all data sources timestamped and staleness-flagged per G7?
- Are at-risk signals assessed independently of date math, not just as a date countdown?
- Confidence: [High] if PM connector + CRM data corroborate / [Medium] if single-source or partially stale / [Low] if manual input only — state which.

## Mode

`--status` (default): Current milestone status for one named account. Shows milestone
table with dates, completion status, days-to-next-milestone, at-risk signals, and
recommended actions. Use before a customer touchpoint or QBR prep.

`--portfolio`: Milestone health summary across all active onboarding accounts. Requires
either a PM connector or a list of account names with contract start dates from the
CSM. Output is a portfolio heat map — not a per-account deep-dive.

`--flag`: At-risk and overdue milestone report. Surfaces only accounts with problems:
overdue milestones, approaching at-risk thresholds, blocked owners, or missing milestone
evidence. Ordered by severity (overdue first, then approaching deadline, then at-risk signal
count). Includes recommended action per flagged account.

---

## Account identification and data pull

### `--status` mode

Ask: "Which account?" If a CRM connector is available, pull contract start date and
CSM/AE assignment. If a PM connector is configured, pull current task status for
this account's milestone tasks.

PM connector pull (if available):
> "[PM: Asana/Linear/Jira/Monday]: [account name] project · [N] tasks found ·
> M[#] in progress · data as of [timestamp]"

If no PM connector:
> "No PM connector configured. Tell me: which milestone is currently active, what's
> complete, and the contract start date — I'll calculate dates and assess risk from
> that."

### `--portfolio` mode

If PM connector available:
> "[PM]: pulling all projects tagged as onboarding accounts..."

If not: "Provide a list of active onboarding accounts with their contract start dates
and current milestone status — I'll build the portfolio view from that input."

### `--flag` mode

Requires either PM connector (preferred) or CSM-provided account list with current
milestone status and contract start dates.

---

## Milestone status calculation

For each milestone, calculate:

1. **Target date** = contract start date + milestone day target from config
2. **Days remaining** = target date − today
3. **Status** — assign one of:
   - `On track` — target date is ≥ 5 days away and no at-risk signals present
   - `Due soon` — target date is 1–4 days away; escalate preparation
   - `At risk` — at-risk signals present (see below) OR days remaining < at-risk
     threshold from config
   - `Overdue` — target date is in the past; milestone not marked complete
   - `Complete` — milestone confirmed complete with evidence

**At-risk signal assessment:**

For each milestone, check the at-risk signals from config. Generic defaults (override
with config values):

| Milestone | At-risk signals |
|-----------|----------------|
| M1 | Required attendees not confirmed 48h before kickoff |
| M2 | Integration credentials not received by Day 7 |
| M3 | No product login activity in the first 14 days |
| M4 | No documented use case completion by Day 25 |
| M5 | Success criteria not confirmed by Day 45 |

Flag an account as At risk if any signal is present, regardless of days remaining.

**Days-overdue escalation thresholds** (from config; defaults below):

| Days overdue | Action |
|-------------|--------|
| 1–3 days | CSM self-resolve — reach out to customer champion |
| 4–7 days | Involve AE or escalation contact from config |
| 8+ days | Executive escalation (if white-glove) or formal risk flag |

---

## `--status` output

```
Milestone Status — [Account Name]
Contract start: [date] · CSM: [name] · Model: [onboarding model]
Generated: [today]

| Milestone | Target | Status | Days remaining | Signal |
|-----------|--------|--------|---------------|--------|
| M1: Kickoff | [date] | Complete ✓ | — | — |
| M2: Tech setup | [date] | [status] | [N] | [signal or —] |
| M3: First use | [date] | [status] | [N] | [signal or —] |
| M4: First value | [date] | [status] | [N] | [signal or —] |
| M5: Handoff ready | [date] | [status] | [N] | [signal or —] |

Current milestone: M[#] — [label]
Next action: [specific recommended action based on current status]

[If any milestone is At risk or Overdue:]
⚠ Risk detail: [signal description and recommended escalation action]
```

**Internal section (not for sharing):**

```
TtV projection [review — internal planning target]:
  Current pace: [N days from start to estimated M5]
  Segment target: [X days]
  Gap/surplus: [±Y days — on track | behind | ahead]

Escalation threshold: [current status vs. config thresholds]
```

---

## `--portfolio` output

```
Onboarding Portfolio — Milestone Health
Generated: [today] · [N] active accounts

| Account | Model | M current | Status | Days remaining | Flag |
|---------|-------|-----------|--------|---------------|------|
| [name] | [model] | M[#] | On track | [N] | — |
| [name] | [model] | M[#] | At risk | [N] | ⚠ [signal] |
| [name] | [model] | M[#] | Overdue | -[N] | 🔴 [days overdue] |

Summary:
  On track:  [N] accounts
  Due soon:  [N] accounts
  At risk:   [N] accounts
  Overdue:   [N] accounts

[If at-risk or overdue accounts exist:]
Recommended first action: [highest-severity item]
```

---

## `--flag` output

Ordered by severity — overdue first, then at-risk, then due soon.

```
At-Risk and Overdue Milestones — [today]

🔴 OVERDUE ([N] accounts)

[Account name] · M[#]: [milestone label] · [N] days overdue
  Signal: [specific signal]
  Recommended action: [escalation step from config escalation matrix]
  Owner: [CSM name]

⚠ AT RISK ([N] accounts)

[Account name] · M[#]: [milestone label] · [N] days remaining
  Signal: [specific at-risk signal]
  Recommended action: [proactive step before milestone becomes overdue]

🟡 DUE SOON ([N] accounts)

[Account name] · M[#]: [milestone label] · [N] days remaining
  Preparation needed: [next action]

---
Accounts reviewed: [N] · No issues: [N] · Flagged: [N]
```

---

## Reviewer note (internal — `--status` and `--portfolio` only)

> ⚠️ Reviewer note
> - **Sources:** [PM connector ✓ | CRM ✓ | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** milestone framework (M1 [X]d, M2 [X]d, M3 [X]d,
>   M4 [X]d, M5 [X]d), escalation thresholds ([values])
> - **At-risk signals evaluated:** [list of signals checked per milestone]
> - **TtV projection:** [status vs. segment target — internal only]
> - **Flagged for your judgment:** [accounts requiring immediate action | none]
> - **Data gaps:** [accounts where contract start date was not available from CRM
>   — dates are estimates | none]

---

## Output

Milestone tracking output — format driven by flag (`--status`, `--portfolio`,
`--flag`). Status mode: per-account milestone table with RAG status and next action.
Portfolio mode: cross-account summary table. Flag mode: at-risk milestone alert.
See mode-specific sections for field-level structure.

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill

---

## Security & Permissions

This skill operates read-only against configuration files and connected MCP data sources.
No filesystem writes, no subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

All milestone data is timestamped and staleness-flagged per G7 (PM connector >3 days, CRM >7 days).
At-risk flags are calculated from milestone math and configured at-risk signals — not from CSM narrative.
Portfolio outputs containing account-level health data require confidentiality check before sharing beyond the CSM.
CSM judgment is required for intervention actions — skill presents options, never directives.

## Guardrails

**At-risk signals override date-only assessment.** A milestone with 10 days remaining
but a confirmed at-risk signal is flagged as At risk — not On track. Days remaining is
a countdown; at-risk signals are behavioral evidence. Both matter.

**TtV projection is internal.** The internal section with TtV labels appears only in
internal outputs and reviewer notes. Customer-facing milestone views show milestone
dates and completion status — not TtV framing.

**`--portfolio` is a health map — not account management.** The portfolio view surfaces
which accounts need attention. It does not replace per-account context. Before escalating
an at-risk flag, run `--status` on that account to understand the full picture.

**Overdue ≠ failed.** An overdue milestone may be legitimately deferred (customer
request, technical dependency, agreed scope change). The tracker flags it; the CSM
judges it. Do not present an overdue flag as a failure without CSM context.

**PM connector data is authoritative over manual input.** If a PM connector returns
task status that conflicts with CSM input, surface the discrepancy:
> "PM connector shows M2 as incomplete, but you've indicated it's done. Confirm
> the PM task has been updated, or I'll flag this as a data inconsistency."

**`--flag` is for intervention — not reporting.** The flag output is a working
document for the CSM's internal action planning. It is not formatted for sharing
with customers, leadership, or QBR decks. Extract and format specific items for
those audiences separately.

**Missing contract start date breaks date calculation.** If the contract start date
is unavailable for any account, all milestone dates for that account are `[unverified]`.
Do not estimate contract start dates — request them from the CSM or CRM before
proceeding.
