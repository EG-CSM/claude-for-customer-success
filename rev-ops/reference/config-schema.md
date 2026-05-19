# RevOps Plugin Config Schema
## claude-for-customer-success / rev-ops — v1.0.0

Defines every field in `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`.
Skills read configuration against this schema. Cold-start interview writes against it.

Fields marked **required** must be present before analytical skills run.
Fields marked **optional** have documented defaults; skills degrade gracefully when absent.

---

## Fields Inherited from company-profile.md (read-only — do not re-ask)

These are written by the first C4CS cold-start. Rev-ops reads them directly.

| Field | Type | Example |
|-------|------|---------|
| `company_name` | string | "Acme Corp" |
| `primary_segment` | enum: SMB \| Mid-Market \| Enterprise \| Strategic | "Enterprise" |
| `current_arr` | number (USD) | 12000000 |
| `fiscal_year_start_month` | integer 1–12 | 2 (February) |
| `crm_system` | enum: HubSpot \| Salesforce \| Other | "HubSpot" |
| `cs_platform` | enum: Gainsight \| ChurnZero \| Totango \| Vitally \| Planhat \| None | "Gainsight" |

---

## Rev-Ops Specific Fields

### Planning Parameters

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `target_growth_pct` | required | float 0–2.0 | — | YoY ARR growth target. E.g., 0.45 = 45% |
| `nrr_current` | required | float 0.5–2.0 | — | Current Net Revenue Retention. E.g., 1.10 = 110% |
| `sales_motion` | required | enum | — | `Outbound-Heavy \| Mixed \| Inbound-Dominant \| PLG` |
| `touch_model` | required | enum | — | `High-Touch \| Tech-Touch \| Pooled` |
| `ae_quota` | required | number (USD) | — | Annual new ARR quota per fully-ramped AE |
| `ae_attainment_planning_rate` | optional | float | 0.75 | Planning attainment rate. KBCM actuals median 55–65% |
| `arr_per_csm` | required | number (USD) | — | Target ARR per CSM for current segment and touch model |
| `avg_deal_acv` | optional | number (USD) | — | Average new deal ACV. Used for account-count capacity modeling |
| `avg_sales_cycle_days` | optional | integer | — | Average days to close by segment. Used in Tier 1 churn detection |
| `uog_baseline_path` | optional | string (file path) | — | Path to saved unit-of-growth-calculator output for current plan year |

### Headcount

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `current_ae_count` | required | integer | — | Current fully-ramped AE headcount |
| `current_csm_count` | required | integer | — | Current CSM headcount |
| `current_sdr_count` | optional | integer | — | Current SDR headcount |
| `open_ae_requisitions` | optional | integer | 0 | AE reqs open and in process |
| `open_csm_requisitions` | optional | integer | 0 | CSM reqs open and in process |
| `csm_avg_ramp_days` | optional | integer | 90 | Average days to full CSM productivity |

### Discount and Deal Desk

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `discount_standard_threshold_pct` | required | float | — | Max discount AE manager can approve. E.g., 0.15 = 15% |
| `discount_elevated_threshold_pct` | required | float | — | Max discount RevOps lead can approve |
| `discount_executive_threshold_pct` | optional | float | — | Above this: CRO + Finance dual approval |
| `payment_terms_standard_days` | optional | integer | 30 | Standard payment terms in days (net-N) |
| `renewal_conversation_window_days` | optional | integer | 90 | Days before renewal date to initiate renewal conversation |

### Lead Definitions

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `mql_definition` | required | string | — | What constitutes a Marketing Qualified Lead |
| `sal_definition` | required | string | — | What constitutes a Sales Accepted Lead |
| `sql_definition` | required | string | — | What constitutes a Sales Qualified Lead |

