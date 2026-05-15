---
name: ttv-analysis
description: >
  Time-to-value analysis for onboarding performance — single account or portfolio.
  Reads TtV targets by segment and milestone framework from your onboarding profile.
  Analyzes actual milestone completion dates against targets to assess pace, surface
  pattern signals, and produce recommendations for accounts that are behind. TtV
  outputs are always labeled as internal planning targets — never presented as
  commitments to customers. Use --account (default) for a single-account TtV
  assessment, --portfolio for a comparative TtV view across all closed or active
  onboarding accounts, or --patterns to identify common delay patterns across your
  book and recommend proactive interventions.
argument-hint: "[<account-name-or-ID>] [--account | --portfolio | --patterns]"
version: "1.0.0"
---

# /onboarding:ttv-analysis

Time-to-value performance analysis — internal planning use only.

---

## Pre-flight

Read both configuration files before running any TtV analysis:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- TtV targets by segment (Enterprise / Mid-Market / SMB — the benchmarks against which
  actual performance is measured)
- Milestone framework (day targets and completion criteria — required to calculate
  actual vs. planned performance at each milestone)
- Onboarding model (white-glove accounts have different TtV expectations than
  guided-self-serve; analysis segments by model)
- At-risk signals (identifies which signals correlated with TtV delays)

If TtV targets are `[PLACEHOLDER]`:
> "TtV targets aren't configured. Run
> `/onboarding:cold-start-interview --section milestones` to set segment-level
> targets before running TtV analysis — analysis will use milestone day targets as
> a proxy without segment-level benchmarks."

Proceed using milestone day targets as the reference if confirmed.

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G7 (flag any milestone completion data that is stale — include source date and staleness indicator on all TtV figures).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--account` (default): TtV assessment for one named account. Compares actual
milestone completion dates against planned dates to calculate TtV trajectory.
Produces a pace assessment, variance breakdown by milestone, and recommended
acceleration actions if behind.

`--portfolio`: Comparative TtV analysis across multiple accounts. Requires either
a PM connector with milestone completion data or a CSM-provided list of accounts
with actual completion dates. Produces a portfolio table ranked by TtV performance.

`--patterns`: Pattern analysis across all accounts with TtV data. Identifies which
milestone transitions produce the most delay, which customer segments or onboarding
models perform best, and which blocker types correlate most with TtV extension.
Requires at least 5 accounts with complete milestone data for meaningful output.

---

## Critical framing — every output

**TtV is an internal planning metric — not a customer commitment.**

Every TtV label, target, projection, and comparison in this skill's output carries
the tag `[review — internal planning target]`. These figures never appear in
customer-facing documents, customer communications, or shared onboarding plans. They
are diagnostic tools for the CSM and their management team.

This applies without exception. If a user asks to include TtV projections in a
customer-facing document, redirect:
> "TtV targets are internal planning benchmarks — they're not appropriate for
> customer-facing materials. The customer-facing plan shows milestone dates and
> completion criteria. I can help you frame progress in those terms instead."

---

## Account identification and data pull

### `--account` mode

Ask: "Which account? Provide the account name and, if possible, the actual completion
dates for any milestones that are done."

If PM connector available, pull milestone task completion dates:
> "[PM]: [account name] · M1 complete [date] · M2 complete [date] · M3 in progress
> · data as of [timestamp]"

If CRM connector available, pull contract start date and segment:
> "[CRM]: contract start [date] · segment: [segment] · model: [onboarding model]"

If neither connector: "Tell me the account name, segment, contract start date, and
the actual dates each milestone was completed — I'll calculate TtV from that."

### `--portfolio` and `--patterns` modes

Requires data across multiple accounts. If PM connector available, pull all
onboarding projects with milestone completion dates. If not: "Provide a list or
spreadsheet with account names, segments, contract start dates, and milestone
completion dates."

---

## TtV calculation method

**TtV definition used here:** Number of days from contract start date to M4 First
value completion (the date the customer achieves their first measurable outcome).
M5 is the graduation milestone; M4 is the value milestone.

For accounts where M4 is not yet complete:
- **Actual TtV:** Not yet calculable — show projected TtV
- **Projected TtV** = contract start date + (M4 target day from config)
  adjusted for current pace (if milestones are running ahead or behind, project
  the adjustment forward)

**Pace calculation:**

For each completed milestone:
  Variance = actual completion date − planned date
  (positive = late; negative = early)

Cumulative variance = sum of all milestone variances to date.

Pace multiplier = (actual days elapsed / planned days elapsed at the same milestone)

Projected TtV = M4 day target × pace multiplier

If pace multiplier > 1.15 (more than 15% behind pace), flag as TtV at risk.
If pace multiplier < 0.85 (more than 15% ahead of pace), note as ahead of target.

---

## `--account` output

```
TtV Analysis — [Account Name]
[review — internal planning target]

Segment: [segment] · Model: [onboarding model] · CSM: [name]
Contract start: [date] · Segment TtV target: [X days]
Generated: [today]

Milestone Performance:

| Milestone | Planned date | Actual date | Variance | Status |
|-----------|-------------|-------------|----------|--------|
| M1: Kickoff | [date] | [date] | [±N days] | Complete |
| M2: Tech setup | [date] | [date or —] | [±N or —] | [status] |
| M3: First use | [date] | [date or —] | [±N or —] | [status] |
| M4: First value | [date] | [date or —] | [±N or —] | [status] |
| M5: Handoff ready | [date] | [date or —] | [±N or —] | [status] |

TtV Assessment [review — internal planning target]:
  Segment target:      [X days]
  Projected TtV:       [Y days]
  Variance:            [±Z days — ahead of target / on target / behind target]
  Current pace:        [pace multiplier]x — [interpretation]

