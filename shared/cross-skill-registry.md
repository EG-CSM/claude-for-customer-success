# Cross-Skill Registry — claude-for-customer-success

Canonical reference for all skills across all plugins. Use this registry to determine
which skill and command to invoke for a given task. Do not hardcode skill command
strings in individual SKILL.md files — reference this document instead.

Last updated: 2026-05-18

---

## How to Read This Registry

**Command format:** `/plugin:skill-name [arguments]`

**Modes** map to the `argument-hint` flags defined in each skill's frontmatter.
All flag combinations are defined in the individual skill's SKILL.md.

**Typical trigger condition** describes when a CSM or ops user would reach for this
skill. It is not an exhaustive trigger list — see individual SKILL.md for full
`Use when` / `Do NOT use for` blocks.

---

## CSM Plugin (`/csm:*`)

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| expansion-business-case | `/csm:expansion-business-case` | `mode=csql` | Generating a CSQL expansion business case package for a specific account; producing the CSQL handoff doc for Rev-Ops |
| expansion-onboarding | `/csm:expansion-onboarding` | `operation=create` · `operation=update` · `operation=close` | Creating an expansion onboarding plan after a CSQL is won; updating milestone progress; confirming adoption and closing the plan |
| account-research | `/csm:account-research` | `--brief` · `--deep` · `--stakeholders` | Need a fast account profile before a call or QBR; want stakeholder org chart pulled from CRM |
| call-prep | `/csm:call-prep` | `kickoff` · `qbr` · `health` · `renewal` · `check-in` · `custom` | Preparing for any scheduled customer call; need agenda, context, and talking points by call type |
| cold-start-interview | `/csm:cold-start-interview` | `--redo` · `--check-integrations` | First-run plugin setup; rerunning config after integrations change |
| customize | `/csm:customize` | `--full` · `--section <name>` · `--reset` | Editing CSM plugin configuration (thresholds, escalation matrix, health weights) |
| escalation-memo | `/csm:escalation-memo` | `--open` · `--update` · `--close` · `--type technical\|complaint\|executive\|internal` | Drafting or updating a formal escalation record; closing a resolved escalation |
| health-score-review | `/csm:health-score-review` | `--triage` · `--deep` · `--portfolio` | Running a single-account deep dive or portfolio triage; weekly health check |
| qbr-builder | `/csm:qbr-builder` | `--draft` · `--review` · `--exec-brief` | Building QBR deck content; generating executive summary variant |
| renewal-readiness | `/csm:renewal-readiness` | `--brief` · `--timeline` · `--customer-summary` | Pre-renewal health + readiness assessment; building renewal timeline |
| risk-flag | `/csm:risk-flag` | `--brief` · `--escalation-memo` | Flagging an at-risk account; generating escalation memo from risk signal |
| stakeholder-map | `/csm:stakeholder-map` | `--map` · `--gap-analysis` · `--sponsor-risk` | Mapping account stakeholders; identifying executive sponsor gaps |
| success-plan-builder | `/csm:success-plan-builder` | `--new` · `--reset` · `--review` | Creating or reviewing a customer success plan; resetting stale plan |
| taro-play-runner | `/csm:taro-play-runner` | `--situation <description>` · `--play <play-name>` | Running a TARO play for a specific account situation; selecting from play library |
| value-statement | `/csm:value-statement` | `--internal` · `--customer` · `--exec-brief` · `--ae-handoff` | Generating value narrative for renewal, EBR, or AE handoff |

---

