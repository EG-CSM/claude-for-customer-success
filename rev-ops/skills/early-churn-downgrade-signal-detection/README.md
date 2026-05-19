# rev-ops.early-churn-downgrade-signal-detection

Detects early churn and downgrade signals using a 3-tier model: Tier 1 at-close (rule-mode or cohort-mode; cohort requires 6+ months data), Tier 2 30-90d behavioral, Tier 3 90-120d pre-renewal. Produces risk flags with tier classification and recommended intervention. Output is analytical input (G5); escalation path required on all flags (G7).

## Use it for

- Run Tier 1 rule-mode or cohort-mode detection at deal close
- Surface Tier 2 behavioral signals at 30-90d post-close
- Identify Tier 3 pre-renewal risk signals at 90-120d
- Produce risk flag report with tier classification
- Route flags to csm:risk-flag cross-plugin handoff

## Don't use it for

- Churn intervention execution (route to CSM skill)
- Renewal pipeline management (use renewals domain)
- CRM edits (G9)

## How to trigger it

Say something like:

- "churn signals"
- "downgrade risk"
- "early churn detection"
- "at-risk accounts"
- "Tier 1 churn check"

## What you get

- Risk flag report with tier classification and intervention recommendation (Markdown)

## Prerequisites

- Account activity and health data from CS platform
- Cohort baseline (6+ months of data for cohort-mode)
- Renewal date for Tier 3 detection window

## Governance

- {'G5': 'output is analytical input, not performance ruling'}
- {'G6': 'data-as-of timestamp on all reads'}
- {'G7': 'escalation path required on all risk flags'}
- Cohort-mode requires 6+ months of data; fall back to rule-mode if insufficient

## See also

- csm.risk-flag
- renewals.risk-assessment
- rev-ops.deal-desk-workflow-management

---

*Domain: `rev-ops` · Skill ID: `rev-ops.early-churn-downgrade-signal-detection`*
