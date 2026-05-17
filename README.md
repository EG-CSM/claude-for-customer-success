# Claude for Customer Success

A suite of five Claude Code plugins that bring AI-native support to every function in a modern Customer Success and Revenue Operations organization — CSMs, CS Ops, renewals specialists, onboarding teams, and RevOps. Methodology-opinionated (SuccessCOACHING), tool-agnostic.

---

## Plugins

| Plugin | Who it's for | Core skills |
|--------|-------------|-------------|
| [`csm/`](./csm/) | Customer Success Managers — daily account work | Account research, QBR prep, success plans, health review, risk flags, TARO plays |
| [`cs-ops/`](./cs-ops/) | CS Operations — portfolio analytics and systems | Health model review, segmentation, capacity planning, playbook audits, data quality |
| [`renewals/`](./renewals/) | Renewals managers and AMs owning GRR/NRR | Renewal forecasting, expansion signals, churn analysis, negotiation prep, contract review |
| [`onboarding/`](./onboarding/) | Onboarding teams and implementation managers | Kickoff prep, onboarding plans, milestone tracking, TtV review, handoff documentation |
| [`rev-ops/`](./rev-ops/) | RevOps leads, CROs, and CS Ops owning revenue operations | Forecast intelligence, pipeline health, annual planning, CRM quality, deal desk governance |

Each plugin installs independently. Install only what your team needs.

---

## Methodology

This suite is built on the **SuccessCOACHING** methodology — specifically the **TARO framework** (Trigger, Action, Resource, Outcome) and the **Customer Journey Workflow** (Onboarding → Adoption → Value Realization → Renewal/Expansion). Skills reference these frameworks natively.

You don't need prior SuccessCOACHING certification. Cold-start interviews introduce relevant methodology concepts contextually, tied to your actual accounts and tools.

---

## Setup

### First install (any plugin)

Run the cold-start interview in whichever plugin you install first. It will:
1. Build a **shared company profile** at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
2. Configure that plugin's practice profile

Subsequent plugin installs reuse the shared company profile and skip company-level questions (~2 min vs. ~15 min for the full first setup).

```bash
# CSM plugin (most common first install)
/csm:cold-start-interview

# Or any other plugin
/cs-ops:cold-start-interview
/renewals:cold-start-interview
/onboarding:cold-start-interview
/rev-ops:cold-start-interview
```

### Integrations

Each plugin works with whatever you have connected. Cold-start will detect what's available and report which integrations are live. Skills have fallbacks for every integration — no connector required to get value, but connected tools give significantly richer outputs.

**CSM** — CRM (Salesforce, HubSpot, Gainsight), CS Platform (Gainsight, Totango, ChurnZero, Vitally, Planhat), Call recording (Gong, Chorus, Clari)

**CS Ops** — Data warehouse (Snowflake, BigQuery, Redshift), CS Platform, BI (Looker, Tableau, Metabase)

**Renewals** — CRM, CPQ (Salesforce CPQ, DealHub, Conga), Contract storage (DocuSign CLM, Ironclad, Drive/SharePoint)

**Onboarding** — Project management (Asana, Linear, Jira, Monday), CRM

**Rev-Ops** — CRM (HubSpot), Slack, Google Drive, Linear, CS Platform, Zapier

---

## Managed Agent Cookbooks

The [`managed-agent-cookbooks/`](./managed-agent-cookbooks/) directory contains ten agents for teams running Claude as a background workflow engine, plus five rev-ops agents in [`rev-ops/managed-agent-cookbooks/`](./rev-ops/managed-agent-cookbooks/). Six CS suite agents are scheduled headless agents that run autonomously on a cron cadence; four are on-demand agents. All five rev-ops agents support both scheduled and on-demand modes.

### Scheduled agents

