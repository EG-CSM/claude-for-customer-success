---
name: cold-start-interview
description: >
  Run the Renewals plugin configuration interview — collects renewal motion,
  book of business details, pricing model, discount authority, churn signal
  definitions, escalation matrix, and integration status to produce the
  renewals practice config file. Runs automatically on first use of any
  renewals skill when config is missing or contains placeholder markers.
  Use --redo to update existing configuration. Use --check-integrations to
  re-verify connector status without re-running the full interview.
argument-hint: "[--full | --quick | --redo | --check-integrations | --redo-company-profile | --section <section-name>]"
version: "1.0.0"
config_skill: true
---

# /renewals:cold-start-interview

Configure the Renewals plugin so every skill runs against your actual book
of business — not generic defaults.

---

## When this runs

This interview runs automatically when any renewals skill detects that
`~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
is missing or contains `[PLACEHOLDER]` markers.

It can also be invoked directly:
- `--full` — Complete 8-section interview (≈15 minutes). Default on first install.
- `--quick` — Role + integrations + key thresholds only (≈2 minutes). Safe for a first pass; skill outputs will ask for context they need.
- `--redo` — Re-run the full interview against an existing configuration; shows current values as defaults.
- `--check-integrations` — Re-verify which connectors are live without touching configuration content.
- `--redo-company-profile` — Re-run company-level questions only; updates shared `company-profile.md`.
- `--section <name>` — Reconfigure one section only. Valid section names: `book`, `pricing`, `churn-signals`, `escalation`, `integrations`, `team`, `methodology`, `communication`.

---

## Pre-flight

Check for `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If the shared company profile exists: read it, then skip Section 1 (Company context)
during the interview — all those questions are answered. Say: "I see you've already
run setup on another plugin. I'll skip the company-level questions and focus on
renewals-specific configuration."

If it doesn't exist: run Section 1 in full and write the shared company profile
when the interview completes.

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of configuration interview request is this?
   - **First-Run Full Configuration**: No existing config file; all 8 sections needed. Optimize for pacing — front-load high-impact sections before fatigue sets in.
   - **Targeted Reconfiguration**: Existing config present; user updating one section via `--section` or `--redo`. Check cross-section dependencies before writing.
   - **Integration Verification**: `--check-integrations` mode; no config content changes, only connector status verification. Distinguish configured vs. verified vs. live.
   - **Quick-Start Bootstrap**: `--quick` mode; minimum viable config to start using skills. Select questions that maximize downstream skill output quality.
   - **Company Profile Update**: `--redo-company-profile` mode; shared company-level questions only. Changes propagate to all plugins, not just renewals.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Never write configuration without explicit user confirmation — config values propagate to every renewals skill output.
   - G2: Discount authority must be bounded — if user claims "unlimited," probe for the practical threshold and log with advisory note if they insist.
   - G4: Escalation matrix entries require all three parts (who, notification method, SLA) — incomplete entries degrade escalation-dependent skills.
   - G5: GRR/NRR targets and ARR figures in configuration carry revenue commitment implications — flag Finance/RevOps review requirement on write.
   - G7: Integration status must distinguish "configured" from "verified" — only mark verified after a successful test call this session.

3. **EXPERT CHECK**: What would a veteran renewals operations lead verify first?
   - Is the interview mode matched to the user's actual need? A user asking for `--full` who has zero integrations may be better served by `--quick` first.
   - Are churn signals specific and measurable, or vague labels? "Low adoption" is not actionable — push for the metric and threshold.
   - Do discount authority, escalation thresholds, and price increase policy form a consistent chain? A 10% discount authority with a 5% escalation trigger is contradictory.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Running all 8 sections in rigid order regardless of user fatigue — offer a save point after Section 3 (book of business).
   - Accepting vague churn signals without probing for specific metrics or thresholds that skills can actually evaluate against.
   - Writing a `--section` update without checking whether the change invalidates values in dependent sections.
   - Marking integrations as "verified" because they appear in the config, without running a live test call.
   - Collecting quick-start answers that skip GRR/NRR targets and churn signals — these are the values most skills need to produce useful output.
   - Displaying proposed configuration in raw markdown instead of readable, section-organized format before confirmation.

**After execution**, verify:
- Does the written configuration contain enough specificity for downstream skills to produce calibrated (not generic) output?
- Are all integration statuses accurately reflecting their actual verification state?
- Is the output mode (full/quick/section/check-integrations) matched to what the user actually needed?
- Confidence: [High] if all sections completed with specific, bounded values / [Medium] if placeholders remain or integration verification incomplete / [Low] if quick-start with majority placeholders — state which and recommend next step.

## Interview — full configuration

Run each section in order, one question at a time. Confirm answers before
advancing to the next section. Display the completed configuration for full
review before writing anything to disk.

---

### Section 1 — Company context
*(Skip if `company-profile.md` already exists)*

1. What's your company name?
2. What does your product do? (2–3 sentences — customers, use case, category)
3. What's your pricing model at a high level? (SaaS subscription / usage-based / flat fee / hybrid)
4. What are the primary verticals or customer segments you serve?

