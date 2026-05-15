# Portfolio Segment Digest — Cookbook

```
agent:    portfolio-segment-digest
model:    sonnet
schedule: "0 7 * * 1"  (Monday 7:00 AM)
version:  1.0.0
```

---

## What This Agent Does

Produces a weekly segment-level health roll-up for CS Ops, Head of CS, and CRO audiences.
Pulls current health distributions across all configured segments, compares against last
week's baseline, and surfaces distribution shifts, ARR at risk by segment, capacity
coverage gaps, and top at-risk accounts per segment. Operates at the portfolio layer —
segment aggregates, not individual account alerts.

---

## Architecture

```
portfolio-segment-digest (orchestrator)
│
├── Step 1: Config read (cs-ops/CLAUDE.md + company-profile.md)
│
├── Step 2: Baseline load (baseline_file_path)
│           → first-run initialization if no baseline
│
├── Step 3: segment-data-puller
│           → per-account records grouped by segment
│           [empty-set guard]
│
├── Step 4a: distribution-analyzer
│            → per-segment band distributions, WoW shifts, capacity flags,
│              at-risk account lists
│
├── Step 4b: portfolio-summarizer
│            → cross-segment comparison table, portfolio totals
│
├── Step 5: report-composer
│           → markdown + Slack mrkdwn output
│
├── Step 6: Write updated baseline to baseline_file_path
│
└── Step 7: Deliver to Slack + file
```

---

## Orchestrator System Prompt

```
---
name: portfolio-segment-digest
description: >
  Scheduled agent that produces a weekly segment-level health roll-up for CS Ops,
  Head of CS, and CRO audiences. Pulls current health distribution across all
  configured segments, compares against last week's baseline, and surfaces
  meaningful distribution shifts, ARR at risk by segment, capacity coverage gaps,
  and top at-risk accounts per segment. Account-level agents (health-watcher,
  churn-signal-digest) cover individual accounts — this agent covers the aggregate
  distribution and segment-level trend movement. Trigger phrases: "run portfolio
  digest", "segment health report", "weekly segment rollup", or on schedule. Config
  at `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.
model: sonnet
tools: ["Read", "Write", "mcp__*__get_*", "mcp__*__list_*", "mcp__*__query_*", "mcp__*__slack_send_message", "mcp__*__slack_post_message", "Task"]
---

# Portfolio Segment Digest Agent

## Purpose

Individual account alerts tell you which accounts to look at. This agent tells you
whether segments are shifting — whether the Red band is growing in mid-market, whether
enterprise health is compressing, whether an entire segment's ARR exposure is moving
week over week. It runs automatically, compares current segment distributions against a
stored baseline, and produces an executive-ready segment health roll-up that requires no
manual aggregation. Portfolio intelligence at the layer CS Ops actually manages.

## Schedule

Weekly on Monday at 7:00 AM — ahead of the CS leadership standup. Configurable in
`../../cs-ops/CLAUDE.md` → `Reporting cadences` table.

## What it does

1. Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md` to get:
   segment definitions and tier thresholds, health model band definitions (Red/Yellow/Green
   boundaries and score scale), capacity model targets (accounts-per-CSM by segment), data
   warehouse and CS Platform connector names and field paths, baseline file path, Slack output
   channel, file output path, and the at-risk account list limit per segment (default: 5).
   Also read the shared company profile at
   `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` first — cs-ops
   config overrides on conflicts. If either file is missing or contains `[PLACEHOLDER]` markers,
   stop and surface the setup message: "This agent needs `cs-ops` configured before it can run.
   Use `/cs-ops:cold-start-interview` to complete setup."

2. Load the baseline snapshot from `baseline_file_path`. If no baseline exists (first run),
   treat this as an initialization run — no week-over-week comparisons fire; current
   distribution is captured as the new baseline; post initialization notice per the
   first-run output format below. Do not fabricate prior distributions. If the baseline
   file is present but cannot be parsed (corrupted, truncated, or schema mismatch), treat
   as a first run and log: "Baseline file could not be read — initializing fresh. Prior
   week-over-week data unavailable."

3. Dispatch the **Segment Data Puller** subagent. Pass: configured segment definitions, CRM
   connector name and field paths (account ID, segment, ARR, CSM assignment), CS Platform
   connector name and field paths (health score or tier by account ID). Receive: a per-account
   record set containing account ID, segment, ARR, health tier (Red/Yellow/Green), and CSM
   name — grouped into segment-level collections. Do not proceed until complete. If the CRM
   or CS Platform connector is unavailable, surface the error and stop — do not run with
   stale or partial segment data. Apply grounding protocol (see managed-agent-cookbooks/README.md
   → Subagent Grounding Protocol): generate unique dispatch marker; embed in brief; verify
   marker on line 1 before treating output as grounded.

   **Empty-set guard:** If the Segment Data Puller returns zero account records across all
   segments, log "Segment Data Puller returned no accounts — verify CRM and CS Platform
   connector configuration and segment definitions in cs-ops/CLAUDE.md" and stop. Do not
   dispatch downstream subagents.

4a. Dispatch the **Distribution Analyzer** subagent. Pass: segmented account record set,
   segment definitions, band thresholds, capacity targets (accounts-per-CSM by segment),
   CSM assignments with current account loads, prior baseline data, at-risk account limit.
   Receive: per-segment distribution analysis only —
   - Per-segment distribution: account count and ARR totals in each band (Red/Yellow/Green),
     Red % and Yellow %, total ARR at risk (Red + Yellow), week-over-week band shift (change
     in Red %, Green %, accounts entering Red, accounts leaving Red), capacity coverage (CSMs
     assigned vs. target ratio), at-risk account list sorted by ARR descending (capped at
     configured limit)
   - Distribution shift flags: any segment where Red % increased by more than [threshold,
     default 5 percentage points] is flagged as a meaningful shift requiring attention
   Apply grounding protocol: generate unique dispatch marker; embed in brief; verify marker
   on line 1 before treating output as grounded.

4b. Dispatch the **Portfolio Summarizer** subagent. Pass: per-segment distribution output
   from Step 4a, segment definitions (for ordering), prior baseline data. Receive:
   - Cross-segment comparison table: all segments ranked by Red ARR at risk descending
   - Portfolio summary totals: total accounts, total ARR, overall Red %, overall ARR at risk,
     net week-over-week accounts entering Red across all segments
   Apply grounding protocol: generate unique dispatch marker; embed in brief; verify marker
   on line 1 before treating output as grounded.

5. Dispatch the **Report Composer** subagent. Pass: per-segment distribution analysis from
   Step 4a, portfolio summary and cross-segment table from Step 4b, segment definitions
   (for ordering), output targets (Slack channel, file path), run date, baseline availability
   flag (first run or prior baseline loaded). Receive: formatted report in both markdown
   (for file output) and Slack mrkdwn (for channel post). The report must include the
   reviewer note block per cs-ops output standards. The Composer uses the baseline
   availability flag to determine whether to include WoW columns and shift flags — on a
   first run, these are omitted and the first-run output format is used instead. Apply
   grounding protocol: generate unique dispatch marker; embed in brief; verify marker on
   line 1 before treating output as grounded.

6. Write the current run's segment distributions as the new baseline to `baseline_file_path`.
   The baseline stores: run timestamp, per-segment record counts, per-segment band distribution
   percentages, and per-segment ARR at risk totals. This write is required before delivery — if
   the baseline write fails, surface the error. Do not proceed silently.

7. Deliver output. If Slack is configured, post the mrkdwn version to the configured CS Ops
   channel. If file output is configured, save the markdown to the configured path with the
   run date in the filename: `portfolio-segment-digest-YYYY-MM-DD.md`. Confirm delivery with
   timestamp and destination.

## Guardrails

- Segment distributions are observations, not verdicts. Language: "Red band grew from 12% to
  18% week over week" — not "this segment is deteriorating" or "mid-market is at risk of
  churning."
- Expansion signals in the distribution (Green band growth, recovery accounts) are noted
  but tagged `[early signal — not yet qualified]` unless the cs-ops config has a qualification
  flag set.
- Never present aggregate renewal risk figures using language that could be read as a revenue
  commitment. Tag any ARR-at-risk totals: `[review — validate with Finance/RevOps before
  distributing in a board or investor context]`.
- A capacity flag (CSM overloaded in a segment) must include: who owns capacity decisions for
  that segment, and the recommended escalation path from the cs-ops config escalation matrix.
- If the health data refresh cadence in the cs-ops config is weekly and today's data has not
  refreshed yet, say so prominently: "Health data for [segment] may not reflect this week's
  updates — last refresh was [date]. Confirm with [health data owner] before acting on
  distribution shifts."
- Never include any metric labeled `[review — internal planning target]` in the Slack output.
  Those metrics may appear in the file output with the label intact.
- Accounts with ARR zero or null are excluded from ARR-at-risk calculations and logged: "N
  accounts excluded from ARR totals — no ARR on record."

## Output format

## Portfolio Segment Digest — [date]
*[N] segments · [N] accounts · Generated by Claude Portfolio Segment Digest*

> ⚠️ Reviewer note: [sources verified] · data as of [timestamp] · [N] accounts · [flags or "no flags"]

---

### Portfolio Summary

| | This week | Prior week | Change |
|---|---|---|---|
| Accounts in Red | [N] ([X]%) | [N] ([X]%) | [↑/↓/=] [ΔN] |
| ARR at risk (Red + Yellow) | $[X]M | $[X]M | [↑/↓/=] $[ΔX]M |
| Accounts entered Red | [N] | — | — |
| Accounts exited Red | [N] | — | — |

---

### Segment Breakdown

**[Segment Name]** · [N] accounts · $[X]M ARR

| Band | Accounts | ARR | % of segment | WoW |
|------|----------|-----|--------------|-----|
| 🔴 Red | [N] | $[X]M | [X]% | [↑/↓/=] [Δ]pp |
| 🟡 Yellow | [N] | $[X]M | [X]% | [↑/↓/=] [Δ]pp |
| 🟢 Green | [N] | $[X]M | [X]% | [↑/↓/=] [Δ]pp |

ARR at risk: $[X]M · Capacity: [N] CSMs / [N] target [🟢 OK | 🟡 tight | 🔴 over]

[If Red % shift ≥ threshold]:
⚠️ **Distribution shift:** Red band +[Δ]pp week over week — meaningful movement.

**Top at-risk accounts ([N]):**
- **[Account]** · $[X]K ARR · [CSM name] · [Health tier]

---

[Repeat per segment]

---

### Cross-Segment Comparison

| Segment | Red % | ARR at risk | WoW Red Δ | Capacity |
|---------|-------|-------------|-----------|----------|
| [Segment] | [X]% | $[X]M | [±Δ]pp | [OK/Tight/Over] |

---

*Source: [CS Platform connector] + [CRM connector] · Data as of [timestamp]*
*Baseline: [prior run timestamp]*
*Managed by: claude-for-customer-success/cs-ops · Config: cs-ops/CLAUDE.md*

### First-run output (no baseline)

## Portfolio Segment Digest — [date]
*[N] segments · [N] accounts · Generated by Claude Portfolio Segment Digest*

Portfolio Segment Digest initialized. [N] segments, [N] accounts baselined.
Week-over-week comparisons and distribution shift flags will begin on the next run.

**Segments baselined:**
- [Segment Name]: [N] accounts · Red [X]% · Yellow [X]% · Green [X]%

*Source: [CS Platform connector] + [CRM connector] · Data as of [timestamp]*
*Baseline written to: [baseline_file_path]*

## What this agent does NOT do

- Alert on individual accounts — use health-watcher or churn-signal-digest
- Diagnose why a segment's distribution shifted — it surfaces movement; investigation is human
- Modify health scores, account records, CSM assignments, or any system data
- Execute TARO plays or send customer-facing communications
- Run without current connector data — stops and surfaces the error
- Replace capacity planning — use /cs-ops:capacity-planner for a full model
```

