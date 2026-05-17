# Customer Success Agent Capability Model

**Status:** [VALIDATED]  
**Date:** 2026-05-15  
**System:** `claude-for-customer-success`  
**Scope:** 8-stage customer lifecycle — agent capability per stage and task category

---

## Overview

This model describes what the `claude-for-customer-success` agentic system can do at each lifecycle stage — which skills handle which task categories, at what complexity tier, and how multi-skill compositions are triggered. It is organized by lifecycle stage rather than by plugin, to support journey-oriented thinking.

The system operates across five primary plugins — **csm**, **renewals**, **onboarding**, **cs-ops**, and **rev-ops** — with supporting capability provided by sales, marketing, customer-support, data, and operations plugins. The **Outcome & Value Catalog (OCV)** is not a plugin; it is an artifact produced by `rev-ops:outcome-statement-builder` and consumed by downstream skills (particularly `rev-ops:outcome-to-value-tracking`) that require a validated outcome library for value evidence scoring and tracking.

All skills execute against a practice profile (CLAUDE.md + company-profile.md) pre-flight, giving them account and organizational context without requiring explicit input on every call.

---

## Capability Model by Lifecycle Stage

---

### Stage 0 — Handoff

**Agent objective:** Receive, validate, and prepare a new account for customer ownership transfer.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Receive handoff package | `onboarding:handoff-doc` | T1 | `csm:account-research` | Structured handoff document with relationship map, deal context, commitments |
| Validate completeness | `cs-ops:data-quality-check` | T1 | `onboarding:handoff-doc` | Data quality report with gap flags and remediation actions |
| Score handoff quality | `rev-ops:sales-cs-handoff-quality-scoring` | T1 | `cs-ops:data-quality-check` | Handoff quality score with completeness flags fed to capacity planning |
| Kickoff preparation | `onboarding:kickoff-prep` | T1 | `csm:stakeholder-map` | Internal prep brief and customer-facing kickoff agenda |
| Cold start (thin data) | `csm:cold-start-interview` | T1 | — | Interview guide + initial account profile |

**Branch capability:**  
- Incomplete handoff → `data-quality-check` flags gaps → remediation actions returned inline; `sales-cs-handoff-quality-scoring` records systemic pattern for rev-ops reporting
- All cold-start variants handled by `cold-start-interview` (csm, renewals, onboarding, cs-ops, rev-ops each carry their own variant)

**Composition pattern:**  
`handoff-doc` → `data-quality-check` → `sales-cs-handoff-quality-scoring` → `kickoff-prep` (sequential, blocking)

---

### Stage 1 — Onboarding

**Agent objective:** Execute a structured onboarding program that achieves initial time-to-value and establishes success infrastructure.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Define success criteria | `onboarding:success-criteria` | T1 | `csm:success-plan-builder` | Signed success criteria document with measurable outcomes |
| Build onboarding plan | `onboarding:onboarding-plan` | T2 | `onboarding:success-criteria` | Phased onboarding plan with milestones, owners, dates |
| Track milestone progress | `onboarding:milestone-tracker` | T1 | — | Milestone status report with completion metrics |
| Resolve blockers | `onboarding:blocker-review` | T1 | `csm:escalation-memo` | Blocker analysis with prioritized resolution path |
| Stakeholder engagement | `csm:stakeholder-map` | T2 | `csm:call-prep` | Relationship map with engagement recommendations |
| Measure time-to-value | `onboarding:ttv-analysis` | T2 | `csm:value-statement` | TTV analysis with benchmark comparison and trajectory |
| Build success plan | `csm:success-plan-builder` | T2 | `onboarding:success-criteria`, `csm:value-statement` | Comprehensive success plan with goal framework |

**Branch capability:**  
- Stalled onboarding → `csm:risk-flag` → acceleration protocol
- Failed onboarding → `renewals:risk-assessment` → early churn assessment

**Composition pattern:**  
`success-criteria` → `onboarding-plan` → `milestone-tracker` (ongoing loop)  
`ttv-analysis` → `value-statement` (value measurement chain)  
`risk-flag` → `risk-assessment` → `escalation-memo` (at-risk branch)

---

