# Cross-Skill Registry — claude-for-customer-success

Canonical reference for all skills across all plugins. Use this registry to determine
which skill and command to invoke for a given task. Do not hardcode skill command
strings in individual SKILL.md files — reference this document instead.

Last updated: 2026-05-14

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

---

## Registry Maintenance

- Add new skills here before or when the skill SKILL.md is created
- Update modes when `argument-hint` changes in a SKILL.md
- Cross-plugin patterns table is illustrative — add patterns as workflows are validated
- This file is the source of truth; individual SKILL.md files must not hardcode alternative command strings