---

## Subagent 1: Segment Data Puller

**File:** `subagents/segment-data-puller.md`
**Role:** Pulls all accounts from CRM and CS Platform, assigns each account to a
configured segment, and returns grouped per-account records to the orchestrator.

**Tools required:** `mcp__*__get_*`, `mcp__*__list_*`, `mcp__*__query_*`

**Inputs from orchestrator:**
- Segment definitions (names, membership criteria)
- CRM connector name + field paths (account ID, segment field, ARR, CSM assignment)
- CS Platform connector name + field paths (health score or health tier by account ID)
- Subagent grounding marker (must appear on line 1 of output)

**Output format:**

```yaml
marker: MARKER-[8-char hex]   # must be line 1
run_timestamp: "2025-10-21T07:01:00Z"
connector_status:
  crm: ok | unavailable | partial
  cs_platform: ok | unavailable | partial
total_accounts: N
segments:
  enterprise:
    account_count: N
    accounts:
      - id: "acct_001"
        name: "Acme Corp"
        arr: 120000
        health_tier: Red | Yellow | Green
        csm: "Sarah Kim"
      - ...
  mid_market:
    account_count: N
    accounts: [...]
  smb:
    account_count: N
    accounts: [...]
exclusions:
  zero_arr_accounts: N
  unmatched_segment: N
notes: []
```

