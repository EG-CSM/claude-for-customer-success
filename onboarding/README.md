# Onboarding Plugin — Claude for Customer Success

**For:** Onboarding specialists, implementation managers, and CSMs owning the onboarding motion in B2B SaaS
**Methodology:** SuccessCOACHING TARO framework + Customer Journey Workflow

---

## What this plugin does

Brings AI-native assistance to the full onboarding lifecycle: kickoff preparation, onboarding plan creation, success criteria definition, milestone tracking, blocker reviews, time-to-value analysis, and CSM handoff documentation.

Every skill reads your configured practice profile — your onboarding model, your milestone definitions, your TtV targets, your escalation chain — so outputs are calibrated to how your team actually runs onboarding, not a generic implementation template.

---

## Quick start

```bash
/onboarding:cold-start-interview
```

Takes 2 minutes for quick start (role + integrations + defaults) or 15 minutes for full setup (adds milestone framework, success criteria model, graduation criteria, handoff format, escalation matrix, playbook sources).

**If this is your first `claude-for-customer-success` plugin install**, cold-start builds the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` — all other plugins read this and skip duplicated questions.

**If you've already run cold-start on another plugin**, cold-start reads the shared profile and skips the company-level questions. Expect ~5 minutes.

---

## Skills

| Skill | What it does | Typical use |
|-------|-------------|-------------|
| `cold-start-interview` | Setup interview — configures your practice profile | First install; re-run with `--redo` to update |
| `kickoff-prep` | Internal and customer-facing kickoff brief with agenda and attendee research | 24–48 hours before kickoff call |
| `onboarding-plan` | Generate or review a structured onboarding plan with milestones and owners | Kickoff; plan reset; mid-onboarding review |
| `success-criteria-builder` | Co-author account-specific success criteria with observable milestones | Kickoff; when criteria drift or need reset |
| `milestone-tracker` | Status review of milestone completion, at-risk signals, and next actions | Weekly onboarding review; escalation decision |
| `blockers-review` | Structured review of active blockers — type, owner, path to resolution | When progress stalls; pre-escalation |
| `time-to-value-review` | Assess TtV trajectory — on track / at risk / off track — with assumption audit | Mid-onboarding; ahead of milestone gate reviews |
| `handoff-doc` | Generate a CSM handoff document when onboarding graduation criteria are met | Graduation; CSM transition call prep |
| `customize` | Update practice profile mid-session | When account context, milestones, or team changes |

---

## Integrations

This plugin works standalone (manual account context) and gets progressively richer with connected tools.

| Integration | What it unlocks | How to connect |
|-------------|----------------|---------------|
| **Project management** (Asana, Linear, Jira, Monday) | Live milestone status, task completion, blocker tracking | Cowork: Settings → Connectors / Code: `.mcp.json` |
| **CRM** (Salesforce, HubSpot) | Account details, contract dates, stakeholder contacts, AE notes | Same — connector per platform |
| **Document storage** (Google Drive, SharePoint, Box) | Onboarding plans, success criteria docs, kickoff decks | Same |
| **CS Platform** (Gainsight, Totango, ChurnZero, Vitally, Planhat) | Health signals, lifecycle stage, CTA status during onboarding | Same |

Skills have graceful fallbacks for every integration — if a connector isn't available, the skill asks you to paste or describe the context instead. No connector is required.

---

## Shared guardrails

These apply to every skill in this plugin and cannot be overridden:

1. **Health scores are heuristics, not verdicts** — show component signals (milestone completion rate, engagement, blocker count), not a color verdict on onboarding health
2. **Expansion requires qualification** — tag upsell signals discovered during onboarding as early leads; do not surface them in customer-facing onboarding documents without authorization
3. **Renewal forecasts have revenue accounting implications** — flag any onboarding summary language that implies renewal likelihood before sharing with leadership
4. **No triage recommendation without an escalation path and owner** — a risk flag names who handles it (onboarding lead, SE, Head of CS) and how they're reached
5. **Account content is confidential customer data** — skills perform a destination check before emitting account-specific output
6. **TARO plays are leads, not mandates** — the onboarding manager reads the play recommendation, validates the trigger, and owns execution
7. **No silent data freshness** — every output states what data it drew on; project tracker data not confirmed live triggers a freshness warning

---

## Configuration

Your practice profile lives at:
```
~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md
```

The template in this directory ships with the plugin and is replaced on every update. Do not write user data to it.

**To update your configuration:**
```bash
/onboarding:cold-start-interview --redo          # full re-interview
/onboarding:cold-start-interview --redo company  # re-do company profile only
/onboarding:cold-start-interview --check-integrations  # re-verify what's connected
```

Or edit `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md` directly — it's a plain text file.

---

## Methodology: SuccessCOACHING TARO

Skills reference the SuccessCOACHING TARO framework (Trigger, Action, Resource, Outcome) and the Customer Journey Workflow natively. The `milestone-tracker` skill maps milestone completion against the Onboarding stage of the Customer Journey. The `time-to-value-review` skill identifies TARO triggers when TtV trajectory signals risk.

---

## Related plugins

| Plugin | For |
|--------|-----|
| `csm` | Customer Success Managers — account research, call prep, QBRs, health reviews, TARO plays |
| `cs-ops` | CS Operations — health model review, segmentation, capacity planning, playbook audits |
| `renewals` | Renewals managers — renewal forecasting, expansion signals, churn analysis, negotiation prep |

---

`claude-for-customer-success` v1.0.0 · Onboarding plugin
