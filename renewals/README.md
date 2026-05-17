# Renewals Plugin — Claude for Customer Success

**For:** Renewals managers and AMs owning GRR and NRR in B2B SaaS
**Methodology:** SuccessCOACHING TARO framework + Customer Journey Workflow

---

## What this plugin does

Brings AI-native intelligence to the full renewal cycle: risk assessment, expansion signal detection, renewal forecasting, negotiation prep, price increase planning, churn analysis, and executive renewal summaries.

Every skill reads your configured practice profile — your pricing structure, your discount authority, your churn signals, your escalation chain — so outputs are calibrated to your actual book of business, not a generic renewals template.

---

## Quick start

```bash
/renewals:cold-start-interview
```

Takes 2 minutes for quick start (role + integrations + defaults) or 15 minutes for full setup (adds pricing model, discount authority, churn signal definitions, escalation matrix, renewal portfolio details).

**If this is your first `claude-for-customer-success` plugin install**, cold-start builds the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` — all other plugins read this and skip duplicated questions.

**If you've already run cold-start on another plugin**, cold-start reads the shared profile and skips the company-level questions. Expect ~5 minutes.

---

## Skills

| Skill | What it does | Typical use |
|-------|-------------|-------------|
| `cold-start-interview` | Setup interview — configures your practice profile | First install; re-run with `--redo` to update |
| `renewal-forecast` | Build a weighted renewal forecast with scenario modeling | Monthly/quarterly forecast; pipeline reviews |
| `risk-assessment` | Structured churn risk assessment for a specific account | 90/60/30-day outreach windows; red account review |
| `expansion-signal` | Identify and qualify expansion signals in an account | Pre-renewal; QBR prep; post-adoption milestone |
| `negotiation-prep` | Negotiation brief — positioning, walk-away, objection handling | Before price conversation; contract negotiation |
| `price-increase-prep` | Plan and execute a price increase for an account or cohort | Annual renewals; CPI adjustments; tier migration |
| `churn-analysis` | Root cause analysis of churn or contraction in a closed account | Win/loss review; portfolio retrospective |
| `executive-summary` | Executive-ready renewal summary for a strategic account | CRO/board update; strategic account review |
| `contract-review` | Extract and flag renewal-relevant terms from a contract | Before renewal conversation; redline review |
| `customize` | Update practice profile mid-session | When pricing, portfolio, or team structure changes |

---

## Integrations

This plugin works standalone (manual account context) and gets progressively richer with connected tools.

| Integration | What it unlocks | How to connect |
|-------------|----------------|---------------|
| **CRM** (Salesforce, HubSpot) | Live account data — ARR, renewal dates, opportunity stage, contact history | Cowork: Settings → Connectors / Code: `.mcp.json` |
| **CS Platform** (Gainsight, Totango, ChurnZero, Vitally, Planhat) | Health scores, CTAs, engagement history, usage trends | Same — connector per platform |
| **CPQ** (Salesforce CPQ, DealHub, Conga) | Quote history, pricing tiers, discount history | Same |
| **Contract storage** (DocuSign CLM, Ironclad, Google Drive, SharePoint) | Contract terms, renewal dates, amendments | Same |
| **Call recording** (Gong, Chorus, Clari) | Renewal call transcripts, objection extraction, sentiment | Same |

Skills have graceful fallbacks for every integration — if a connector isn't available, the skill asks you to paste or describe the context instead. No connector is required.

---

## Shared guardrails

These apply to every skill in this plugin and cannot be overridden:

1. **Health scores are heuristics, not verdicts** — show component signals, not a pronouncement on renewal probability
2. **Expansion requires qualification** — tag expansion signals as leads until an economic buyer conversation qualifies them
3. **Renewal forecasts have revenue accounting implications** — flag language that could be read as a committed revenue figure before sharing with finance or leadership
4. **No triage recommendation without an escalation path and owner** — a risk flag names who handles it (AE, Head of CS, CRO) and how they're reached
5. **Account content is confidential customer data** — skills perform a destination check before emitting account ARR, contract terms, or stakeholder names
6. **TARO plays are leads, not mandates** — the renewals manager reads the play recommendation, validates the trigger, and owns execution
7. **No silent data freshness** — every output states the data-as-of timestamp; CRM data older than 7 days triggers a freshness warning

---

## Configuration

Your practice profile lives at:
```
~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md
```

The template in this directory ships with the plugin and is replaced on every update. Do not write user data to it.

**To update your configuration:**
```bash
/renewals:cold-start-interview --redo          # full re-interview
/renewals:cold-start-interview --redo company  # re-do company profile only
/renewals:cold-start-interview --check-integrations  # re-verify what's connected
```

Or edit `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md` directly — it's a plain text file.

---

## Methodology: SuccessCOACHING TARO

Skills reference the SuccessCOACHING TARO framework (Trigger, Action, Resource, Outcome) and the Customer Journey Workflow natively. The `risk-assessment` skill maps account signals to TARO triggers. The `negotiation-prep` skill references your configured playbook sources for counter-messaging and objection handling patterns.

---

## Managed Agents

The renewals plugin hosts one scheduled agent and one on-demand agent.

**Scheduled (runs on a cron cadence):**
- [`renewal-scanner`](../managed-agent-cookbooks/renewal-scanner/) — daily renewal pipeline scan; per-account risk classification 90/60/30 days out; expansion signals

**On-demand (triggered in chat):**
- [`churn-intelligence-agent`](../managed-agent-cookbooks/churn-intelligence/) — signal timeline, churn drivers, exit interview guide, blameless postmortem, learnings, and win-back assessment for a churned or at-risk account

Before deploying the churn-intelligence-agent, run `/renewals:cold-start-interview` to build `renewals/CLAUDE.md` — it is the only managed agent in this plugin that reads a dedicated config file separate from `csm/CLAUDE.md`.

Agent registration files are in [`renewals/agents/`](./agents/). Full cookbook documentation is in [`managed-agent-cookbooks/`](../managed-agent-cookbooks/).

---

## Related plugins

| Plugin | For |
|--------|-----|
| `csm` | Customer Success Managers — account research, call prep, QBRs, health reviews, TARO plays |
| `cs-ops` | CS Operations — health model review, segmentation, capacity planning, playbook audits |
| `onboarding` | Onboarding teams — kickoff prep, onboarding plans, milestone tracking, TtV review |

---

`claude-for-customer-success` v1.0.0 · Renewals plugin
