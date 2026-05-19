---
name: deal-health-scoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Scores each open opportunity on five dimensions (activity recency, stakeholder coverage, stage-age ratio, competitive signal, rep forecast accuracy history). Composite 0–100 score. Deals below 50 flagged for next-best-action. Triggers: 'deal health', 'health score', 'which deals are at risk', 'pipeline health', 'risky deals this quarter'."
---

[PROPOSED]

# Deal Health Scoring

Five-dimension health score per open opportunity. Below 50 triggers
automatic handoff to `next-best-action-recommendation`.

**Reference:** Health score dimensions and confidence bands →
`../../../shared/revops-domain-model.md §2`
**Config reads:** `avg_sales_cycle_days`, `primary_segment`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `avg_sales_cycle_days`, `primary_segment`

---

## Use when
- User needs a structured health score for one or more active pipeline deals — applies to both Sales new-logo pipeline and CS expansion pipeline
- Deal review requires objective signal aggregation (engagement, velocity, stakeholder thread, competitive)
- Sales manager or CS leader needs to identify at-risk deals before a forecast or pipeline review call

## Do NOT use for
- Deal classification by type or segment (use deal-classification)
- Pipeline coverage ratio analysis (use pipeline-coverage-analysis)
- Closed deal outcome tracing (use deal-to-outcome-tracing)

## Typical activation
"Score this deal", "deal health for [account]", "which deals are at risk", "health check on my pipeline", "flag unhealthy expansion deals", "CS pipeline health"

## Application context
This skill applies to **both pipelines** — Sales new-logo deals and CS-originated expansion deals.
The scoring model is identical; interpretation differs:
- **New-logo deals:** stakeholder roles are AE-defined (EB, Champion, Technical Contact)
- **CS expansion deals:** stakeholder roles are CSM-defined — CS sponsor, economic buyer at the account, and any internal CS champion
At-risk expansion deals below 50 route to `next-best-action-recommendation` for CS-specific intervention options.

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of deal health request is this?
   - Single deal score (one opportunity, full five-dimension breakdown)
   - Portfolio scan (rep, segment, or all open pipeline — composite + distribution)
   - At-risk identification (deals below threshold — flag + escalation path)
   - CS expansion pipeline health (CSM-owned deals — same model, CS stakeholder roles)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user wants deal health view or at-risk identification
   2. Check HubSpot connector — activity history required; declare fallback if absent
   3. Apply G5 — health score is analytical input; rep and manager own the response
   4. Apply G6 — surface data-as-of on all activity reads
   5. For any score triggering a risk flag, confirm escalation path exists (G7)
   6. Confirm output destination and scope (single deal, rep, segment, all pipeline)

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Is activity data fresh enough to score? Stale HubSpot activity produces misleading
     health signals — declare data age before presenting scores.
   - Are stakeholder roles correctly mapped to pipeline type? CS expansion deals use
     CS-defined roles (CS sponsor, economic buyer, CS champion) — not Sales AE roles.
   - Is the G7 escalation path named for every at-risk deal? "Flag to manager" without
     naming the manager is not an actionable escalation path.
   - Is a portfolio scan scoped before pulling data? Full pipeline scans on large CRMs
     may return partial data — declare scope and any data limits upfront.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting health score as a directive or override (G5 violation — analytical input only)
   - Surfacing scores without data-as-of timestamp (G6 violation)
   - Flagging at-risk deals without an escalation path (G7 violation)
   - Applying Sales stakeholder role definitions to CS expansion deals — different roles,
     same scoring model

**After execution**, verify:
- G5 qualifier present on all outputs: health scores are analytical inputs
- G6 data-as-of label applied to all HubSpot activity reads
- G7 escalation path named for every at-risk deal (score < 50)
- Confidence: High when HubSpot is connected and activity data is current; Moderate when
  data is stale or connector is unavailable

---

## Scoring Model

| Dimension | Weight | Commit signal (full points) | Degraded |
|-----------|--------|-----------------------------|---------|
| Activity recency | 25% | Contact ≤7 days | −5pts per 7 days beyond |
| Stakeholder coverage | 25% | EB + Champion + TC engaged | −8pts per missing role |
| Stage-age ratio | 20% | At/ahead of historical avg | −4pts per 25% beyond avg |
| Competitive signal | 15% | No competitor / counter-play logged | −8pts if competitor active and no response |
| Rep forecast accuracy | 15% | Trailing commit accuracy ≥70% | Scaled linearly to 0 at <30% |

---

## Output

```
DEAL HEALTH SCORES — [Scope]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Deal             ACV      Score   Signal    Top risk factor
[Account A]      $XXXk    82      Healthy   —
[Account B]      $XXXk    64      Watch     Stakeholder: no EB contact in 14d
[Account C]      $XXXk    41      AT-RISK   Stage stalled; competitive active
[Account D]      $XXXk    28      AT-RISK   All three dimensions degraded

At-risk (< 50): [N] deals, $XXXk total ACV
→ Run /rev-ops:next-best-action-recommendation for intervention options

Portfolio health distribution:
  Healthy (≥75):   [N] deals  $XXXk
  Watch (50–74):   [N] deals  $XXXk
  At-risk (<50):   [N] deals  $XXXk

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G5: Health scores are analytical inputs. Rep and manager own the response.]
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal and pipeline data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G5: Health score is not a directive — always include the G5 qualifier
- G6: Activity data-as-of timestamp required
- G7: At-risk flags include escalation path: "Flag to [rep's manager] for review"
