# CS Agent Capability Model — By Customer Lifecycle Stage

> **Status:** [DRAFT — updated 2026-05-18 to reflect 80-skill suite]  
> **Source catalog:** `cs-capability-model.yaml` (80 skills, VALIDATED 2026-05-16; +7 new skills 2026-05-18; rev-ops.territory-optimization deprecated)  
> **Lifecycle framework:** Seven-Stage Customer Lifecycle (Stages 0–6)  
> **Domain coverage:** cs-ops · csm · onboarding · renewals · rev-ops  

This document organizes all 80 skills in the `claude-for-customer-success` agent system by the customer lifecycle stage where they deliver primary value. For full schema detail (inputs, outputs, integration, guardrails, evaluation signals), see `cs-capability-model.yaml`.

**Reading format per skill entry:**
```
- `domain.skill-id` — One-line summary
  Tasks: key task 1 · key task 2 · key task 3
```

---

## Outcome & Value Statement Model

Before using the lifecycle map, understand the two-layer structure that governs how outcomes and value are defined, communicated, and tracked across the entire lifecycle.

**Layer 1 — Market-level (catalog)**  
Canonical outcome and value statements built from product capabilities and ICP patterns. These define *what the product can deliver* in structured, repeatable language — the authoritative vocabulary for sales, marketing, and CS. Built once, maintained as the product evolves. They are not account-specific; they are the template from which all customer-level statements are derived.

> Primary skill: `rev-ops.outcome-statement-builder` — constructs and maintains the catalog-level outcome statement library.

**Layer 2 — Customer-level (tailored)**  
Layer 1 statements instantiated with the customer's terminology, metrics, business context, and committed success criteria. The core outcome or value claim does not change — no new outcomes are invented — but language is adapted to the customer's world. "Reduce manual reconciliation time" becomes "eliminate the 3-day month-end close your RevOps team runs in spreadsheets."

> Primary skill: `csm.value-statement` — generates customer-specific value narratives consuming Layer 1 as input.

**Lifecycle flow of outcome and value language:**

| Layer | When created | Artifact | Primary skill |
|-------|-------------|----------|---------------|
| L1 Market outcomes | Pre-sales / catalog build | Outcome Catalog entries | `rev-ops.outcome-statement-builder` |
| L1 Market value statements | Pre-sales / catalog build | Value statement templates | `rev-ops.outcome-statement-builder` |
| L2 Customer outcome statements | Stage 0 — sales plan | Deal-specific outcome map | `rev-ops.outcome-statement-builder` (tailoring mode) |
| L2 Customer value baseline | Stage 0–1 — success criteria | Success plan value baseline | `csm.value-statement` + `onboarding.success-criteria` |
| L2 Realized value statements | Stages 2–6 — proof | QBR, exec summary, advocacy | `csm.value-statement` · `renewals.executive-summary` · `rev-ops.revenue-brief-generation` |

The outcome catalog must exist before Stage 0 begins. Without Layer 1, every CSM invents their own language — and the value conversation breaks down at renewal.

---

## Stage 0 — Pre-Onboarding
*Sales-to-CS bridge, expectation calibration, stakeholder identification, implementation readiness, outcome and value baseline.*

### System Configuration (All Domains)
These meta-skills configure each domain agent's CLAUDE.md before any customer-facing work begins. Run once per deployment or major environment change.

- `csm.cold-start-interview` — Guided interview to capture CSM team context, tech stack, and operating norms
  Tasks: extract team size and segment · capture CRM and health score tooling · write domain CLAUDE.md
- `csm.customize` — Apply interview outputs to personalize CSM agent behavior
  Tasks: inject company-specific terminology · set default account segments · configure escalation paths

- `onboarding.cold-start-interview` — Guided interview for onboarding team context and tooling
  Tasks: capture kickoff template preferences · identify integration dependencies · set milestone definitions
- `onboarding.customize` — Apply interview outputs to personalize onboarding agent behavior
  Tasks: inject onboarding playbook norms · set TtV benchmarks · configure handoff criteria

- `cs-ops.cold-start-interview` — Guided interview for CS Ops team context, metrics, and data systems
  Tasks: capture health model inputs · identify reporting cadences · map data source integrations