### Stage 2 — Adoption

**Agent objective:** Drive product adoption, surface and resolve barriers, and quantify value realization.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Monitor adoption health | `csm:health-score-review` | T1 | `cs-ops:metric-dashboard` | Health score summary with trend analysis and risk indicators |
| Monitor portfolio-level metrics | `rev-ops:gtm-unified-metrics-pulse` | T1 | `rev-ops:growth-model-vs-actuals-tracking` | Portfolio adoption and revenue metrics; signals fed to capacity and planning models |
| Drive feature adoption | `csm:taro-play-runner` | T2 | `cs-enablement-toolkit:performance-support-designer` | Prescriptive play execution plan with owner assignments |
| Resolve adoption barriers | `onboarding:blocker-review` | T1 | `csm:risk-flag` | Barrier analysis with escalation recommendations |
| Quantify realized value | `csm:value-statement` | T2 | `rev-ops:outcome-to-value-tracking` | Value statement with quantified outcomes; outcome-to-value tracking scores evidence quality against OCV catalog |
| Flag at-risk signals | `csm:risk-flag` | T1 | `renewals:risk-assessment` | Risk summary with severity classification and recommended actions |
| Escalate unresolved risks | `csm:escalation-memo` | T1 | `renewals:risk-assessment` | Escalation memo for leadership with context and recommended resolution |

**Branch capability:**  
- Low adoption → `risk-flag` → `risk-assessment` → intervention play via `taro-play-runner`
- Non-usage → `risk-flag` → `escalation-memo` → `risk-assessment` (T2 full at-risk protocol)
- Portfolio metric divergence → `gtm-unified-metrics-pulse` → `growth-model-vs-actuals-tracking` → planning adjustment signal

**Composition pattern:**  
`health-score-review` → `risk-flag` (monitoring loop)  
`taro-play-runner` → `milestone-tracker` (play execution → tracking)  
`value-statement` + `outcome-to-value-tracking` (value evidence chain)  
`gtm-unified-metrics-pulse` → `growth-model-vs-actuals-tracking` (portfolio intelligence loop)

---

### Stage 3 — Nurture

**Agent objective:** Deepen executive and multi-stakeholder relationships, reinforce delivered value, and maintain proactive health governance.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| QBR preparation | `csm:qbr-builder` | T2 | `csm:value-statement`, `csm:health-score-review`, `renewals:executive-summary` | QBR deck with value narrative, health summary, and strategic roadmap |
| Call preparation | `csm:call-prep` | T1 | `csm:account-research` | Pre-call brief with objectives, context, recommended talking points |
| Stakeholder relationship mapping | `csm:stakeholder-map` | T2 | `csm:account-research` | Updated relationship map with engagement gaps and recommended actions |
| Executive engagement | `renewals:executive-summary` | T1 | `csm:stakeholder-map` | Executive-ready summary of account health and strategic value |
| Value reinforcement | `csm:value-statement` | T2 | `rev-ops:outcome-to-value-tracking` | Updated value statement with latest outcome evidence scored against OCV catalog |
| Proactive health monitoring | `csm:health-score-review` | T1 | `cs-ops:health-model-review` | Health score with trend analysis and proactive risk flags |

**Branch capability:**  
- Declining relationship → `csm:escalation-memo` → executive intervention protocol
- At-risk indicators → `renewals:risk-assessment` → save strategy pre-activation

**Composition pattern:**  
`health-score-review` → `risk-flag` → `escalation-memo` (proactive at-risk chain)  
`account-research` → `stakeholder-map` → `qbr-builder` (QBR preparation chain)  
`value-statement` + `outcome-to-value-tracking` → `qbr-builder` (value reinforcement chain)

---

### Stage 4 — Growth (Expansion)

