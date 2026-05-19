---
name: handoff-doc
description: >
  Generate the onboarding graduation handoff document — the structured transfer of
  account context from the onboarding CSM to the post-onboarding team (CSM, AE,
  support, or partner). Reads graduation criteria, escalation contacts, and handoff
  format from your onboarding profile. Pulls account history from CRM and PM
  connectors if available. Use --draft (default) to generate the full handoff document,
  --readiness to run a graduation readiness check before generating the document, or
  --summary to produce an abbreviated handoff brief for a verbal or async handoff.
argument-hint: "[<account-name-or-ID>] [--draft | --readiness | --summary]"
version: "1.0.0"
deployment_target: plugin
---

<!-- Status: [PROPOSED] -->

# /onboarding:handoff-doc

Onboarding graduation handoff document.

---

## Pre-flight

Read both configuration files before generating any handoff materials:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- Graduation criteria (the specific conditions that must be met before the handoff
  is valid — these drive the readiness check)
- Onboarding model (affects handoff recipient and document structure — white-glove
  has an executive relationship section; implementation-plus-handoff has a technical
  configuration section; partner-led has a partner context section)
- Milestone framework (M5 Handoff ready criteria and target date)
- Escalation matrix (post-onboarding escalation path — included in the handoff doc
  so the receiving team knows what to do in the first 30 days)
- CS methodology (play references in the "recommended next plays" section)

If graduation criteria are `[PLACEHOLDER]`:
> "Graduation criteria aren't configured. Run
> `/onboarding:cold-start-interview --section handoff` to define graduation criteria
> before generating a handoff document. Without configured criteria, the readiness
> check cannot be run and the document will use generic conditions."

Proceed with generic graduation criteria if confirmed.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Trigger Precision

**Use when:**
- Running a pre-handoff graduation check to confirm the account is ready to transfer (`--readiness`)
- Generating the full onboarding graduation handoff document for the receiving team (`--draft`)
- Producing an abbreviated handoff brief for a verbal or async handoff (`--summary`)

**Do NOT use for:**
- Ongoing milestone tracking during onboarding (use `/onboarding:milestone-tracker`)
- Blocker resolution before the account is ready to graduate (use `/onboarding:blocker-review`)
- Success criteria definition — graduation criteria must be configured before handoff is valid

## Typical Activation
- "Run the graduation readiness check for [Account]"
- "Generate the handoff document for [Account]"
- "I need a quick handoff brief for [Account] for tomorrow's call"
- CSM runs `/onboarding:handoff-doc [account] --readiness` before generating the handoff doc
- CSM runs `/onboarding:handoff-doc [account] --draft` to produce the full graduation handoff document
- CSM runs `/onboarding:handoff-doc [account] --summary` for an abbreviated async handoff brief

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of handoff request is this?
   - **Clean Graduation**: All criteria met, milestones on track, no blockers. Optimize for completeness and receiving-team readability over speed.
   - **Conditional Graduation**: Most criteria met but 1-2 items pending — adoption gaps, incomplete integrations, or unconfirmed success criteria. Focus on open-item ownership and override justification.
   - **Model-Variant Handoff**: Onboarding model (white-glove, implementation-plus-handoff, partner-led) requires model-specific sections. Verify config model and include the correct Section 8 variant.
   - **Summary / Async Handoff**: Full document exists; CSM needs an abbreviated brief. Verify the --draft exists before generating; summary supplements, never replaces.

2. **CONSTRAINTS**: What limits the solution space?
   - G2: Expansion signals are observations for the AE and receiving CSM — describe what was observed, never convert to pipeline commitment or qualification in the handoff document.
   - G4: Post-onboarding escalation path must come from the configured escalation matrix with named owner and channel — no generic "escalate to your manager."
   - G5: Handoff documents contain ARR, contract terms, and health context — confirm the receiving team is authorized before sharing. Flag if distribution extends beyond the named recipients.
   - G7: Flag stale data with source date and staleness indicator — CRM >7 days, PM >3 days. Contact information is the most commonly stale field; always ask CSM to verify.
   - Graduation criteria from config drive the readiness check — if criteria are placeholders, warn before proceeding with generic conditions.

