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
---

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


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G7 (flag any milestone status data that is stale — always include source date and staleness indicator).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

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