**Agent objective:** Identify expansion opportunities, build business case, support expansion selling, and onboard expanded scope.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Identify expansion signals | `renewals:expansion-signal` | T1 | `csm:account-research` | Expansion signal report with opportunity prioritization |
| Trace deal-to-outcome alignment | `rev-ops:deal-to-outcome-tracing` | T1 | `rev-ops:outcome-to-value-tracking` | Outcome delivery map; shows where committed outcomes are being met and where expansion makes sense |
| Detect early churn/downgrade risk | `rev-ops:early-churn-downgrade-signal-detection` | T1 | `csm:risk-flag` | Early-warning signal for accounts signaling churn or contraction before formal at-risk classification |
| Build expansion business case | `renewals:negotiation-prep` ⚠️ | T2 | `renewals:price-increase-prep`, `csm:value-statement` | Negotiation context doc; upsell-specific business case requires adaptation |
| Support expansion selling | `csm:stakeholder-map` + `sales:call-prep` ⚠️ | T2 | `sales:pipeline-review` | Stakeholder alignment and sales call preparation; no native expansion-close skill |
| Define expansion success criteria | `onboarding:success-criteria` ⚠️ | T1 | — | Success criteria adapted for expansion scope; onboarding context assumes greenfield |
| Execute expansion onboarding | `onboarding:onboarding-plan` ⚠️ | T2 | `cs-enablement-toolkit:learning-journey-architect` | General onboarding plan; expansion-specific contextual adaptation needed |
| Handle expansion declined | `csm:taro-play-runner` ⚠️ | T1 | `csm:risk-flag` | Play execution for declined expansion; no dedicated expansion-declined play |

⚠️ = Partially covered — skills apply with adaptation; see gap report for details

**Composition pattern:**  
`expansion-signal` → `account-research` → `deal-to-outcome-tracing` → `negotiation-prep` (expansion identification + evidence chain)  
`early-churn-downgrade-signal-detection` → `risk-flag` → `risk-assessment` (early warning chain)  
`stakeholder-map` → `sales:call-prep` (expansion selling bridge)  
`success-criteria` → `onboarding-plan` → `milestone-tracker` (expansion onboarding chain, reused)

---

### Stage 5 — Retention (Renewal)

**Agent objective:** Prepare for renewal, assess and mitigate risk, build business case, execute renewal, and save at-risk accounts.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Initiate renewal timeline | `csm:renewal-readiness` | T1 | `renewals:contract-review` | Renewal readiness assessment with timeline and risk indicators |
| Review contract terms | `renewals:contract-review` | T1 | — | Contract analysis with term flags and negotiation points |
| Assess renewal risk | `renewals:risk-assessment` | T2 | `csm:risk-flag`, `renewals:renewal-forecast` | Risk assessment with scoring, drivers, and mitigation recommendations |
| Forecast renewal | `renewals:renewal-forecast` | T2 | `renewals:risk-assessment` | Renewal probability forecast with scenario modeling |
| Build renewal business case | `csm:value-statement` | T2 | `renewals:executive-summary`, `rev-ops:outcome-to-value-tracking` | Value evidence package with ROI summary; outcome-to-value tracking scores evidence against OCV catalog |
| Model revenue and capacity impact | `rev-ops:forecast-variance-analysis` + `rev-ops:closed-won-to-cs-capacity-modeling` | T2 | `rev-ops:growth-model-vs-actuals-tracking` | Renewal outcome modeled against portfolio forecast; CS capacity impact of won/lost renewal quantified |
| Prepare renewal proposal | `renewals:negotiation-prep` | T2 | `renewals:price-increase-prep` | Negotiation strategy with terms, pricing options, and fallback positions |
| Handle price increase | `renewals:price-increase-prep` | T1 | `renewals:negotiation-prep` | Price increase communication strategy with justification framing |
| Develop save strategy | `renewals:churn-analysis` | T2 | `renewals:risk-assessment` | Churn driver analysis with save viability assessment |
| Execute save playbook | `csm:escalation-memo` | T1 | `renewals:churn-analysis` | Executive escalation with save options and owner assignments |

**Composition pattern (renewal execution):**  
`renewal-readiness` → `contract-review` → `risk-assessment` → `renewal-forecast` (renewal intelligence chain)  
`value-statement` + `outcome-to-value-tracking` → `executive-summary` → `negotiation-prep` (business case chain)  
`forecast-variance-analysis` + `closed-won-to-cs-capacity-modeling` → `growth-model-vs-actuals-tracking` (revenue continuity chain)  
`churn-analysis` → `risk-assessment` → `escalation-memo` (save play chain)