- `cs-ops.customize` — Apply interview outputs to personalize CS Ops agent behavior
  Tasks: set metric calculation conventions · configure segment definitions · inject tooling context

- `renewals.cold-start-interview` — Guided interview for renewals team context, contract norms, and risk thresholds
  Tasks: capture ARR bands and renewal motions · identify contract system integrations · set churn risk thresholds
- `renewals.customize` — Apply interview outputs to personalize renewals agent behavior
  Tasks: inject pricing and discount norms · configure expansion signal definitions · set executive summary format

- `rev-ops.cold-start-interview` — Guided interview for Rev Ops team context, GTM motion, and data infrastructure
  Tasks: capture CRM stage definitions · identify forecast methodology · map territory and quota structures

### Outcome & Value Catalog (Layer 1)
The market-level outcome and value statement library must be built before customer-facing work begins. These are the templates that all downstream customer-level statements derive from.

- `rev-ops.outcome-statement-builder` *(Layer 1 — catalog build; also Layer 2 — customer tailoring at Stage 0)* — Build and maintain structured outcome statements connecting product capabilities to business value at the market and customer level
  Tasks: extract capability patterns from ICP and product data · construct canonical outcome statements in structured format · generate customer-tailored variants preserving core outcome language

### Pre-Onboarding Operations
- `rev-ops.sales-cs-handoff-quality-scoring` — Score the completeness and quality of sales-to-CS handoff packages, including whether customer-level outcome statements were captured during the sales process
  Tasks: audit handoff document completeness · flag missing outcome statements or success criteria · generate readiness score with remediation list

---

## Stage 1 — Onboarding
*Kickoff execution, onboarding plan delivery, milestone tracking, time-to-value acceleration, graduation handoff. Customer-level outcome and value baseline locked into success criteria.*

- `onboarding.kickoff-prep` — Prepare all materials and agenda for the customer kickoff meeting
  Tasks: pull stakeholder roster from CRM · generate agenda aligned to success criteria · surface open pre-work items

- `onboarding.onboarding-plan` — Build a structured, time-bound onboarding plan with milestones and owner assignments
  Tasks: define phase gates and dependencies · assign DRI per milestone · export shareable plan document

- `onboarding.success-criteria` — Translate customer goals into measurable, agreed-upon success criteria, using Layer 1 outcome statements as the structural template and customer language as the surface
  Tasks: extract goals from discovery notes · map goals to catalog outcome statements · draft customer-specific criteria for sign-off

- `onboarding.milestone-tracker` — Track milestone completion status and surface blockers in real time
  Tasks: pull current milestone status · flag overdue or at-risk milestones · generate stakeholder progress update

- `onboarding.blocker-review` — Identify, triage, and action onboarding blockers
  Tasks: surface blocker log from tracker · classify blockers by type and owner · draft escalation memo for critical blockers

- `onboarding.ttv-analysis` — Analyze time-to-value performance against benchmarks and surface acceleration opportunities
  Tasks: calculate TtV for current cohort · compare to segment benchmarks · identify top delay drivers

- `onboarding.handoff-doc` — Generate the graduation handoff document transitioning the account to post-onboarding CS, including the committed outcome and value baseline
  Tasks: summarize onboarding outcomes vs. criteria · document open items and owner assignments · package for CSM intake

- `csm.expansion-onboarding` — Execute the onboarding workflow for a newly-closed expansion — additional seats, tier upgrade, or new product module — triggered by a won CSQL from rev-ops.csql-tracking
  Tasks: generate expansion onboarding plan with milestones · align stakeholders to new scope and success criteria · produce expansion handoff brief for ongoing CSM ownership

---

## Stage 2 — Adoption
*Product usage deepening, success plan execution, stakeholder engagement, initial value realization against the committed baseline.*

- `csm.success-plan-builder` — Build or refresh a structured success plan aligned to customer outcomes, anchoring to the Layer 2 outcome statements established at Stage 0–1
  Tasks: map customer goals to catalog outcome statements · define leading indicators per goal · draft success plan for customer review

- `csm.success-plan-canvas` — Generate a one-page visual success plan canvas summarizing the account's committed outcomes, key milestones, health signals, and CSM action priorities; designed for customer-facing alignment conversations
  Tasks: pull committed success criteria and current health signals · map milestones to outcome categories · produce shareable canvas for customer review

