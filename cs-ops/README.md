# CS-Ops Plugin — Claude for Customer Success

**For:** Customer Success Operations teams managing B2B SaaS portfolios
**Methodology:** SuccessCOACHING TARO framework + Customer Journey Workflow

---

## What this plugin does

Brings AI-native analytics and operational intelligence to CS Ops work: portfolio health analysis, segmentation modeling, capacity planning, playbook auditing, data quality checks, and metric dashboard specs.

Every skill reads your configured practice profile — your data warehouse, your health model weights, your segmentation tiers, your playbook inventory — so outputs reflect your actual portfolio structure, not a generic CS Ops template.

---

## Quick start

```bash
/cs-ops:cold-start-interview
```

Takes 2 minutes for quick start (role + data stack + defaults) or 15 minutes for full setup (adds health model config, segmentation model, capacity benchmarks, playbook inventory, reporting cadences).

**If this is your first `claude-for-customer-success` plugin install**, cold-start builds the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` — all other plugins read this and skip duplicated questions.

**If you've already run cold-start on another plugin**, cold-start reads the shared profile and skips the company-level questions. Expect ~5 minutes.

---

## Skills

| Skill | What it does | Typical use |
|-------|-------------|-------------|
| `cold-start-interview` | Setup interview — configures your practice profile | First install; re-run with `--redo` to update |
| `health-model-review` | Audit health model components, weights, and signal coverage | Quarterly health model calibration; board prep |
| `segment-analyzer` | Analyze portfolio health and risk distribution by segment | Weekly/monthly segment review; leadership reporting |
| `capacity-planner` | Model CSM capacity against book of business; surface overload risk | Headcount planning; reorg scenarios |
| `playbook-auditor` | Review playbook library for coverage gaps, stale plays, and execution frequency | Quarterly playbook review; methodology audit |
| `data-quality-check` | Identify data quality issues in CRM, CSP, or warehouse exports | Before board reporting; after system migration |
| `metric-dashboard` | Spec or interpret a portfolio metrics dashboard | Leadership reporting; QBR prep; investor materials |
| `process-doc` | Document or audit a CS Ops process — workflow, ownership, cadences | Process improvement; team onboarding; SOC audit |
| `customize` | Update practice profile mid-session | When data stack, team structure, or segments change |

---

## Integrations

This plugin works standalone (uploaded exports or pasted data) and gets progressively richer with connected tools.

| Integration | What it unlocks | How to connect |
|-------------|----------------|---------------|
| **Data warehouse** (Snowflake, BigQuery, Redshift, Databricks) | Live portfolio queries — usage, health trends, cohort analysis | Cowork: Settings → Connectors / Code: `.mcp.json` |
| **CS Platform** (Gainsight, Totango, ChurnZero, Vitally, Planhat) | Health scores, CTA queues, lifecycle distribution, segment counts | Same — connector per platform |
| **CRM** (Salesforce, HubSpot) | Account list, ARR, renewal dates, CSM assignments | Same |
| **BI tool** (Looker, Tableau, Metabase, Power BI) | Dashboard data pulls, chart interpretation | Same |

Skills have graceful fallbacks for every integration — if a connector isn't available, the skill asks you to paste or describe the data instead. No connector is required.

---

## Shared guardrails

These apply to every skill in this plugin and cannot be overridden:

1. **Health scores are heuristics, not verdicts** — show component signals and weights, not a pronouncement on churn probability
2. **Expansion requires qualification** — tag expansion signals as leads until a qualifying sales conversation occurs at the account level
3. **Renewal forecasts have revenue accounting implications** — flag language that could be read as a revenue commitment before board or investor distribution
4. **No triage recommendation without an escalation path and owner** — a portfolio risk flag names who handles it and how
5. **Portfolio analytics contain confidential customer data** — skills perform a destination check before emitting account-level output
6. **TARO plays are leads, not mandates** — CS Ops routes play recommendations to CSMs; CS Ops does not execute plays autonomously
7. **No silent data freshness** — every output states the data-as-of timestamp; stale data (>14 days) is flagged prominently

---

## Configuration

Your practice profile lives at:
```
~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md
```

The template in this directory ships with the plugin and is replaced on every update. Do not write user data to it.

**To update your configuration:**
```bash
/cs-ops:cold-start-interview --redo          # full re-interview
/cs-ops:cold-start-interview --redo company  # re-do company profile only
/cs-ops:cold-start-interview --check-integrations  # re-verify what's connected
```

Or edit `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md` directly — it's a plain text file.

---

## Methodology: SuccessCOACHING TARO

Skills reference the SuccessCOACHING TARO framework (Trigger, Action, Resource, Outcome) and the Customer Journey Workflow (Onboarding → Adoption → Value Realization → Renewal/Expansion) natively. The `playbook-auditor` skill maps your playbook inventory against the TARO library to surface coverage gaps. The `segment-analyzer` skill aligns segment health reporting to lifecycle stages.

---

## Related plugins

| Plugin | For |
|--------|-----|
| `csm` | Customer Success Managers — account research, call prep, QBRs, health reviews, TARO plays |
| `renewals` | Renewals managers — renewal forecasting, expansion signals, churn analysis, negotiation prep |
| `onboarding` | Onboarding teams — kickoff prep, onboarding plans, milestone tracking, TtV review |

---

`claude-for-customer-success` v1.0.0 · CS-Ops plugin