---

### Stage 6 — Advocacy

**Agent objective:** Identify advocates, facilitate references and success stories, enable community participation, and recognize contributions.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Identify advocate candidates | `csm:health-score-review` ⚠️ | T1 | `csm:account-research` | Health + relationship data; no advocate scoring rubric |
| Facilitate customer references | *(none)* | — | — | ❌ No coverage |
| Support success story development | `marketing:content-creation` ⚠️ | T1 | — | Content creation support; no CSM-native story coordination skill |
| Enable community participation | *(none)* | — | — | ❌ No coverage |
| Recognize/reward advocates | *(none)* | — | — | ❌ No coverage |

**Branch capability:** Minimal. Advocacy declined → low-effort alternatives not specifically guided. Advocate fatigue → no fatigue management skill.

---

### Stage 7 — Churn / Non-Renewal

**Agent objective:** Execute professional offboarding, capture learning, share insights, update playbooks, and maintain win-back relationship.

| Task Category | Primary Skill | Tier | Supporting Skills | Output |
|---------------|---------------|------|-------------------|--------|
| Professional offboarding | *(none)* | — | — | ❌ No coverage |
| Exit interview | `renewals:churn-analysis` ⚠️ | T2 | — | Post-mortem analytics; live interview facilitation not guided |
| Internal post-mortem | `renewals:churn-analysis` + `cs-ops:playbook-auditor` ⚠️ | T2 | — | Churn analytics + playbook gap analysis; meeting facilitation not guided |
| Extract learnings | `cs-ops:playbook-auditor` ⚠️ | T1 | `renewals:churn-analysis` | Playbook gap identification; learning synthesis implicit not explicit |
| Share learnings / update playbooks | `cs-ops:process-doc` ⚠️ | T1 | `cs-ops:playbook-auditor`, `operations:runbook` | Process documentation and playbook updates; distribution workflow not guided |
| Maintain win-back relationship | *(none)* | — | — | ❌ No coverage |

---

## Cross-Stage Composition Patterns

These are the multi-skill invocation sequences that drive the highest-value outcomes in the system.

### Pattern 1 — Account Intelligence Baseline
`csm:account-research` → `csm:stakeholder-map` → `csm:value-statement`  
*Builds a complete account context layer: who they are, who matters, what value has been delivered. Used at stage transitions and ahead of high-stakes meetings.*

### Pattern 2 — QBR Preparation Chain
`csm:account-research` → `csm:value-statement` + `rev-ops:outcome-to-value-tracking` → `csm:health-score-review` → `csm:qbr-builder`  
*Full QBR preparation from account intelligence through value evidence (scored against OCV catalog) to health context to structured deck. Optionally adds `renewals:executive-summary` for exec-facing delivery.*

### Pattern 3 — Renewal Intelligence Chain
`csm:renewal-readiness` → `renewals:contract-review` → `renewals:risk-assessment` → `renewals:renewal-forecast`  
*Complete renewal readiness picture. Outputs feed directly into the renewal execution chain.*

### Pattern 4 — Renewal Execution Chain
`csm:value-statement` + `rev-ops:outcome-to-value-tracking` → `renewals:executive-summary` → `renewals:negotiation-prep`  
*Builds the renewal business case from value evidence (scored against OCV catalog) through executive narrative to negotiation strategy.*

### Pattern 5 — At-Risk Escalation Chain
`csm:health-score-review` → `csm:risk-flag` → `renewals:risk-assessment` → `csm:escalation-memo`  
*Full at-risk escalation path: detect → assess → escalate. Applies across stages 2, 3, and 5.*

### Pattern 6 — Save Play Chain
`renewals:churn-analysis` → `renewals:risk-assessment` → `csm:escalation-memo`  
*Stage 5 save play activation. `churn-analysis` establishes root causes; `risk-assessment` validates save viability; `escalation-memo` drives executive involvement.*

### Pattern 7 — Onboarding Execution Loop
`onboarding:success-criteria` → `onboarding:onboarding-plan` → `onboarding:milestone-tracker` → `onboarding:blocker-review` (cyclical)  
*Core onboarding execution. Milestone-tracker and blocker-review cycle until TTV milestone is achieved, then gates to ttv-analysis.*