- `csm.taro-play-runner` — Execute a TARO-structured CS play (Trigger → Action → Resource → Outcome)
  Tasks: identify trigger condition · select appropriate play · generate action steps with resources

- `csm.stakeholder-map` — Build and maintain a stakeholder map for an account
  Tasks: identify key personas and decision-makers · assess relationship strength per stakeholder · flag engagement gaps

- `csm.account-research` — Research an account's business context, industry signals, and product usage profile
  Tasks: pull firmographic and technographic data · surface recent news or funding signals · synthesize account brief

- `csm.call-prep` — Prepare for a CSM customer call with agenda, account context, and recommended talking points
  Tasks: pull recent health and usage data · surface open action items · draft agenda with risk and opportunity flags

- `csm.value-statement` *(Layer 2 — customer-level; also Stage 3 Nurture, Stage 4 Growth, Stage 5 Retention, Stage 6 Advocacy)* — Generate a customer-specific value statement quantifying realized outcomes against the committed baseline; consumes Layer 1 catalog statements as structural input
  Tasks: pull usage and outcome metrics against committed baseline · map metrics to customer business impact language · draft executive-ready value narrative

---

## Stage 3 — Nurture
*QBR delivery, health monitoring, risk identification, ongoing stakeholder engagement. Value statement updated each QBR cycle.*

- `csm.health-score-review` — Review current health score signals for an account and recommend interventions
  Tasks: pull multi-dimensional health inputs · surface degradation signals · generate recommended CSM actions

- `csm.qbr-builder` — Build a Quarterly Business Review deck with outcome data, risks, and next-period plan; value statement provides the realized-value narrative for each QBR
  Tasks: aggregate usage and outcome data for the period · frame results against committed success criteria · draft QBR narrative with recommendations

- `csm.success-plan-progress-review` — Review progress against a customer's active success plan, surfacing milestone completions, lagging indicators, and recommended adjustments before the next CSM touchpoint or QBR
  Tasks: pull current milestone status vs. success plan targets · flag lagging or at-risk indicators · generate progress summary with recommended CSM actions

- `csm.risk-flag` — Identify and document a risk signal for an account with recommended response
  Tasks: characterize the risk type and severity · document evidence · draft risk memo with escalation recommendation

- `csm.escalation-memo` — Draft an internal escalation memo for an at-risk account requiring cross-functional response
  Tasks: summarize account history and current state · articulate business impact · recommend escalation path and owners

- `cs-ops.health-model-review` — Audit the CS health scoring model for coverage gaps, weighting issues, and data quality
  Tasks: review signal coverage across lifecycle stages · assess weight calibration vs. churn/expansion outcomes · recommend model updates

- `cs-ops.playbook-auditor` — Audit existing CS playbooks for currency, coverage, and alignment to current ICP and product
  Tasks: inventory active playbooks · flag outdated or missing plays · generate remediation priority list

---

## Stage 4 — Growth
*Expansion signal identification, upsell/cross-sell execution, outcome-to-value tracking. Customer-level outcome statements extended for expansion scope.*

- `renewals.expansion-signal` — Identify expansion signals in an account and surface them to the CSM or AE
  Tasks: analyze usage patterns for expansion indicators · cross-reference with product capability gaps · generate expansion brief for sales handoff

- `csm.expansion-business-case` — Build a structured expansion business case for an account where usage signals or CSM judgment indicate expansion readiness; produces the CSQL that feeds rev-ops.csql-tracking
  Tasks: qualify expansion opportunity against adoption and outcome signals · quantify expected value for customer and seller · generate CSQL brief for rev-ops handoff

- `rev-ops.csql-tracking` — Track CS-Qualified Leads (CSQLs) from identification through closed expansion, recording source, pipeline stage, ARR value, and close outcome; bridges csm.expansion-business-case and csm.expansion-onboarding
  Tasks: log new CSQL with source, ARR estimate, and owning CSM · update CSQL stage as opportunity progresses · close out CSQL as won (triggers expansion-onboarding) or lost (triggers RCA)

- `rev-ops.outcome-to-value-tracking` — Track whether promised outcomes are being realized and surface deviations from the committed baseline
  Tasks: pull committed outcomes from success plan · compare to current performance data · flag at-risk outcomes with root cause

