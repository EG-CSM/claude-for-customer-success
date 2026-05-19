# rev-ops.csql-tracking

Tracks CS-Qualified Lead (CSQL) progression from identification through closed expansion. Records CSQL source (expansion business case, health score signal, or CSM nomination), pipeline stage, ARR value, and close outcome. Feeds expansion pipeline reporting and closes the loop between csm.expansion-business-case and csm.expansion-onboarding.

## Use it for

- Log a new CSQL with source, ARR estimate, and owning CSM
- Update CSQL stage as it progresses through the expansion pipeline
- {'Report CSQL pipeline health': 'volume, velocity, and conversion rate'}
- Close out a CSQL as won (triggers expansion-onboarding handoff) or lost (triggers RCA)

## Don't use it for

- New logo pipeline tracking (sales domain)
- Renewal forecasting (use renewals.renewal-forecast)
- Full comp or quota modeling (use rev-ops.comp-simulation)

## How to trigger it

Say something like:

- "log a CSQL"
- "track expansion lead"
- "CSQL pipeline"
- "update expansion opportunity"
- "expansion pipeline report"
- "close out CSQL"

## What you get

- CSQL log entry (structured markdown or CRM field update proposal)
- CSQL pipeline health report (volume, velocity, conversion — on report request)
- Expansion-onboarding handoff brief (on --won close)

## Prerequisites

- Domain CLAUDE.md (reads at startup; routes to cold-start-interview if missing)
- Account name or ID
- {'CSQL source': 'expansion-business-case, health-score-signal, or CSM-nomination'}
- Estimated expansion ARR
- Current pipeline stage

## Governance

- {'G6': 'all pipeline data reads surface data-as-of timestamp'}
- {'G9': 'CRM log entries are proposals until user confirms; no autonomous CRM writes'}

## See also

- csm.expansion-business-case
- csm.expansion-onboarding
- rev-ops.forecast-variance-analysis
- renewals.renewal-forecast

---

*Domain: `rev-ops` · Skill ID: `rev-ops.csql-tracking`*