## Renewals Plugin (`/renewals:*`)

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| churn-analysis | `/renewals:churn-analysis` | `--deep` · `--quick` · `--portfolio-scan` | Diagnosing churn drivers for a specific account or scanning portfolio for churn patterns |
| cold-start-interview | `/renewals:cold-start-interview` | `--full` · `--quick` · `--redo` · `--check-integrations` · `--redo-company-profile` · `--section <name>` | First-run setup; updating specific config sections after org or process changes |
| contract-review | `/renewals:contract-review` | `--extract` · `--flag` · `--summary` | Reviewing contract terms before renewal; flagging non-standard clauses |
| customize | `/renewals:customize` | `--section <name>` · `--show` · `--edit` · `--validate` | Viewing or updating Renewals plugin configuration; validating config completeness |
| executive-summary | `/renewals:executive-summary` | `--brief` · `--full` · `--board` | Generating executive renewal narrative; preparing board-level renewal summary |
| expansion-signal | `/renewals:expansion-signal` | `--deep` · `--quick` · `--catalog` | Identifying expansion signals in an account; scanning catalog for upsell opportunities |
| negotiation-prep | `/renewals:negotiation-prep` | `--brief` · `--full` · `--export` | Preparing negotiation strategy and talking points before renewal conversation |
| price-increase-prep | `/renewals:price-increase-prep` | `--plan` · `--draft` · `--objections` · `--cohort` | Planning a price increase communication; preparing objection-handling guide |
| renewal-forecast | `/renewals:renewal-forecast` | `--full` · `--cohort 90\|60\|30` · `--segment <name>` · `--account <name>` | Generating pipeline-weighted renewal forecast; 90/60/30-day cohort views; segment breakdown |
| risk-assessment | `/renewals:risk-assessment` | `--deep` · `--quick` · `--triage` | Assessing renewal risk for a specific account; portfolio risk triage |

---

## Onboarding Plugin (`/onboarding:*`)

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| blocker-review | `/onboarding:blocker-review` | `--diagnose` · `--escalate` · `--log` | Diagnosing a stalled onboarding; escalating a technical or stakeholder blocker |
| cold-start-interview | `/onboarding:cold-start-interview` | `--full` · `--quick` · `--redo` · `--check-integrations` · `--redo-company-profile` · `--section <name>` | First-run Onboarding plugin setup; refreshing config after integration changes |
| customize | `/onboarding:customize` | `--view` · `--update <section>` · `--reset <section>` · `--validate` | Viewing or editing Onboarding plugin config (milestone targets, TtV thresholds) |
| handoff-doc | `/onboarding:handoff-doc` | `--draft` · `--readiness` · `--summary` | Generating onboarding-to-CSM handoff document; readiness gate assessment |
| kickoff-prep | `/onboarding:kickoff-prep` | `--prep` · `--agenda` · `--checklist` | Preparing for customer kickoff call; generating agenda and pre-kickoff checklist |
| milestone-tracker | `/onboarding:milestone-tracker` | `--status` · `--portfolio` · `--flag` | Checking milestone progress for a single account; portfolio milestone overview; flagging at-risk milestones |
| onboarding-plan | `/onboarding:onboarding-plan` | `--draft` · `--update` · `--summary` | Creating or updating a customer onboarding plan |
| success-criteria | `/onboarding:success-criteria` | `--define` · `--refine` · `--review` · `--export` | Defining or refining customer success criteria at onboarding start; exporting for customer sign-off |
| ttv-analysis | `/onboarding:ttv-analysis` | `--account` · `--portfolio` · `--patterns` | Calculating TtV pace for a single account; portfolio TtV overview; identifying systemic delay patterns |

---

## CS-Ops Plugin (`/cs-ops:*`)

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| capacity-planner | `/cs-ops:capacity-planner` | `--current` · `--headcount` · `--redistribution` · `--departure <csm-name>` | Assessing current CSM capacity; modeling headcount needs; planning account redistribution after CSM departure |
| cold-start-interview | `/cs-ops:cold-start-interview` | `--full` · `--section <name>` | First-run CS-Ops plugin setup; re-running a specific config section |
| customize | `/cs-ops:customize` | `--section <name>` · `--show` · `--reset <name>` | Viewing or updating CS-Ops config (segment definitions, capacity model, metric targets) |
| data-quality-check | `/cs-ops:data-quality-check` | `--full` · `--completeness` · `--staleness` · `--consistency` · `--field <name>` | Auditing CRM/CS Platform data quality; checking specific field coverage or data freshness |
| health-model-review | `/cs-ops:health-model-review` | `--distribution` · `--calibration` · `--component-audit` · `--full` | Auditing health model scoring distribution; calibrating component weights; full model review |
| metric-dashboard | `/cs-ops:metric-dashboard` | `--weekly` · `--monthly` · `--quarterly` · `--board` · `--csm-performance` | Generating CS metrics snapshot; building board-level KPI view; CSM performance report |
| playbook-auditor | `/cs-ops:playbook-auditor` | `--full` · `--coverage` · `--adoption` · `--dead-plays` · `--play <name>` | Auditing playbook coverage and adoption; identifying unused or stale plays |
| process-doc | `/cs-ops:process-doc` | `--csm-handoff` · `--playbook-governance` · `--data-quality` · `--escalation` · `--segment-change` · `--sop <name>` | Generating or updating CS process documentation; creating SOPs for specific workflows |
| segment-analyzer | `/cs-ops:segment-analyzer` | `--full` · `--segment <name>` · `--reclassification` · `--at-risk` | Analyzing segment health and distribution; identifying misclassified accounts; at-risk segment view |