| Agent | What it does | Primary plugin |
|-------|-------------|----------------|
| [`health-watcher`](./managed-agent-cookbooks/health-watcher/) | Scans portfolio health daily; routes movement alerts | csm |
| [`churn-signal-digest`](./managed-agent-cookbooks/churn-signal-digest/) | Aggregates cross-source churn signals; P1/P2/P3 digest | csm |
| [`qbr-prep-agent`](./managed-agent-cookbooks/qbr-prep-agent/) | Researches and drafts QBR packages on a schedule or on-demand | csm |
| [`renewal-scanner`](./managed-agent-cookbooks/renewal-scanner/) | Reviews upcoming renewals; risk classification 90/60/30 days out | renewals |
| [`onboarding-milestone-tracker`](./managed-agent-cookbooks/onboarding-milestone-tracker/) | Tracks M1–M5 milestone completion; flags at-risk accounts | onboarding |
| [`portfolio-segment-digest`](./managed-agent-cookbooks/portfolio-segment-digest/) | Segment-level health roll-up; ARR at risk by band; CS Ops / leadership | cs-ops |

### On-demand agents

| Agent | What it does | Primary plugin |
|-------|-------------|----------------|
| [`adoption-motion-agent`](./managed-agent-cookbooks/adoption-motion/) | Feature coverage map, gap diagnosis (6-type taxonomy), TARO play prescription | csm |
| [`expansion-builder-agent`](./managed-agent-cookbooks/expansion-builder/) | Whitespace inventory, business case, AE handoff package | csm |
| [`advocacy-agent`](./managed-agent-cookbooks/advocacy/) | Burnout-protected advocate qualification, ask script or story structure | csm |
| [`churn-intelligence-agent`](./managed-agent-cookbooks/churn-intelligence/) | Signal timeline, churn drivers, exit interview guide, postmortem, win-back assessment | renewals |

### Rev-ops agents (scheduled and on-demand)

| Agent | What it does |
|-------|-------------|
| [`gtm-pulse-runner`](./rev-ops/managed-agent-cookbooks/gtm-pulse-runner/) | Weekly GTM metrics pulse — pipeline, run-rate, velocity, churn signals; five Slack sections with HITL gate |
| [`capacity-monitor`](./rev-ops/managed-agent-cookbooks/capacity-monitor/) | CS capacity headroom vs. closed-won actuals; NRR-adjusted projections; silent-green Slack pattern |
| [`churn-signal-scanner`](./rev-ops/managed-agent-cookbooks/churn-signal-scanner/) | Tier 1/2/3 churn signal scan; Tier-3 triggers Linear escalation with human confirmation |
| [`deal-desk-watcher`](./rev-ops/managed-agent-cookbooks/deal-desk-watcher/) | SLA breach monitor across stage age, approval aging, close date drift, and single-threaded risk |
| [`planning-cycle-orchestrator`](./rev-ops/managed-agent-cookbooks/planning-cycle-orchestrator/) | Five-phase GTM planning cycle with phase-gate governance and Slack digest after every run |

Agent registration files for the CS suite agents live in `csm/agents/` and `renewals/agents/`; rev-ops agent cookbooks live in `rev-ops/managed-agent-cookbooks/`. See each cookbook's `README.md` for deployment instructions and `steering-examples.json` for prompting patterns. Full architecture documentation is in [`managed-agent-cookbooks/README.md`](./managed-agent-cookbooks/README.md).

---

## Shared Guardrails

All five plugins enforce these constraints — they are not optional and cannot be overridden by plugin configuration:

1. **Health scores are heuristics, not verdicts.** Never present a health score as a definitive churn prediction. Surface the signal; the CSM owns the judgment.
2. **Expansion requires qualification.** Flag early-stage expansion signals as leads. Do not present expansion opportunity as confirmed pipeline without sales qualification.
3. **Renewal forecasts have revenue accounting implications.** Language that could be construed as a revenue commitment requires the reviewer to validate before sharing with finance.
4. **No triage recommendation without an escalation path and owner.** A risk flag is not complete unless it names who handles it and how.
5. **Account content is confidential customer data.** Before producing or sending any output containing customer information, check the destination audience.
6. **TARO plays are leads, not mandates.** The CSM reads the play, validates the trigger, and owns the decision to run it. The agent does not run plays autonomously.
7. **No silent data freshness.** Every output that draws on CRM or CSP data surfaces the data-as-of timestamp. Stale data that drives a wrong action is worse than no data.