3. **EXPERT CHECK**: What would a veteran onboarding CSM verify first?
   - Were success criteria confirmed by the customer (call notes, email, written acknowledgment), or assumed by the CSM? Customer-confirmed evidence must exist for each "Achieved" criterion.
   - Does every open item in Section 6 have a named owner on the receiving side with a target date? An item owned by the departing onboarding CSM is effectively orphaned.
   - Is the stakeholder map current — have any contacts changed roles during onboarding? Cross-reference CRM records against recent call attendees when call data is available.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Generating --draft without running --readiness first — transfers an account that may not be ready, with no documented graduation check.
   - Marking success criteria "Achieved" based on CSM assumption without customer-confirmed evidence — the receiving team inherits false confidence.
   - Listing open items without named owners — orphaned problems that no one picks up in the first 30 days.
   - Omitting the model-specific Section 8 for white-glove, implementation-plus-handoff, or partner-led accounts — the receiving team misses critical service structure context.
   - Using boilerplate override justification ("business decision") when overriding a HOLD finding — justification must name the unmet criterion, the risk, and the mitigation plan.
   - Generating --summary when no full --draft document exists — the summary becomes the authoritative record by default, losing critical context.

**After execution**, verify:
- Does the handoff document give the receiving team everything they need for their first 30 days — or are there gaps they'll discover only after the onboarding CSM is gone?
- Are all data sources timestamped and staleness-flagged per G7?
- Is the output mode (--draft / --readiness / --summary) matched to the actual need?
- Confidence: [High] if CRM + PM data corroborate and graduation check passed / [Medium] if single-source or partially stale data / [Low] if manual input only — state which.

## Mode

`--readiness` (run before `--draft`): Pre-handoff graduation check. Assesses whether
the account has met all graduation criteria before the document is generated. Produces
a pass/fail assessment per criterion, flags any unmet items, and recommends whether
to proceed with handoff or address remaining gaps first. Use this to avoid handing
off an account that isn't actually ready.

`--draft` (default): Full handoff document. Generates the complete account context
transfer — milestone history, success criteria achievement status, stakeholder map,
technical configuration, relationship notes, open items, and recommended next plays
for the receiving team. Requires the graduation readiness check to pass (or CSM
override with documented justification).

`--summary`: Abbreviated handoff brief — 1–2 page overview for verbal or async
handoffs. Covers only the most critical context: who the account is, what they
achieved in onboarding, who owns what now, and what the receiving team needs to do
in their first 30 days. Use when the full document exists but the receiving CSM needs
a quick-read version.

---

## Account identification and data pull

Ask: "Which account is graduating? Provide the account name and the handoff date
(when the receiving team takes ownership)."

If CRM connector available, pull:
- Account name, segment, ARR, and product tier
- Contract dates, renewal date, and any expansion flags
- All stakeholder records: executive sponsor, champion, technical lead, billing contact
- Account history notes and activity log (last 90 days)
- AE name and any pipeline notes related to the account

If PM connector available, pull:
- Milestone completion dates (M1–M5)
- Open tasks or incomplete items at handoff
- Blocker log (if recorded during onboarding)

Confirm:
> "[CRM]: [account name] · [segment] · ARR: [value] · renewal: [date] · data as of
> [timestamp]"
> "[PM]: M1–M5 completion dates retrieved · [N] open items at handoff · data as of
> [timestamp]"

If neither connector: "Provide the account name, key stakeholders, milestone completion
dates, and any open items — I'll build the handoff document from your input."

---

## `--readiness` mode: Graduation check

Run before generating the handoff document. Check each graduation criterion from config:

Present as a checklist:

```
Graduation Readiness — [Account Name]
M5 target date: [date] · Readiness check date: [today]

Graduation Criteria:

[ ] M5 milestone complete — all completion criteria met
[ ] Success criteria confirmed — customer has acknowledged achievement in writing
    or on a call (not assumed by CSM)
[ ] All provisioned users have logged in at least once
[ ] Integration(s) active and validated
[ ] Customer has named their post-onboarding point of contact
[ ] Open items from onboarding are documented and ownership transferred
[ ] Receiving team has been introduced to the customer or has a scheduled intro call
[ ] Executive sponsor has been updated (if white-glove model)
[ ] Implementation handoff complete (if implementation-plus-handoff model)
[ ] Partner alignment confirmed (if partner-led model)

Overall: [PASS — ready to generate handoff doc | CONDITIONAL PASS — [N] items
pending, see recommendations | HOLD — graduation criteria not met]
```