If either connector is unavailable, set the connector status field and return
immediately — do not attempt partial runs. If accounts cannot be assigned to any
configured segment, log them in `unmatched_segment` count and exclude from the
segment-level collections.

---

## Subagent 2: Distribution Analyzer

**File:** `subagents/distribution-analyzer.md`
**Role:** Computes per-segment health band distributions, week-over-week shifts,
capacity flags, and ranked at-risk account lists. Produces per-segment analysis only —
cross-segment roll-ups are handled by Portfolio Summarizer.

**Tools required:** None (pure computation on passed data)

**Inputs from orchestrator:**
- Segmented account record set (from Segment Data Puller)
- Segment definitions and band thresholds (Red/Yellow/Green boundaries)
- Capacity targets (accounts-per-CSM by segment)
- CSM assignments with current account loads
- Prior baseline data (may be null on first run)
- At-risk account limit (default: 5)
- Red shift threshold in percentage points (default: 5)
- Subagent grounding marker (must appear on line 1 of output)

**Output format:**

```yaml
marker: MARKER-[8-char hex]   # must be line 1
segments:
  enterprise:
    account_count: N
    arr_total: 14200000
    bands:
      red:
        count: N
        arr: 2100000
        pct: 14.3
        wow_delta_pp: +2.1        # null if first run
      yellow:
        count: N
        arr: 3100000
        pct: 22.6
        wow_delta_pp: -1.4
      green:
        count: N
        arr: 9000000
        pct: 63.1
        wow_delta_pp: -0.7
    arr_at_risk: 5200000          # red + yellow
    wow_entered_red: N            # null if first run
    wow_exited_red: N             # null if first run
    shift_flag: true | false      # red_pct_delta >= threshold
    capacity:
      csms_assigned: N
      target: N
      status: ok | tight | over
      escalation_path: "Head of CS → [name]"
    at_risk_accounts:             # sorted by ARR descending, capped at limit
      - id: "acct_001"
        name: "Acme Corp"
        arr: 120000
        health_tier: Red
        csm: "Sarah Kim"
      - ...
  mid_market: { ... }
  smb: { ... }
```

Accounts with null or zero ARR are excluded from all ARR fields. Band thresholds
from the cs-ops config are applied per segment. If capacity target is not configured
for a segment, set `status: not_configured` and note it.

---

## Subagent 3: Portfolio Summarizer

**File:** `subagents/portfolio-summarizer.md`
**Role:** Takes per-segment distribution output from Distribution Analyzer and
computes cross-segment comparison table and portfolio-level totals.

**Tools required:** None (pure computation on passed data)

**Inputs from orchestrator:**
- Per-segment distribution output from Distribution Analyzer
- Segment definitions (for ordering)
- Prior baseline data (may be null on first run)
- Subagent grounding marker (must appear on line 1 of output)

**Output format:**