---

## Architecture Extensions

The 72 skills across these five plugins are built on the standard Claude Code SKILL.md pattern — frontmatter metadata, trigger blocks, instruction body, and guardrails. That baseline is sufficient for a standalone skill. It isn't sufficient for a coordinated suite where 72 skills across 5 plugins need to produce consistent outputs, apply the same domain formulas, enforce the same behavioral constraints, and remain maintainable over time.

A single-skill codebase gets away with embedding domain logic in the skill itself. A 72-skill suite that does that drifts — health score bands defined differently in the CSM health review skill vs. the CS Ops health model review skill, GRR formulas that don't match across renewals and ops, guardrails that exist in some skills but not others. The extensions below solve that problem.

### Shared Domain Model

**File:** [`shared/cs-domain-model.md`](./shared/cs-domain-model.md)

The single authoritative source for every domain constant the suite uses. Skills reference this document rather than defining their own versions of shared concepts.

What it contains:
- Health model score bands (0–100) and the 6-component model (product engagement, business outcomes, relationship strength, support health, adoption breadth, contract health) — with the 14-day staleness threshold and the interpretation rule that forbids presenting a health score as a churn prediction
- Customer segmentation labels (Enterprise / Mid-Market / SMB) aligned to ARR thresholds
- GRR and NRR formulas — exact arithmetic, not approximations
- Renewal forecast pipeline stage weights and the 3-scenario modeling approach (conservative / base / upside)
- Time-to-Value definitions, the pace multiplier formula, and the projected TtV calculation
- Source attribution taxonomy — 8 labels (`[CRM ✓ live]`, `[CS Platform ✓ live]`, `[PM ✓ live]`, `[user provided]`, `[config]`, `[inferred]`, `[stale — N days]`, `[unknown]`) that every skill uses when attributing data in its outputs
- The 7 shared guardrails (G1–G7) in their canonical form

**Why this matters:** When a CSM asks for a health summary and separately asks for a portfolio health review, the two outputs use identical scoring definitions. When a renewals skill calculates NRR and a CS Ops skill audits NRR, they use the same formula. Domain consistency doesn't happen automatically — it requires a single source and explicit references to it.

### Cross-Skill Registry

**File:** [`shared/cross-skill-registry.md`](./shared/cross-skill-registry.md)

A canonical routing table listing all 72 skills with their command format, available modes, and typical trigger conditions. Skills that reference other skills (e.g., a renewal prep skill that hands off to a negotiation skill) point here instead of hardcoding command strings.

**Why this matters:** Hardcoded command strings in SKILL.md files break when skill names change or plugins are reorganized. The registry is the single place to update routing; every skill that references it picks up the change automatically. It also gives contributors and operators a complete map of the suite at a glance.

### Per-Plugin Config Schemas

**Files:** `[plugin]/reference/config-schema.md` (one per plugin)

Structured schemas defining every configuration field each plugin reads from its practice profile — field names, types, valid values, defaults, and required vs. optional status. Skills reference these schemas when reading configuration rather than making assumptions about what fields exist.

**Why this matters:** Cold-start interviews write practice profiles that skills then read. Without a schema, skills guess at field names, handle missing fields inconsistently, and break silently when configuration is incomplete. The schema creates a contract between the interview that writes configuration and the skills that consume it.

### Per-Plugin Token Economics

**Files:** `[plugin]/reference/token-economics.md` (one per plugin)

Per-skill token cost estimates covering prompt construction, tool call overhead, connector data volume, and output generation. Estimates are provided for typical (well-configured), minimal (no connectors), and heavy (large account, full connector stack) usage patterns.