If HOLD or CONDITIONAL PASS:
> "The account is not yet ready for handoff. Unmet criteria:
> - [criterion 1] — recommended action: [action]
> - [criterion 2] — recommended action: [action]
>
> If you need to proceed despite unmet criteria, document the justification and I'll
> include it in the handoff document as an open item for the receiving team."

---

## Handoff document structure

### Section 1 — Account summary

```
Account: [name]
Segment: [segment] · ARR: [value] · Product tier: [tier]
Contract start: [date] · Renewal: [date]
Onboarding model: [model]
Onboarding CSM: [name] · Receiving team: [name(s)]
Handoff date: [date]
```

### Section 2 — Onboarding performance summary

Milestone history:

| Milestone | Target date | Actual date | Variance | Notes |
|-----------|-------------|-------------|----------|-------|
| M1: Kickoff | [date] | [date] | [±N days] | [any notable context] |
| M2: Tech setup | [date] | [date] | [±N days] | |
| M3: First use | [date] | [date] | [±N days] | |
| M4: First value | [date] | [date] | [±N days] | |
| M5: Handoff ready | [date] | [date] | [±N days] | |

Blockers encountered during onboarding (from blocker log or CSM input):
- [Blocker type]: [brief description] · Resolved [date] · Days lost: [N]
- (If none: "No significant blockers recorded during onboarding.")

### Section 3 — Success criteria achievement

For each confirmed success criterion:

```
Criterion: [criterion statement]
Status: ✓ Achieved / ◐ Partially achieved / ○ Not achieved
Evidence: [what the CSM observed or the customer confirmed]
Owner during onboarding: [customer name/role]
Post-onboarding owner: [who maintains this outcome going forward]
```

If any criterion was not achieved:
> "⚠ Criterion [X] was not fully achieved. Recommended action for the receiving team:
> [specific next step — do not leave unachieved criteria without a recommended path]."

### Section 4 — Stakeholder map

| Role | Name | Contact | Engagement level | Notes |
|------|------|---------|-----------------|-------|
| Executive sponsor | [name] | [email/Slack] | [high/medium/low] | [engagement notes] |
| Champion | [name] | [contact] | [level] | [notes] |
| Technical lead | [name] | [contact] | [level] | [notes] |
| Day-to-day contact | [name] | [contact] | [level] | [notes] |
| Billing contact | [name] | [contact] | — | [notes] |

Relationship notes: [Any relationship dynamics the receiving team should know — exec
relationship quality, political sensitivities, communication preferences, preferred
meeting format]

### Section 5 — Technical configuration

Integration and technical setup:

| Integration / configuration | Status | Owner | Notes |
|----------------------------|--------|-------|-------|
| [Integration 1] | Active | [technical lead] | [any quirks or custom config] |
| [Integration 2] | Active / Pending | | |

User provisioning:
- Total provisioned users: [N]
- Active users (logged in at least once): [N]
- Teams / departments configured: [list]