- `rev-ops.deal-to-outcome-tracing` — Trace closed deals back to the customer outcomes they were sold on, verifying Layer 1 catalog accuracy against delivery reality
  Tasks: retrieve deal close notes and opportunity data · map deal promises to catalog outcome statements · surface gaps between sold and delivered outcomes

- `rev-ops.next-best-action-recommendation` — Recommend the highest-impact next action for an account based on current signals
  Tasks: aggregate health, usage, and engagement signals · score action options by expected impact · generate prioritized action recommendation

- `rev-ops.revenue-leakage-scanning` — Scan the revenue base for leakage patterns including unused seats, contract mismatches, and billing gaps
  Tasks: cross-reference contract terms with billing records · flag seat and license discrepancies · generate leakage report with remediation steps

- `csm.value-statement` *(also Stage 2 Adoption)* — At growth stage, value statement surfaces expansion-relevant outcomes to support upsell and cross-sell conversations
  Tasks: pull realized outcomes and usage headroom · frame value in terms of expansion opportunity · draft expansion-oriented value narrative

---

## Stage 5 — Retention
*Renewal forecasting, risk assessment, contract negotiation, churn prevention, post-churn analysis. Value statement anchors negotiation and price justification.*

- `renewals.renewal-forecast` — Generate a renewal forecast for a book of business with confidence ratings and risk flags
  Tasks: score each renewal by likelihood · aggregate ARR at risk by tier · generate forecast summary for leadership

- `renewals.risk-assessment` — Conduct a structured risk assessment for a renewal account
  Tasks: score risk across health, engagement, champion, and competitive dimensions · weight by ARR and strategic value · generate risk brief with recommended interventions

- `renewals.contract-review` — Review contract terms ahead of renewal for risk, negotiation leverage, and compliance gaps
  Tasks: extract key contract terms · flag non-standard clauses or expiring protections · summarize negotiation position

- `renewals.negotiation-prep` — Prepare a negotiation brief for an upcoming renewal conversation
  Tasks: summarize account health and outcome realization · document leverage points and risk factors · draft recommended negotiation posture

- `renewals.price-increase-prep` — Prepare messaging and objection handling for a price increase conversation, grounded in the realized value statement
  Tasks: calculate value delivered vs. price paid using customer value statement · draft value justification narrative · anticipate objections with recommended responses

- `renewals.executive-summary` — Generate an executive-ready account summary for renewal or QBR conversations, synthesizing the customer-level value statement with health and outcomes data
  Tasks: synthesize health, outcomes, and engagement data · frame summary for executive audience · include strategic recommendations

- `renewals.churn-rca` — Analyze a fully-churned account (full cancellation) to identify root causes and systemic failure patterns; scoped to complete cancellations only — contract contractions route to renewals.downgrade-analysis
  Tasks: reconstruct account timeline from signals · classify churn cause category · generate learnings brief for CS and product

- `renewals.downgrade-analysis` — Analyze a contract contraction request (seat reduction, scope reduction, tier downgrade) to diagnose drivers, quantify ARR impact, and produce counter-proposal inputs; scoped to contractions only — full cancellations route to renewals.churn-rca
  Tasks: analyze contraction drivers across budget, value gap, and usage dimensions · quantify ARR impact of proposed vs. alternative scenarios · generate counter-proposal inputs for renewals.negotiation-prep

- `csm.renewal-readiness` — Assess whether a CSM's account portfolio is positioned for successful renewals
  Tasks: score renewal readiness per account · flag accounts needing immediate intervention · generate portfolio renewal health summary

- `rev-ops.early-churn-downgrade-signal-detection` — Detect early warning signals of churn or downgrade risk before they reach the renewal stage
  Tasks: monitor usage, engagement, and support signal patterns · score churn probability by account · generate early warning alert list with recommended actions

---

## Stage 6 — Advocacy
*Executive value proof, reference generation, community contribution, customer-led growth. Customer value statement reaches its fullest expression as external proof.*

- `csm.value-statement` *(Layer 2 — full realization; also Stages 2–5)* — At advocacy stage, the customer value statement is finalized as an external-facing proof asset for case studies, reference calls, and executive presentations; the same Layer 1 structure, now fully evidenced
  Tasks: pull complete outcome and metric history · map to business impact in customer's own language · draft executive-ready narrative suitable for external reference use