### Pattern 8 — Expansion Identification Chain
`renewals:expansion-signal` → `csm:account-research` → `rev-ops:deal-to-outcome-tracing` → `csm:stakeholder-map`  
*Identifies expansion opportunity, traces outcome delivery alignment as business case foundation, maps stakeholders for expansion conversation. Bridges to negotiation-prep for proposal.*

### Pattern 9 — Revenue Continuity Chain (Rev-Ops)
`rev-ops:forecast-variance-analysis` → `rev-ops:closed-won-to-cs-capacity-modeling` → `rev-ops:growth-model-vs-actuals-tracking`  
*Portfolio-level revenue health: variance analysis identifies forecast gaps; capacity modeling translates renewal outcomes to CS resource requirements; actuals tracking closes the feedback loop to planning.*

### Pattern 10 — Handoff Quality Chain
`onboarding:handoff-doc` → `cs-ops:data-quality-check` → `rev-ops:sales-cs-handoff-quality-scoring`  
*Validates new account handoff completeness and quality; scores feed rev-ops portfolio reporting to surface systemic handoff issues across Sales-to-CS transitions.*

### Pattern 11 — Early Warning Chain
`rev-ops:early-churn-downgrade-signal-detection` → `csm:risk-flag` → `renewals:risk-assessment`  
*Pre-emptive risk surfacing at Stage 4: early signals trigger risk classification before formal at-risk designation, enabling earlier intervention.*

---

## Tier Distribution

| Tier | Skill Count (approx.) | Description |
|------|----------------------|-------------|
| T1 | ~35 | Single skill, direct output, minimal orchestration |
| T2 | ~22 | Structured analysis, multi-input synthesis, recommended context loading |
| T3 | ~5 | Multi-skill orchestration, cross-plugin composition, strategic output |

Rev-ops adds 33 skills across portfolio intelligence, forecasting, pipeline health, CRM data quality, revenue operations, and planning functions; the majority are T1–T2. T3 scenarios span: full renewal execution (readiness → risk → forecast → business case → negotiation), at-risk escalation through to executive intervention, multi-stage expansion management, and annual planning orchestration.

---

## System Architecture Notes

**Practice profile pre-flight:** All skills read CLAUDE.md + company-profile.md before executing. This means account context, product terminology, and organizational conventions are injected without requiring explicit user input on every skill invocation. Skills behave as informed colleagues, not generic assistants.

**Five-plugin architecture:** The system's primary execution capability lives in csm, renewals, onboarding, cs-ops, and rev-ops. Rev-ops operates as the portfolio intelligence and organizational infrastructure layer — it provides revenue analytics, capacity modeling, and CRM data quality functions that span the full lifecycle, rather than per-account execution (that's csm/renewals/onboarding/cs-ops). Supporting capability from sales, marketing, customer-support, data, and operations plugins extends into gaps at Stage 4 (expansion selling), Stage 6 (advocacy/content), and Stage 7 (post-churn documentation).

**Outcome & Value Catalog (OCV):** The OCV is not a plugin. It is an artifact produced by `rev-ops:outcome-statement-builder` — a registry of sold outcomes, with evidence quality scoring and value delivery tracking. Skills that need to validate value claims against committed outcomes (primarily `rev-ops:outcome-to-value-tracking`) consume the OCV catalog path stored in the practice profile. The OCV enables the system to distinguish between "we delivered something valuable" and "we delivered the specific outcome the customer paid for."

**Cold start coverage:** All five primary plugins carry a `cold-start-interview` skill variant. When account data is sparse, cold-start produces a profile that seeds downstream skills. Particularly important at Stage 0 and for net-new expansion accounts.

**Managed-agent cookbooks:** A separate `managed-agent-cookbooks` directory contains orchestrated workflows — gtm-pulse-runner, capacity-monitor, churn-signal-scanner, deal-desk-watcher, planning-cycle-orchestrator, and others — for autonomous revenue monitoring at portfolio scope. These are distinct from the rev-ops plugin's individual skills and operate as higher-order compositions built on top of the five-plugin skill catalog.