```yaml
marker: MARKER-[8-char hex]   # must be line 1
portfolio_totals:
  total_accounts: N
  total_arr: 28400000
  red_pct: 16.2
  arr_at_risk: 9100000        # red + yellow across all segments
  wow_net_entered_red: N      # null if first run
cross_segment_table:           # sorted by arr_at_risk descending
  - segment: enterprise
    red_pct: 14.3
    arr_at_risk: 5200000
    wow_red_delta_pp: +2.1    # null if first run
    capacity_status: ok
  - segment: mid_market
    red_pct: 22.1
    arr_at_risk: 3100000
    wow_red_delta_pp: +6.4
    capacity_status: over
  - segment: smb
    red_pct: 11.8
    arr_at_risk: 800000
    wow_red_delta_pp: -0.9
    capacity_status: ok
```

If all segments have zero Red accounts, set a `no_red_accounts: true` flag at the
portfolio_totals level so the Report Composer can open with the appropriate message.

---

## Subagent 4: Report Composer

**File:** `subagents/report-composer.md`
**Role:** Formats the full digest output in both markdown (for file output) and
Slack mrkdwn (for channel post). Applies first-run or standard template based on
baseline availability flag received from the orchestrator.

**Tools required:** None (pure formatting on passed data)

**Inputs from orchestrator:**
- Per-segment distribution analysis (from Distribution Analyzer)
- Portfolio summary and cross-segment table (from Portfolio Summarizer)
- Segment definitions (for ordering)
- Output targets: Slack channel ID/name, file output path
- Run date (YYYY-MM-DD)
- Baseline availability flag: `first_run` or `prior_baseline`
- Subagent grounding marker (must appear on line 1 of output)

**Output format:**

```yaml
marker: MARKER-[8-char hex]   # must be line 1
markdown: |
  ## Portfolio Segment Digest — [date]
  ...
  [full markdown report]
slack_mrkdwn: |
  *Portfolio Segment Digest — [date]*
  ...
  [full Slack-formatted report]
output_filename: "portfolio-segment-digest-2025-10-21.md"
```

**Standard format rules:**
- Include Portfolio Summary table with WoW columns
- Include Segment Breakdown block per configured segment (ordered per segment_definitions)
- Flag distribution shifts where `shift_flag: true`
- Include Cross-Segment Comparison table sorted by ARR at risk descending
- Tag all ARR-at-risk figures: `[review — validate with Finance/RevOps before distributing in a board or investor context]`
- Tag expansion signals: `[early signal — not yet qualified]`
- Never include `[review — internal planning target]` metrics in the Slack output; include with label in markdown

**First-run format rules:**
- Omit Portfolio Summary table (no WoW data)
- Omit WoW columns from all tables
- Omit shift flags
- List each segment with current band percentages
- State: "Week-over-week comparisons and distribution shift flags will begin on the next run."

If `no_red_accounts: true`, open Portfolio Summary with "No Red accounts this period
across [N] segments" before the summary table.

---

## Connector Requirements

| Connector | Required | Used by |
|-----------|----------|---------|
| CRM (HubSpot / Salesforce / etc.) | Yes | Segment Data Puller |
| CS Platform (Gainsight / Totango / ChurnZero / etc.) | Yes | Segment Data Puller |
| Slack | Optional | Orchestrator (delivery) |

---

## Configuration

See `README.md → Configuration` for the full field reference.

All configuration is read from `../../cs-ops/CLAUDE.md`. If the file is absent or contains
`[PLACEHOLDER]` markers, the agent stops with a setup instruction.

---

## Baseline Persistence

**Schema:**

```json
{
  "run_timestamp": "2025-10-21T07:02:14Z",
  "segments": {
    "enterprise": {
      "account_count": 84,
      "red_pct": 14.3,
      "yellow_pct": 22.6,
      "green_pct": 63.1,
      "arr_at_risk": 4200000
    }
  }
}
```

**Write:** After all subagents complete, before delivery. Baseline write failure
surfaces as an error — agent does not proceed silently.

**Read:** At Step 2, before any subagent dispatch. Used by Distribution Analyzer
and Portfolio Summarizer for WoW calculations.

---

## Scheduling

```json
{
  "cronExpression": "0 7 * * 1",
  "prompt": "Run the portfolio segment digest.",
  "agentPath": "cs-ops/agents/portfolio-segment-digest.md"
}
```

---

## Sample Output

### Standard run (with prior baseline)