[If projected TtV > segment target + 10%:]
⚠ TtV at risk — current pace projects [Y days], [Z days] past the [X-day] target.

Delay breakdown:
  Most significant delay: [milestone with highest positive variance] ([±N days])
  Root cause (if known): [blocker type from config at-risk signals or CSM input]

Recommended acceleration actions:
  1. [Specific action with owner and deadline]
  2. [Specific action]
  3. [If applicable]
```

---

## `--portfolio` output

```
Portfolio TtV Summary [review — internal planning target]
Generated: [today] · [N] accounts included

| Account | Segment | Model | Projected TtV | Target | Variance | Status |
|---------|---------|-------|--------------|--------|----------|--------|
| [name] | Enterprise | white-glove | [X]d | [Y]d | [±Z]d | On target |
| [name] | Mid-Market | guided-self-serve | [X]d | [Y]d | [+Z]d | ⚠ Behind |
| [name] | SMB | guided-self-serve | [X]d | [Y]d | [-Z]d | Ahead |

Portfolio summary:
  Median projected TtV:    [X days]
  Segment target (median): [Y days]
  Accounts ahead of target: [N]
  Accounts on target:       [N]
  Accounts behind target:   [N]

Accounts requiring attention (behind by >15%):
  [Account name] — [N days behind] — [most significant delay milestone]
  [Recommended action]
```

---

## `--patterns` output

Requires minimum 5 accounts with complete milestone data for meaningful analysis.
If fewer accounts are available:
> "[N] accounts have complete data — pattern analysis is most reliable with 5 or
> more. I'll surface what's observable, but treat these findings as directional
> rather than conclusive."

```
TtV Pattern Analysis [review — internal planning target]
Generated: [today] · [N] accounts analyzed

Data period: [earliest contract start] to [latest M4 completion]

1. MILESTONE VELOCITY PATTERNS

Milestone transitions ranked by average delay (highest to lowest):
  M2→M3: avg [X] days over target — [interpretation]
  M1→M2: avg [X] days over target
  M3→M4: avg [X] days over target
  M4→M5: avg [X] days over target

Fastest milestone: [M#] — avg [X] days under target

2. SEGMENT PERFORMANCE

| Segment | Accounts | Median TtV | Target | On-target rate |
|---------|----------|-----------|--------|---------------|
| Enterprise | [N] | [X]d | [Y]d | [N]% |
| Mid-Market | [N] | [X]d | [Y]d | [N]% |
| SMB | [N] | [X]d | [Y]d | [N]% |

3. MODEL PERFORMANCE

| Model | Accounts | Median TtV | Target | On-target rate |
|-------|----------|-----------|--------|---------------|
| white-glove | [N] | [X]d | [Y]d | [N]% |
| guided-self-serve | [N] | [X]d | [Y]d | [N]% |
| implementation-plus-handoff | [N] | [X]d | [Y]d | [N]% |

4. BLOCKER CORRELATION (if blocker log data available)

Most common blocker types in accounts with TtV extension >20%:
  - [blocker type]: [N] occurrences
  - [blocker type]: [N] occurrences

5. PROACTIVE RECOMMENDATIONS

Based on the patterns above:
  1. [Specific proactive action targeting the highest-delay milestone transition]
  2. [Segment or model-specific recommendation]
  3. [Systemic recommendation if a pattern is addressable at the process level]
```

---

## Reviewer note (internal — all modes)

> ⚠️ Reviewer note
> - **Sources:** [PM connector ✓ | CRM ✓ | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** TtV targets ([segment: X days]), milestone framework
>   ([M1 Xd, M2 Xd, M3 Xd, M4 Xd, M5 Xd])
> - **TtV calculation method:** contract start → M4 completion date
> - **Accounts with complete data:** [N] of [N] total
> - **Pace projection confidence:** [High — multiple milestones complete | Moderate —
>   early-stage projection | Low — only M1 complete]
> - **Data gaps:** [accounts missing contract start date or milestone completion dates]
> - **Flagged for your judgment:** [accounts requiring immediate attention | none]

---

## Output

Time-to-Value analysis output — format driven by flag (`--account`, `--portfolio`,
`--patterns`). Account mode: single-account TtV calculation with contributing
factors and acceleration recommendations. Portfolio mode: ranked table. Patterns
mode: cohort analysis with systemic findings. See mode-specific sections for
field-level structure.

## Guardrails

**TtV is always labeled — no exceptions.** Every TtV figure, projection, comparison,
and target carries the tag `[review — internal planning target]`. This tag is not
optional and is not removed for any output mode. If a user requests TtV framing in
a customer communication, redirect to milestone-date language.

**Projected TtV requires at least M1 completion.** A TtV projection based only on
the contract start date is not a projection — it is the target. At least one
milestone must be complete before pace can be calculated. Flag projections based
on zero completed milestones as target-based estimates, not pace-based projections.

**Portfolio comparison is segment-adjusted.** A 45-day TtV for an SMB account is
not comparable to a 45-day TtV for an Enterprise account with a different target.
All portfolio comparisons are against segment-level targets, not absolute numbers.

**Pattern analysis requires caution with small sample sizes.** Fewer than 5 accounts
produce directional signals, not reliable patterns. Always state the sample size and
flag when it is below the threshold for confident conclusions.

**Acceleration recommendations are CSM-owned.** The skill identifies what's causing
the delay and recommends actions. The CSM determines whether those actions are
appropriate given account context. Do not present acceleration recommendations as
instructions — present them as options for CSM judgment.

**Negative variance is not always good news.** An account completing milestones
faster than target should be noted, but also checked: is M4 being marked complete
prematurely? A milestone completed early without confirmed completion criteria is
a data quality issue, not a performance win. Flag early completions for verification.