### OCV Catalog

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `ocv_catalog_path` | optional | string (file path) | — | Path to ratified Outcome & Value Registry file |
| `ocv_catalog_version` | optional | string | — | Version of catalog currently in use. E.g., "1.2.0" |
| `ocv_catalog_last_ratified` | optional | date | — | Date of last cross-functional ratification |

### Churn Detection

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `tier1_mode` | optional | enum | `rule` | `rule \| cohort` — rule mode is default until 6+ months of churn cohort data available |
| `tier1_single_thread_flag` | optional | boolean | true | Flag single-threaded deals at close as Tier 1 risk |
| `tier1_long_cycle_multiplier` | optional | float | 2.0 | Flag deals where sales cycle > segment avg × this multiplier |
| `churn_cohort_data_path` | optional | string (file path) | — | Path to closed/won-to-churn cohort dataset. Required for cohort mode |

### Connectors

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `hubspot_connected` | optional | boolean | false | HubSpot MCP connector confirmed live |
| `google_drive_connected` | optional | boolean | false | Google Drive connector confirmed live |
| `slack_connected` | optional | boolean | false | Slack connector confirmed live |
| `linear_connected` | optional | boolean | false | Linear connector confirmed live |
| `zapier_connected` | optional | boolean | false | Zapier MCP connector confirmed live (CS platform webhooks) |
| `cs_platform_connected` | optional | boolean | false | CS platform data available (via CS platform connector or Zapier) |

---

## Fallback Behavior by Field Group

When required fields are absent, skills behave as follows:

| Missing field group | Fallback behavior |
|---------------------|------------------|
| Planning parameters | Skills run with user-provided inputs for the session only; prompt to complete cold-start |
| Headcount | Capacity analysis runs in structural-only mode; no gap vs. current headcount |
| Discount thresholds | Deal desk skills flag all discounts for human review; no tiered routing |
| Lead definitions | Attribution and handoff skills skip definition-drift detection |
| OCV catalog | Outcome tracking runs on CRM signals only; confidence downgraded to Low |
| Churn config | Tier 1 uses hardcoded defaults: 15% discount, 2x cycle multiplier |

---

## Company Profile Template

Cold-start writes this file to:
`~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`

```markdown
# Rev-Ops Company Profile
## claude-for-customer-success / rev-ops
## Written by: cold-start-interview v1.0.0
## Date: [DATE]

### Planning Parameters
target_growth_pct: [VALUE]
nrr_current: [VALUE]
sales_motion: [VALUE]
touch_model: [VALUE]
ae_quota: [VALUE]
ae_attainment_planning_rate: 0.75
arr_per_csm: [VALUE]
avg_deal_acv: [VALUE or omit]
avg_sales_cycle_days: [VALUE or omit]
uog_baseline_path: [PATH or omit]

### Headcount
current_ae_count: [VALUE]
current_csm_count: [VALUE]
current_sdr_count: [VALUE or omit]
open_ae_requisitions: [VALUE or 0]
open_csm_requisitions: [VALUE or 0]
csm_avg_ramp_days: 90

### Discount and Deal Desk
discount_standard_threshold_pct: [VALUE]
discount_elevated_threshold_pct: [VALUE]
discount_executive_threshold_pct: [VALUE or omit]
payment_terms_standard_days: 30
renewal_conversation_window_days: 90

### Lead Definitions
mql_definition: "[VALUE]"
sal_definition: "[VALUE]"
sql_definition: "[VALUE]"

### OCV Catalog
ocv_catalog_path: [PATH or omit]
ocv_catalog_version: [VERSION or omit]
ocv_catalog_last_ratified: [DATE or omit]

### Churn Detection
tier1_mode: rule
tier1_single_thread_flag: true
tier1_long_cycle_multiplier: 2.0
churn_cohort_data_path: [PATH or omit]

### Connectors
hubspot_connected: [true/false]
google_drive_connected: [true/false]
slack_connected: [true/false]
linear_connected: [true/false]
zapier_connected: [true/false]
cs_platform_connected: [true/false]
```