---

## Rev-Ops Plugin (`/rev-ops:*`)

Rev-ops skills are single-mode — no mode flags. Trigger by natural language. Skills are
grouped by Skill Area for navigation; all commands follow the `/rev-ops:<skill-name>` pattern.

### SA1 — Forecast Intelligence

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| forecast-variance-analysis | `/rev-ops:forecast-variance-analysis` | — | Analyzing why forecast was missed; classifying variance by rep, deal band, or segment |
| scenario-modeling | `/rev-ops:scenario-modeling` | — | Building P10/P50/P90 range forecast; modeling win-rate sensitivity or downside scenarios |
| pipeline-coverage-analysis | `/rev-ops:pipeline-coverage-analysis` | — | Assessing pipeline coverage before a forecast call, board review, or quarter-close |
| pipeline-velocity-tracking | `/rev-ops:pipeline-velocity-tracking` | — | Tracking deal cycle time; flagging deals aging past historical stage averages |
| deal-classification | `/rev-ops:deal-classification` | — | Independent Commit / Best Case / Pipeline scoring without relying on rep self-reporting |
| deal-health-scoring | `/rev-ops:deal-health-scoring` | — | Five-dimension health score per open opportunity; identifying at-risk deals this quarter |
| next-best-action-recommendation | `/rev-ops:next-best-action-recommendation` | — | Producing specific interventions for deals flagged at-risk by health scoring or velocity tracking |
| revenue-brief-generation | `/rev-ops:revenue-brief-generation` | — | Generating weekly or monthly executive revenue narrative for RevOps lead review |
| gtm-unified-metrics-pulse | `/rev-ops:gtm-unified-metrics-pulse` | — | Weekly cross-functional metrics report covering pipeline, handoff quality, CS capacity, and churn flags |

### SA2 — Pipeline Health

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| stage-integrity-audit | `/rev-ops:stage-integrity-audit` | — | Detecting stage-skipping, backward movement, or stale stage in CRM before forecast pulls |
| field-completion-monitoring | `/rev-ops:field-completion-monitoring` | — | Tracking required field completion by rep and stage gate; pre-quarter-close hygiene |
| revenue-leakage-scanning | `/rev-ops:revenue-leakage-scanning` | — | Identifying underpriced services, missing expansion clauses, or renewal misalignment before close |
| non-standard-terms-detection | `/rev-ops:non-standard-terms-detection` | — | Flagging off-playbook payment terms, SLA commitments, or custom provisions for Legal/Finance routing |
| sales-cs-handoff-quality-scoring | `/rev-ops:sales-cs-handoff-quality-scoring` | — | Scoring closed/won deals on handoff completeness; triggering AE manager issue when below threshold |

### SA3 — Planning Engine

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| annual-planning-workflow | `/rev-ops:annual-planning-workflow` | — | Initiating the seven-phase annual or mid-year planning cycle (gated, phase-by-phase) |
| unit-of-growth-calculator | `/rev-ops:unit-of-growth-calculator` | — | Computing GTM headcount requirements and capacity diagnostics using the UoG pod model |
| quota-sensitivity-analysis | `/rev-ops:quota-sensitivity-analysis` | — | Modeling quota achievability at multiple attainment levels; standalone or inside annual planning |
| territory-optimization | `/rev-ops:territory-optimization` | — | Evaluating territory fairness across reps; proposing recarves when imbalance exceeds threshold |
| closed-won-to-cs-capacity-modeling | `/rev-ops:closed-won-to-cs-capacity-modeling` | — | Converting sales forecast into CS resource demand; flagging CS capacity ceiling against headcount |
| growth-model-vs-actuals-tracking | `/rev-ops:growth-model-vs-actuals-tracking` | — | Monitoring NRR, GRR, and CAC against UoG plan baseline; routing to replan when drift exceeds threshold |
| mid-year-replan-triggering | `/rev-ops:mid-year-replan-triggering` | — | Monitoring plan-vs-actual drift; producing a replan recommendation memo when thresholds are crossed |
| change-communication-packaging | `/rev-ops:change-communication-packaging` | — | Producing a data-backed rationale memo + FAQ + rollout sequence for territory, quota, or comp changes |

