# CSM Plugin — Claude for Customer Success

**For:** Customer Success Managers working B2B SaaS accounts
**Methodology:** SuccessCOACHING TARO framework + Customer Journey Workflow

---

## What this plugin does

Brings AI-native assistance to the day-to-day work of a CSM: account research, call prep, QBRs, success plans, health reviews, risk flags, TARO play recommendations, and renewal readiness checks.

Every skill reads your configured company profile — your CS motion, your accounts, your tools, your escalation matrix — so outputs are calibrated to how your team actually works, not a generic CSM template.

---

## Quick start

```bash
/csm:cold-start-interview
```

Takes 2 minutes for quick start (role + integrations + defaults) or 15 minutes for full setup (adds health model config, escalation matrix, playbook sources, account portfolio details).

**If this is your first `claude-for-customer-success` plugin install**, cold-start builds the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` — all other plugins read this and skip duplicated questions.

**If you've already run cold-start on another plugin**, cold-start reads the shared profile and skips the company-level questions. Expect ~5 minutes.

---

## Skills

| Skill | What it does | Typical use |
|-------|-------------|-------------|
| `cold-start-interview` | Setup interview — configures your company profile | First install; re-run with `--redo` to update |
| `account-research` | Multi-source account intelligence before a call | Pre-call, QBR prep, renewal planning |
| `call-prep` | Call brief with agenda, attendee research, suggested talking points | 10 min before any customer call |
| `qbr-builder` | Full QBR deck or narrative — value delivered, metrics, next period plan | Quarterly; exec presentations |
| `success-plan-builder` | Co-authoring a success plan with a customer | Kickoff; mid-lifecycle reset; renewal |
| `stakeholder-map` | Map contacts, roles, influence, and engagement history | Before exec engagement; after reorg |
| `health-score-review` | Interpret health signals and score components for an account | Weekly review; escalation decision |
| `risk-flag` | Structured risk flag for a specific account | When something feels off; before renewal |
| `escalation-memo` | Internal memo routing risk to manager or exec | Confirmed red accounts; churn risk |
| `taro-play-runner` | Recommend and draft a TARO play based on account trigger | Trigger identified; playbook execution |
| `value-statement` | Articulate delivered value in the customer's language | QBR prep; renewal conversation; exec brief |
| `renewal-readiness` | Renewal readiness check — risk, expansion signals, talk track | 90/60/30 days before renewal |
| `customize` | Update company profile mid-session | When account context, tools, or team changes |

---

## Integrations

This plugin works standalone (manual account context) and gets progressively richer with connected tools.

| Integration | What it unlocks | How to connect |
|-------------|----------------|---------------|
| **CRM** (Salesforce, HubSpot) | Live account data — ARR, contacts, opportunity history, contract dates | Cowork: Settings → Connectors / Code: `.mcp.json` |
| **CS Platform** (Gainsight, Totango, ChurnZero, Vitally, Planhat) | Health scores, CTAs, lifecycle stage, usage data | Same — connector per platform |
| **Call recording** (Gong, Chorus, Clari) | Transcript pulls, highlight extraction, call summaries | Same |
| **Document storage** (Google Drive, SharePoint, Box) | Success plans, QBR decks, slide pulls | Same |

Skills have graceful fallbacks for every integration — if a connector isn't available, the skill asks you to paste or describe the context instead. No connector is required.

---

## Shared guardrails

These apply to every skill in this plugin and cannot be overridden:

1. **Health scores are heuristics, not verdicts** — show component signals, not a pronouncement on churn probability
2. **Expansion requires qualification** — tag expansion signals as leads until an economic buyer conversation qualifies them
3. **Renewal forecasts have revenue accounting implications** — flag language that could be read as a revenue commitment
4. **No triage recommendation without an escalation path and owner** — a risk flag names who handles it and how
5. **Account content is confidential customer data** — skills perform a destination check before emitting customer-specific output
6. **TARO plays are leads, not mandates** — the CSM reads the play, validates the trigger, and owns execution
7. **No silent data freshness** — every output states what data it drew on and when that data was last refreshed

---

## Configuration

Your company profile lives at:
```
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md
```

The template in this directory ships with the plugin and is replaced on every update. Do not write user data to it.

**To update your configuration:**
```bash
/csm:cold-start-interview --redo          # full re-interview
/csm:cold-start-interview --redo company  # re-do company profile only
/csm:cold-start-interview --check-integrations  # re-verify what's connected
```

Or edit `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` directly — it's a plain text file.

---

## Methodology: SuccessCOACHING TARO

Skills reference the SuccessCOACHING TARO framework (Trigger, Action, Resource, Outcome) and the Customer Journey Workflow (Onboarding → Adoption → Value Realization → Renewal/Expansion) natively. You don't need prior SuccessCOACHING certification — cold-start surfaces the relevant concepts when they matter.

The `taro-play-runner` skill matches account signals to plays in your configured playbook, drafts the outreach, and routes the play to you for approval. Plays are never executed autonomously.

---

## Managed Agents

The csm plugin is the primary plugin for four scheduled agents and three on-demand agents that run multi-stage pipelines automatically or when triggered by a CSM.

**Scheduled (run on a cron cadence):**
- [`health-watcher`](../managed-agent-cookbooks/health-watcher/) — daily portfolio health scan and movement alerts
- [`churn-signal-digest`](../managed-agent-cookbooks/churn-signal-digest/) — cross-source churn signal aggregation; P1/P2/P3 severity ranking
- [`qbr-prep-agent`](../managed-agent-cookbooks/qbr-prep-agent/) — account research, achievement assessment, narrative draft, and slide outline

**On-demand (CSM-triggered in chat):**
- [`adoption-motion-agent`](../managed-agent-cookbooks/adoption-motion/) — feature coverage map, gap diagnosis, TARO play prescription
- [`expansion-builder-agent`](../managed-agent-cookbooks/expansion-builder/) — whitespace inventory, adoption health gate, business case, AE handoff
- [`advocacy-agent`](../managed-agent-cookbooks/advocacy/) — burnout-protected advocate qualification and advocacy package generation

Agent registration files are in [`csm/agents/`](./agents/). Full cookbook documentation — architecture, configuration, subagent specs, and deployment instructions — is in [`managed-agent-cookbooks/`](../managed-agent-cookbooks/).

---

## Related plugins

| Plugin | For |
|--------|-----|
| `cs-ops` | CS Operations — health model review, segmentation, capacity planning, playbook audits |
| `renewals` | Renewals managers — renewal forecasting, expansion signals, churn analysis, negotiation prep |
| `onboarding` | Onboarding teams — kickoff prep, onboarding plans, milestone tracking, TtV review |

---

`claude-for-customer-success` v1.0.0 · CSM plugin