**Why this matters:** Token cost is architecture. A skill that pulls 15 CRM records, 30 days of usage data, and a contract PDF in a single pass can consume 40,000+ tokens. Without visibility into that, operators can't make informed decisions about which skills to run autonomously vs. interactively, or how to scope connector data fetches. Token economics belong in the repository alongside the skills themselves.

### Version Fields

Every SKILL.md frontmatter carries a `version:` field. Version bumps follow semantic versioning conventions: patch for copy fixes, minor for behavior changes, major for breaking changes to inputs or outputs.

**Why this matters:** Plugin update deployments are opaque without versioning. When a skill produces unexpected output, `version:` tells the operator whether they're running the file they think they are. Version history in commit logs correlates with behavior changes across the fleet.

### Reasoning Protocol Sections

Every skill body includes a `## Reasoning Protocol` section — a structured 6-step pre-output checklist the skill runs before generating its response:

1. Confirm activation matches trigger conditions
2. Check connector availability and set fallback path
3. Confirm an escalation path and owner exist before flagging risk
4. Apply the guardrails relevant to this skill's output type
5. Assess output destination (internal CSM use, customer-facing, finance)
6. Confirm mode selection (e.g., research vs. draft vs. update)

Config skills (cold-start interviews and customize commands) run a simplified protocol with no guardrail checks — they don't produce account-level outputs.

**Why this matters:** Guardrail application is the most common failure mode in production CS AI deployments. A skill that "knows" the guardrails in its documentation but doesn't have a structured point in its reasoning to apply them will miss them under pressure — when the question is complex, the data is stale, or the output is destined for finance. The Reasoning Protocol makes guardrail application explicit and auditable. When a skill produces an output that violates G3 (revenue commitment language), the question "did the Reasoning Protocol run step 4?" has a checkable answer.

### How the Extensions Interact

The extensions form a stack. The domain model provides constants and guardrail definitions. The Reasoning Protocol enforces guardrails at output time. The cross-skill registry enables composition without coupling. Config schemas make cold-start configuration machine-readable. Token economics make cost visible before deployment decisions are made. Versioning makes change traceable.

A skill that uses all six extensions: reads domain constants from `shared/cs-domain-model.md` rather than defining its own, applies guardrails through its Reasoning Protocol rather than hoping they're remembered, routes to peer skills through the registry rather than hardcoded commands, reads configuration against a known schema, runs within a documented token budget, and carries a version that can be pinned and audited.

---

## File Locations

```
~/.claude/plugins/config/claude-for-customer-success/
├── company-profile.md          # Shared — all five plugins read this
├── csm/CLAUDE.md               # CSM practice profile (written at cold-start)
├── cs-ops/CLAUDE.md            # CS Ops practice profile
├── renewals/CLAUDE.md          # Renewals practice profile
├── onboarding/CLAUDE.md        # Onboarding practice profile
└── rev-ops/CLAUDE.md           # Rev-Ops practice profile
```

Plugin templates (this directory) ship with the plugin and are replaced on update. User data lives only in `~/.claude/plugins/config/`.

---

## Add-ons

### AUQ Failsafe

**Package:** [`auq-failsafe/`](./auq-failsafe/)

An optional infrastructure add-on that makes `ask_user_input_v0` resilient to render failures. The CS suite plugins use `ask_user_input_v0` extensively — when it works, the user gets an interactive multiple-choice widget; when it fails (unsupported client, missed render, tool error), Claude receives an empty response with no recoverable path.

The `auq-failsafe` plugin installs two Claude Code hooks that detect failures and inject a plain-text multiple-choice fallback so Claude can always proceed. It does not change how AUQ works when it works — it only catches failures.

Installing the plugin is a one-step install. Wiring it into a plugin requires adding two entries to that plugin's `hooks/hooks.json`. All five CS plugins ship with empty hook slots ready to receive the wiring.

See [`auq-failsafe/README.md`](./auq-failsafe/README.md) for install steps and the full T1/T2/T3 protocol.

---

## Version

`claude-for-customer-success` v1.0.0 · Built for Anthropic Claude Code.

Compatible with Claude claude-sonnet-4-6 and claude-opus-4-6.