Support history: [open tickets at handoff, if any · ticket # and status]

### Section 6 — Open items at handoff

Items not fully resolved at graduation, transferred to the receiving team:

| Item | Type | Priority | Owner | Target resolution |
|------|------|----------|-------|------------------|
| [item] | [technical/adoption/relationship] | [P1-P4] | [receiving team member] | [date] |

If no open items: "No open items transferred. Account graduated clean."

### Section 7 — Recommended plays for the receiving team

Based on the account's onboarding history and CS methodology from config, recommend
2–3 specific next plays or actions for the receiving team's first 30 days:

1. [Play or action — specific, not generic]: [why this account needs this next]
2. [Play or action]
3. [If applicable]

Renewal context (if available from CRM):
- Renewal date: [date]
- Expansion signals from onboarding: [any upsell indicators observed — new use cases
  mentioned, additional team requests, feature asks]
- Risk flags: [any concerns the receiving team should monitor]

### Section 8 — Model-specific sections

**white-glove only:**
> "Executive relationship: The executive sponsor is [name]. Engagement during
> onboarding was [high/medium/low]. Preferred communication format: [email/quarterly
> call/Slack]. Last executive touchpoint: [date]. The [receiving role] should
> schedule an executive introduction call within 30 days of handoff."

**implementation-plus-handoff only:**
> "Implementation handoff complete: [date]. The implementation engineer ([name])
> is available for technical questions for [N] days post-handoff per the
> implementation agreement. Escalation path for technical issues post-handoff:
> [support / implementation engineer / CSM]."

**partner-led only:**
> "Partner: [partner name] · Partner contact: [name, contact]. The partner's
> ongoing role post-onboarding: [scope]. Escalation path if customer contacts
> company directly: [path]. Partner relationship quality: [strong/stable/needs
> attention — brief note]."

---

## `--summary` output (quiet mode — for verbal or async handoffs)

```
**[Account Name] — Handoff Brief**
*Handoff: [date] · From: [onboarding CSM] · To: [receiving team]*

**Who they are:**
[2–3 sentences: segment, industry, primary use case, why they bought]

**What they achieved:**
[Success criteria met — 2–3 key outcomes in plain language]

**Who to know:**
[Champion name, executive sponsor if applicable, technical lead — one line each]

**What to watch:**
[Top 1–2 risk flags or open items the receiving team should address first]

**First 30 days:**
[2–3 specific recommended actions — numbered list]

**Renewal context:**
[Renewal date] · [Expansion signals if any] · [Risk level: low/medium/high]

Questions about this account: [onboarding CSM name] · [contact]
```

---

## Reviewer note (internal — `--draft` and `--readiness` only)

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ | PM ✓ | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** graduation criteria ([list]), onboarding model ([value]),
>   escalation matrix ([post-onboarding contacts])
> - **Graduation check:** [PASS / CONDITIONAL PASS — [N] items / HOLD — override
>   documented]
> - **Success criteria status:** [N] of [N] achieved; [N] partially achieved;
>   [N] not achieved
> - **Open items transferred:** [N] — see Section 6
> - **Expansion signals noted:** [yes — see Section 7 | none]
> - **Flagged for your judgment:** [unmet criteria with no recommended path / missing
>   stakeholder contacts / technical open items without an owner | none]
> - **Before sharing with receiving team:** Confirm receiving team contact names are
>   current. Verify renewal date from CRM — do not rely on onboarding plan date.
>   Ensure open items in Section 6 have owners assigned.

---

## Output

Onboarding handoff output — format driven by flag (`--draft`, `--readiness`,
`--summary`). Draft mode: full structured handoff document. Readiness mode:
graduation checklist with go/no-go recommendation. Summary mode: concise async
handoff note. See mode-specific sections for field-level structure.

> [review before sending]

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill

---

## Security & Permissions

This skill operates read-only against configuration files and connected MCP data sources.
No filesystem writes, no subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

Handoff documents contain ARR, contract terms, and health context — confirm receiving team is authorized before sharing (per G5).
All CRM and PM data is timestamped and staleness-flagged per G7 (CRM >7 days, PM >3 days).
Expansion signals in handoff documents are observations only — never converted to pipeline commitment.
Graduation criteria are driven by configured values, not assumed by the skill — placeholder criteria produce a warning before proceeding.

## Guardrails

**Run `--readiness` before `--draft`.** A handoff document generated before the
graduation check has passed may transfer an account that isn't ready. The readiness
check is the gate — not an optional step. If the CSM overrides a HOLD finding, the
justification must be documented in Section 6 as an open item.

**Unachieved success criteria require a forward path.** A success criterion marked
"Not achieved" cannot be silently dropped from the handoff document. It must appear
in Section 3 with a recommended action for the receiving team. Unachieved criteria
without a forward path leave the receiving team without context and the customer
without resolution.

**Stakeholder contacts must be verified.** Contact information pulled from CRM may
be outdated — people change roles. Ask the CSM: "Are all stakeholder contacts
current? Any role changes since kickoff?" Flag unverified contacts in the reviewer note.

**Open items require owners before handoff.** An open item without an owner is an
orphaned problem. Every item in Section 6 must have a named owner — either from
the receiving team or from the customer side. The onboarding CSM should not be
named as owner on items that transfer to the receiving team.

**`--summary` is a supplement — not a replacement.** The handoff brief is for
quick consumption, not the authoritative record. The full `--draft` document
should exist and be accessible to the receiving team even when the summary is used
for the verbal handoff call.

**Expansion signals are observations — not pipeline.** Noting an expansion signal
in the handoff document is appropriate context. Converting it to pipeline commitment
in the handoff document is not — that is the AE's and receiving CSM's job after
reviewing the context. Describe what was observed; do not qualify it.