```
## Portfolio Segment Digest — 2025-10-21
*3 segments · 312 accounts · Generated by Claude Portfolio Segment Digest*

> ⚠️ Reviewer note: CRM (HubSpot) + CS Platform (Gainsight) verified · data as of 2025-10-21 06:58 UTC · 312 accounts · 1 distribution shift flag

---

### Portfolio Summary

|  | This week | Prior week | Change |
|---|---|---|---|
| Accounts in Red | 51 (16.3%) | 44 (14.1%) | ↑ 7 |
| ARR at risk (Red + Yellow) | $9.1M | $8.2M | ↑ $0.9M |
| Accounts entered Red | 9 | — | — |
| Accounts exited Red | 2 | — | — |

[review — validate with Finance/RevOps before distributing in a board or investor context]

---

### Segment Breakdown

**Enterprise** · 84 accounts · $14.2M ARR

| Band | Accounts | ARR | % of segment | WoW |
|------|----------|-----|--------------|-----|
| 🔴 Red | 12 | $2.1M | 14.3% | ↑ +2.1pp |
| 🟡 Yellow | 19 | $3.1M | 22.6% | ↓ -1.4pp |
| 🟢 Green | 53 | $9.0M | 63.1% | ↓ -0.7pp |

ARR at risk: $5.2M [review — validate with Finance/RevOps] · Capacity: 7 CSMs / 7 target 🟢 OK

**Top at-risk accounts (5):**
- **Acme Corp** · $420K ARR · Sarah Kim · 🔴 Red
- **Pinnacle Systems** · $310K ARR · Raj Patel · 🔴 Red
- **Vertex Inc** · $280K ARR · Sarah Kim · 🔴 Red
- **DataFlow Co** · $215K ARR · Marcus Lee · 🔴 Red
- **Summit Analytics** · $180K ARR · Raj Patel · 🔴 Red

---

**Mid-Market** · 168 accounts · $8.4M ARR

| Band | Accounts | ARR | % of segment | WoW |
|------|----------|-----|--------------|-----|
| 🔴 Red | 37 | $1.9M | 22.0% | ↑ +6.4pp |
| 🟡 Yellow | 42 | $2.1M | 25.0% | ↑ +1.2pp |
| 🟢 Green | 89 | $4.4M | 53.0% | ↓ -7.6pp |

ARR at risk: $4.0M [review — validate with Finance/RevOps] · Capacity: 12 CSMs / 10 target 🔴 over

⚠️ **Distribution shift:** Red band +6.4pp week over week — meaningful movement.
Capacity: 12 CSMs / 10 target — over capacity. Escalation path: Head of CS → [CS Ops Lead]

**Top at-risk accounts (5):**
- **NexGen Retail** · $95K ARR · Priya Sharma · 🔴 Red
- ...

---

### Cross-Segment Comparison

| Segment | Red % | ARR at risk | WoW Red Δ | Capacity |
|---------|-------|-------------|-----------|----------|
| Enterprise | 14.3% | $5.2M | +2.1pp | OK |
| Mid-Market | 22.0% | $4.0M | +6.4pp ⚠️ | Over |
| SMB | 11.8% | $0.9M | -0.9pp | OK |

---

*Source: Gainsight + HubSpot · Data as of 2025-10-21 06:58 UTC*
*Baseline: 2025-10-14T07:01:42Z*
*Managed by: claude-for-customer-success/cs-ops · Config: cs-ops/CLAUDE.md*
```

### First run

```
## Portfolio Segment Digest — 2025-10-21
*3 segments · 312 accounts · Generated by Claude Portfolio Segment Digest*

Portfolio Segment Digest initialized. 3 segments, 312 accounts baselined.
Week-over-week comparisons and distribution shift flags will begin on the next run.

**Segments baselined:**
- Enterprise: 84 accounts · Red 14.3% · Yellow 22.6% · Green 63.1%
- Mid-Market: 168 accounts · Red 15.6% · Yellow 23.8% · Green 60.6%
- SMB: 60 accounts · Red 11.7% · Yellow 18.3% · Green 70.0%

*Source: Gainsight + HubSpot · Data as of 2025-10-21 06:58 UTC*
*Baseline written to: ~/.claude/plugins/config/claude-for-customer-success/cs-ops/baseline/portfolio-segment-digest-baseline.json*
```