- `rev-ops.revenue-brief-generation` — Generate a revenue-narrative brief connecting customer outcomes to commercial results for executive and board audiences
  Tasks: aggregate ARR, expansion, and retention data · frame revenue story in terms of customer outcomes · generate brief for executive or investor consumption

---

## Cross-Cutting Operations
*Infrastructure, data quality, capacity, forecasting, planning, and process skills that support all lifecycle stages.*

### CS Operations
- `cs-ops.capacity-planner` — Model CSM capacity against current and projected book of business
  Tasks: calculate current capacity utilization by segment · model headcount scenarios against pipeline · generate capacity recommendation

- `cs-ops.data-quality-check` — Audit CS data inputs for completeness, accuracy, and currency
  Tasks: scan CRM and health data for missing or stale fields · score data quality by segment · generate remediation priority list

- `cs-ops.metric-dashboard` — Build or refresh a CS metrics dashboard for team or leadership consumption
  Tasks: pull current period metrics across health, TtV, renewal, and expansion dimensions · compare to targets · generate dashboard summary narrative

- `cs-ops.process-doc` — Document a CS process or workflow for team reference and onboarding
  Tasks: extract process steps from practitioner input · structure as RACI-aligned workflow · generate shareable process doc

- `cs-ops.segment-analyzer` — Analyze the CS book of business by segment to surface coverage, health, and resource allocation patterns
  Tasks: aggregate account data by segment · score segment health distribution · generate segment analysis with capacity and risk recommendations

### Revenue Operations — Pipeline & Forecast
- `rev-ops.pipeline-coverage-analysis` — Analyze pipeline coverage ratios against quota targets by rep, team, and period
  Tasks: calculate coverage by stage and segment · flag coverage gaps vs. targets · generate coverage report with recommended actions

- `rev-ops.pipeline-velocity-tracking` — Track deal velocity through pipeline stages and surface acceleration or deceleration patterns
  Tasks: calculate average stage duration by cohort · compare current vs. historical velocity · surface stalled deals with intervention recommendations

- `rev-ops.forecast-variance-analysis` — Analyze forecast vs. actuals variance to improve forecast accuracy
  Tasks: compare committed forecast to closed actuals · classify variance by type and owner · generate forecast calibration recommendations

- `rev-ops.growth-model-vs-actuals-tracking` — Compare growth model assumptions to actual performance and surface deviation drivers
  Tasks: pull model assumptions vs. current actuals · calculate variance by driver · generate deviation brief with model update recommendations

- `rev-ops.gtm-unified-metrics-pulse` — Generate a unified GTM metrics pulse across sales, CS, and marketing
  Tasks: aggregate key metrics across GTM functions · surface cross-functional trends and anomalies · generate unified pulse report

- `rev-ops.scenario-modeling` — Model revenue scenarios under different assumptions for planning and decision support
  Tasks: define scenario parameters with user input · calculate revenue outcomes per scenario · generate scenario comparison for leadership

- `rev-ops.quota-sensitivity-analysis` — Analyze quota sensitivity to changes in ramp, attrition, and performance distribution
  Tasks: model quota attainment under variable rep productivity assumptions · identify breakeven capacity requirements · generate sensitivity report

- `rev-ops.comp-simulation` — Model CSM and AE compensation plan outcomes against real or projected portfolio and pipeline data; calculates attainment, payout, and acceleration tier projections under current and proposed plan structures; outputs require HR + Finance dual review before rep distribution (G3)
  Tasks: project individual rep payout under current quota and commission structure · compare payout outcomes across comp plan variants · identify plan design anomalies including cliff risk, attainment bunching, and unintended upside

- `rev-ops.mid-year-replan-triggering` — Identify the conditions that should trigger a mid-year revenue plan revision
  Tasks: compare YTD actuals to plan thresholds · assess pipeline coverage against H2 targets · generate replan trigger recommendation with evidence

- `rev-ops.annual-planning-workflow` — Orchestrate the annual revenue planning workflow across GTM functions
  Tasks: sequence planning activities by function · surface dependencies and decision gates · generate planning calendar and owner assignments

### Revenue Operations — Deal Quality & Data Integrity
- `rev-ops.crm-hygiene-audit` — Audit CRM data quality for completeness, accuracy, and stage integrity
  Tasks: scan opportunity records for missing required fields · flag stage-criteria mismatches · generate hygiene score with remediation list