Say after completion: "Great — I'll write this to the shared company profile so you
won't have to answer these questions when setting up the CS-Ops, CSM, or Onboarding plugins."

---

### Section 2 — Who you are and your renewal motion

1. What's your role? (Renewals Manager / Senior Renewals Manager / Account Manager
   owning renewals / CSM with renewal responsibility / Head of Renewals)
2. Who does your renewals team report to? (Head of CS / VP of Revenue / CRO / VP Sales)
3. How are renewals handled at your company?
   - **CSM-led:** The account's CSM owns the renewal end-to-end
   - **Dedicated renewals team:** Separate renewals team takes over at a set point before renewal
   - **AE-led:** Sales AE leads the commercial conversation; CSM supports
   - **Mixed by segment:** Different motion by account tier (e.g., enterprise = dedicated, SMB = CSM-led)
4. What segments do you cover? (SMB / mid-market / enterprise / all)
5. Who is your primary AE partner or co-owner for expansion conversations?
6. Who is your Finance/RevOps contact for revenue recognition and discount approvals?

---

### Section 3 — Book of business

1. What is the total ARR in your book (or your team's book)?
2. How many accounts are in your portfolio?
3. What is the average renewal deal size? (If segmented: by segment)
4. What renewal cycle do most accounts have? (Annual / multi-year / monthly rolling / mixed)
5. When does outreach typically start? (e.g., 90 days before renewal date)
6. When does a decision need to be locked? (e.g., 30 days before renewal date)
7. What are your renewal targets?
   - GRR target: (e.g., 90%)
   - NRR target: (e.g., 110%)
   - Logo retention target: (e.g., 92%)

---

### Section 4 — Pricing and commercial posture

1. What pricing model do you use? (Per seat / usage-based / flat fee / tiered / hybrid)
2. What discount can you approve without escalation? (e.g., up to 10% or up to $X ARR)
3. What triggers an escalation for approval? (e.g., discount >15%, deal >$100K ARR, contract term changes)
4. Who is in the approval chain for exceptions?
   - Standard discount over threshold: [who]
   - Large deal or strategic exception: [who]
   - Contract terms outside standard: [who — Legal / Finance]
5. Do you apply price increases at renewal?
   - If yes: What is the standard increase? (e.g., CPI / flat % / market-rate review)
   - Who approves a price increase and at what threshold?
6. Do you offer multi-year deals? If yes: what is the standard incentive? (e.g., 10% discount for 2-year, 15% for 3-year)

---

### Section 5 — Churn risk signals

1. What are the primary churn drivers at your company? (Look for 3–5 specific signals — e.g., low adoption, exec sponsor departure, unresolved support tickets, budget freeze)
2. Which signals trigger immediate escalation regardless of account size?
   (Examples: non-renewal notice received, executive escalation from customer, NPS <6, competitor evaluation confirmed)
3. Which signals are early warning flags for monitoring (not yet escalation-worthy)?
   (Examples: login drop >30%, champion role change, missed QBR, lack of expansion in year 2)
4. Which competitors do you most commonly lose to at renewal?
5. Is there a health score threshold below which accounts automatically enter a risk workflow?

---

### Section 6 — Escalation matrix

For each situation below, ask: Who handles it, how do they get notified, and what's the expected response time?

| Situation | Questions |
|-----------|-----------|
| Confirmed churn risk (large account) | Route to / How / SLA |
| Discount request above your authority | Route to / How / SLA |
| Price increase pushback (strategic account) | Route to / How / SLA |
| Executive escalation from customer | Route to / How / SLA |
| Contract terms outside standard | Route to / How / SLA |
| Multi-year deal requiring approval | Route to / How / SLA |

Ask: "What ARR threshold defines a 'large account' for escalation purposes?"

---

### Section 7 — Integrations

For each integration, ask: Do you have this connected? (Yes / No / Not sure)
If yes: what is the specific tool? Run a quick connectivity check if a live MCP
connector is available.

| Integration | Tool options | Live check |
|-------------|-------------|------------|
| CRM | Salesforce / HubSpot / other | If connector available: attempt a test call |
| CS Platform | Gainsight / Totango / ChurnZero / Vitally / Planhat / other | Same |
| CPQ | Salesforce CPQ / DealHub / Conga / other | Same |
| Contract storage | DocuSign CLM / Ironclad / Google Drive / SharePoint / other | Same |
| Call recording | Gong / Chorus / Clari / other | Same |

For each connected tool: record the specific platform name. For unconnected tools:
record the fallback (e.g., "will paste contract excerpts").

---

### Section 8 — Methodology and communication preferences

1. Do you follow a formal CS methodology? (SuccessCOACHING TARO / custom playbook / none)
2. Where does your renewal playbook live? (Drive / Notion / CSP / local path / no formal playbook)
3. How do you prefer to communicate renewal risk internally?
   (CRM fields + pipeline review / shared doc narrative / weekly email / Slack update)
4. What format does leadership expect for executive renewal summaries?
   (Slide / memo / dashboard / none currently)
5. What is your standard negotiation posture with customers?
   (Consultative / direct / data-led / segment-dependent)

---

## After all sections — review and write

Before writing anything:

> "Here's the full configuration I'll write to
> `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`.
> Review it and confirm — or tell me what to change."

[Display the complete proposed configuration rendered in readable format — not raw
markdown. Organize by section with headers. Replace unconfigured items with
⚠️ Not answered.]

After confirmation:

1. Write the configuration to `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`.
2. If Section 1 was completed: also write/update `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.
3. Confirm the write with a timestamp.

---

## `--check-integrations` mode

Run a live connectivity check against each integration listed in the configuration
without touching configuration content.

For each integration:
- Attempt a test tool call if a connector is available
- Report: ✅ Connected / ❌ Not reachable / ⚠️ Not configured

Output table:

| Integration | Tool | Status | Last verified |
|-------------|------|--------|---------------|
| CRM | [name] | [✅/❌/⚠️] | [timestamp] |
| CS Platform | [name] | [✅/❌/⚠️] | [timestamp] |
| CPQ | [name] | [✅/❌/⚠️] | [timestamp] |
| Contract storage | [name] | [✅/❌/⚠️] | [timestamp] |
| Call recording | [name] | [✅/❌/⚠️] | [timestamp] |

Update integration status fields in CLAUDE.md after the check. Confirm the update:

> "Integration status updated in your configuration as of [timestamp].
> Re-run `/renewals:cold-start-interview --check-integrations` any time a
> connector is added or credentials change."

---

## `--quick` mode

Condensed interview — collects the minimum required for most skills to produce
useful output. Ask only:

1. Your role?
2. Renewal motion (CSM-led / dedicated team / AE-led / mixed)?
3. Total ARR and account count in your book?
4. GRR and NRR targets?
5. Standard discount authority (what you can approve without escalation)?
6. Top 3 churn signals?
7. Who handles churn escalations?
8. Which integrations are connected? (list all connected tools by name)

Write the configuration with remaining fields as `[PLACEHOLDER]`. Tell the user:

> "Quick-start configuration complete. Skills will give you useful output on your
> book of business now. When a skill needs a value you haven't configured
> (pricing details, escalation SLAs, methodology), it will ask you in-session.
> Run `/renewals:cold-start-interview --redo` any time to fill in the remaining sections."

---

## `--redo-company-profile` mode

Run only Section 1 questions. Display current company profile values as defaults —
user confirms or updates each. Write only to `company-profile.md`. Do not touch
`../../CLAUDE.md`.

---

## `--section <name>` mode

Reconfigure a single section without re-running the full interview. Valid section names:

| Section | Controls |
|---------|----------|
| `book` | ARR, account count, renewal cycle, targets, negotiation window |
| `pricing` | Pricing model, discount authority, escalation thresholds, price increase policy, multi-year terms |
| `churn-signals` | Primary churn drivers, auto-escalate triggers, early warning signals, competitive threats |
| `escalation` | Escalation matrix — situations, routes, SLAs |
| `integrations` | Connected tools and their status |
| `team` | Role, reporting line, AE partner, Finance/RevOps contact |
| `methodology` | CS framework, playbook location, Customer Journey stages |
| `communication` | Internal forecast format, executive summary format, negotiation posture |

Display current values before asking for changes. Confirm before writing.

---

## Configuration write protocol

Every write follows this sequence:

1. Display the proposed configuration section for review.
2. Require explicit confirmation ("Yes / confirm") before writing.
3. Write to `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`.
4. Confirm with timestamp.
5. Surface which skills will behave differently now that configuration is present.

---

## After setup

> ✅ Renewals plugin configured. Your practice profile is live at:
> `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`

Suggested next steps based on what was configured:
- "You have a renewal coming up soon — run a risk assessment: `/renewals:risk-assessment`"
- "Build your renewal forecast: `/renewals:renewal-forecast`"
- "Review an account before a negotiation: `/renewals:negotiation-prep`"
- "Check integration status: `/renewals:cold-start-interview --check-integrations`"
- "Update a specific section later: `/renewals:customize --section <name>`"

---

> [review before sending]

## Guardrails

**Never write without explicit confirmation.** Configuration writes affect every
renewals skill. Show the proposed values, get a yes, then write.

**Validate discount authority is bounded.** If the user says "unlimited" or "no
ceiling," surface this: "Unlimited discount authority typically means approval is
required above a threshold that hasn't been defined. This will affect negotiation-prep
outputs — they'll be unable to flag when a proposed discount exceeds your authority.
Do you want to set a practical ceiling, or should I log this as 'authority is unlimited'?"

**Protect revenue commitment language.** If the user enters GRR/NRR targets and
a large ARR figure, note: "Renewal forecast outputs that project from these figures
will be flagged for Finance/RevOps review before external distribution — this is a
shared guardrail across all renewals skills."

**Integrations that are not verified remain unverified.** If a connector is listed
but `--check-integrations` hasn't been run, mark it as ✓ configured (not ✓ verified).
The distinction matters for sourcing attribution in skill outputs.