### SA4 — CRM Data Quality

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| crm-hygiene-audit | `/rev-ops:crm-hygiene-audit` | — | Overall CRM health score and rep-level scorecard (completeness, accuracy, recency) |
| duplicate-detection | `/rev-ops:duplicate-detection` | — | Identifying duplicate accounts, contacts, or opportunities with merge-candidate confidence scores |
| data-decay-tracking | `/rev-ops:data-decay-tracking` | — | Flagging stale contacts and account data overdue for enrichment |
| cross-system-reconciliation | `/rev-ops:cross-system-reconciliation` | — | Tracing conflicting ARR or pipeline numbers across CRM, Finance Sheets, and CS platform |

### SA5 — Revenue Continuity

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| early-churn-downgrade-signal-detection | `/rev-ops:early-churn-downgrade-signal-detection` | — | Three-tier churn model: structural risk at close, behavioral signals 30–90 days post-onboarding, late-stage risk pre-renewal |
| outcome-to-value-tracking | `/rev-ops:outcome-to-value-tracking` | — | Mapping customers to L0–L3 rubric levels on OCV entries; surfacing systemic outcome delivery gaps |
| deal-to-outcome-tracing | `/rev-ops:deal-to-outcome-tracing` | — | Linking closed/won deals to CS trajectory and OCV rubric checkpoints at 30/60/90/180 days |
| outcome-statement-builder | `/rev-ops:outcome-statement-builder` | — | Transforming product capabilities into structured outcome statements for OCV catalog development |

### SA6 — Deal Desk

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| deal-desk-workflow-management | `/rev-ops:deal-desk-workflow-management` | — | Managing deal desk approval routing (submit → review → route → decide → log); SLA enforcement |
| discount-threshold-monitoring | `/rev-ops:discount-threshold-monitoring` | — | Flagging deals exceeding approved discount thresholds; routing to correct approval authority |

### Rev-Ops Setup

| Skill | Command | Modes | Typical trigger condition |
|-------|---------|-------|--------------------------|
| cold-start-interview | `/rev-ops:cold-start-interview` | — | First-run rev-ops plugin setup; re-run after major planning cycle changes |

---

## Cross-Plugin Patterns

Common multi-skill workflows that cross plugin boundaries:

| Workflow | Skills involved | Sequence |
|----------|----------------|----------|
| At-risk account triage → escalation | `/csm:health-score-review`, `/csm:risk-flag`, `/renewals:risk-assessment`, `/csm:escalation-memo` | Health review → risk flag → renewal risk → escalation memo |
| Renewal preparation | `/csm:renewal-readiness`, `/renewals:expansion-signal`, `/renewals:negotiation-prep`, `/renewals:renewal-forecast` | Readiness check → expansion scan → negotiation prep → forecast update |
| QBR preparation | `/csm:account-research`, `/csm:value-statement`, `/csm:qbr-builder` | Account research → value statement → QBR build |
| Onboarding close → CSM handoff | `/onboarding:handoff-doc`, `/onboarding:ttv-analysis`, `/csm:success-plan-builder` | Handoff doc → TtV final → success plan creation |
| Portfolio health ops review | `/csm:health-score-review --portfolio`, `/cs-ops:health-model-review`, `/cs-ops:metric-dashboard` | Portfolio triage → model calibration → metrics snapshot |
| Capacity change event | `/cs-ops:capacity-planner --departure`, `/cs-ops:capacity-planner --redistribution` | Departure flag → redistribution plan |
| Expansion CSQL → onboarding plan | `/csm:expansion-business-case`, `/rev-ops:csql-tracking`, `/csm:expansion-onboarding operation=create` | Build business case → log CSQL win in Rev-Ops → create expansion onboarding plan |

---

## Registry Maintenance

- Add new skills here before or when the skill SKILL.md is created
- Update modes when `argument-hint` changes in a SKILL.md
- Cross-plugin patterns table is illustrative — add patterns as workflows are validated
- This file is the source of truth; individual SKILL.md files must not hardcode alternative command strings
