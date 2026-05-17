---
name: gtm-unified-metrics-pulse
version: 1.0.0
description: "Weekly cross-functional metrics report covering five sections: pipeline/forecast/closed-won (all teams), handoff quality (RevOps/CS ops), CS capacity status (leadership), early churn flags with account names (#cs-leadership only), outcome realization summary (aggregate to all, account-level to #cs-leadership). All Slack posts require Write-tier confirmation. Triggers: 'weekly pulse', 'GTM metrics', 'alignment pulse', 'cross-functional metrics', 'run the weekly pulse'."
---

# GTM Unified Metrics Pulse

Five-section weekly signal for the full revenue lifecycle.
The one report that replaces "which number is right?" in the leadership meeting.

**Reference:** Output destination labels → `reference/revops-domain-model.md §11`
**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `slack_connected`, `linear_connected`, `cs_platform_connected`

---

## Reasoning Protocol

1. Confirm activation — user requesting weekly pulse or GTM alignment report
2. Check all connectors — pulse quality degrades section-by-section if unavailable
3. Build each section independently; label connector status per section
4. Apply G1 — forecast language qualification in Section 1
5. Apply G7 — Section 4 churn flags require escalation path per account
6. **Confirm Slack destination before posting** — Write-tier; RevOps lead approval required
7. Route Sections 4–5 account-level data to #cs-leadership only

---

## Five Sections

### Section 1 — Pipeline → Forecast → Closed/Won
```
Source: HubSpot [CRM ✓ live — as of YYYY-MM-DD]
  Pipeline total: $XXXk  (WoW: +$XXXk ↑ / −$XXXk ↓)
  Forecast (P50): $XXXk  (WoW: [delta])
  Closed/won MTD: $XXXk  (vs. $XXXk plan — XX% attainment)

Why it changed: [One line if WoW delta >threshold]
[G1: Forecast is a model. Not a revenue commitment.]
```

### Section 2 — Handoff Quality
```
Source: HubSpot + OCV catalog [CRM ✓ live]
  Deals closed this week: [N]
  Avg handoff score: [N]/100
  Below-threshold deals: [N] — Linear issues created ✓
[No account names — aggregate only]
```

### Section 3 — CS Capacity Signal
```
Source: Practice profile + SA1 forecast [Practice profile]
  CS headroom: XX%  [HEALTHY / AT-RISK / CRITICAL]
  At P50 forecast: CSMs needed [N], in seat [N], gap [+N/-N]
  Hiring lead time flag: [if applicable]
[G2: Structural signal. Hiring requires budget approval.]
```

### Section 4 — Early Churn Flags `[#cs-leadership ONLY]`
```
Source: CS platform + CRM [CS Platform ✓ live / Stale N days]
  Accounts crossing threshold this week: [N]
  [Account name]  Tier [N]  Signal: [specific]  ACV: $XXXk
  [Account name]  Tier [N]  Signal: [specific]  ACV: $XXXk
[G7: Each flag includes escalation path]
[DESTINATION: #cs-leadership only — do not post to #revops-alignment]
```

### Section 5 — Outcome Realization
```
Source: OCV catalog + CS platform [CS Platform ✓ live]
  Portfolio L2+ attainment: XX%  (WoW: +Xpp ↑ / −Xpp ↓)
  L0 accounts past 90-day checkpoint: [N]  (threshold: [N])
  [If cohort diverging: flag — aggregate description, no account names]
[Account-level detail → #cs-leadership only]
```

---

## Slack Delivery (Write-tier — requires confirmation)

```
Confirm before posting:
  Sections 1–3: → #revops-alignment [all C4CS users]
  Section 4 (account names): → #cs-leadership [CS leadership only]
  Section 5 (aggregate): → #revops-alignment
  Section 5 (account detail): → #cs-leadership

Preview shown to RevOps lead before any Slack post.
Once weekly schedule confirmed, subsequent posts auto-proceed UNLESS:
  - Section 4 contains a Tier 3 flag for an enterprise account (individual review)
```

---

## Fallback (connector unavailable)

```
Section 1: No HubSpot → "Pipeline data unavailable [HubSpot: Unavailable]"
Section 3: No CS platform → "CS capacity model running on CRM signals only [Confidence: Moderate]"
Section 4: No CS platform → "Churn signal scan unavailable [CS Platform: Unavailable]"
Section 5: No OCV catalog → "Outcome tracking unavailable — OCV catalog not configured"
```

Always declare what's missing. Never produce a section from unavailable data
without labeling it.

---

## Guardrails

- G1: Section 1 forecast language qualification
- G2: Section 3 structural input qualifier
- G7: Section 4 every flag has escalation path and owner
- G6: Data-as-of on every section header
- Write-tier: Preview required before Slack posts