- `rev-ops.cross-system-reconciliation` — Reconcile data across CRM, billing, and CS platforms to surface discrepancies
  Tasks: pull matching records across systems · identify field-level discrepancies · generate reconciliation report with resolution actions

- `rev-ops.data-decay-tracking` — Track data decay rates across key CRM and CS fields over time
  Tasks: measure field completeness change over rolling periods · identify decay hotspots by field and team · generate decay trend report

- `rev-ops.deal-classification` — Classify deals by type, motion, and strategic category for reporting and planning accuracy
  Tasks: apply classification rules to opportunity records · flag misclassified deals · generate classification audit report

- `rev-ops.deal-health-scoring` — Score deal health across pipeline stages using engagement, activity, and risk signals
  Tasks: pull multi-signal deal data · score health by stage-appropriate criteria · generate deal health report with intervention flags

- `rev-ops.deal-desk-workflow-management` — Manage deal desk workflow including approvals, exceptions, and escalation routing
  Tasks: track pending deal desk requests · flag stalled approvals · generate deal desk status report

- `rev-ops.discount-threshold-monitoring` — Monitor discount levels against policy thresholds and flag violations
  Tasks: pull discount data from opportunity records · compare to approved thresholds by tier · generate violation report with approval status

- `rev-ops.duplicate-detection` — Detect duplicate account, contact, and opportunity records across CRM systems
  Tasks: run fuzzy matching across key identifier fields · score duplicate confidence · generate duplicate report with merge recommendations

- `rev-ops.field-completion-monitoring` — Monitor required and recommended CRM field completion rates by team and stage
  Tasks: calculate field completion rates by team and stage gate · surface chronic gaps · generate completion scorecard with coaching flags

- `rev-ops.stage-integrity-audit` — Audit deal stage assignments for criteria compliance and progression integrity
  Tasks: check stage entry criteria met for all open opportunities · flag premature or stalled stage assignments · generate stage integrity report

### Revenue Operations — Capacity
- `rev-ops.unit-of-growth-calculator` — Calculate the unit economics of growth including CAC, LTV, and payback period
  Tasks: pull CAC and LTV inputs from finance and rev ops data · calculate unit economics by segment and cohort · generate growth unit report

- `rev-ops.closed-won-to-cs-capacity-modeling` — Model the CS capacity impact of projected closed-won volume
  Tasks: project CS workload from pipeline close assumptions · compare to current CS capacity · generate capacity gap report for hiring planning

### Revenue Operations — Strategy & Change
- `rev-ops.change-communication-packaging` — Package GTM process or policy changes for internal communication and enablement
  Tasks: draft change rationale and impact summary · identify affected roles and workflows · generate change communication package with training callouts

---

## Coverage Summary

| Lifecycle Stage | Primary Skills | Domains |
|-----------------|---------------|---------|
| Pre-catalog (L1 build) | 1 | rev-ops |
| Stage 0 Pre-Onboard | 10 config + 1 ops + L2 tailoring | all domains · rev-ops |
| Stage 1 Onboard | 8 | onboarding · csm |
| Stage 2 Adoption | 7 | csm |
| Stage 3 Nurture | 7 | csm · cs-ops |
| Stage 4 Growth | 8 | renewals · rev-ops · csm |
| Stage 5 Retention | 10 | renewals · csm · rev-ops |
| Stage 6 Advocacy | 2 | csm · rev-ops |
| Cross-Cutting Ops | 27 | cs-ops · rev-ops |
| **Total** | **80** | **5 domains** |

> **Two-layer outcome/value model:** `rev-ops.outcome-statement-builder` operates at both Layer 1 (catalog build, pre-sales) and Layer 2 (customer tailoring, Stage 0). `csm.value-statement` operates at Layer 2 across Stages 2–6, consuming Layer 1 as structural input. The core outcome or value claim never changes between layers — only the surface language adapts to the customer's context.

> **Multi-stage skills:** `csm.value-statement` spans Stages 2–6 — listed under Stage 2 (primary activation) with role notes at each subsequent appearance.

---

*Cross-reference: `cs-capability-model.yaml` — full schema with inputs, outputs, integration points, guardrails, and evaluation signals for all 81 skills.*
