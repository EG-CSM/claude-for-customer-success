---
name: success-criteria
description: >
  Define, refine, and track onboarding success criteria with the customer. Produces
  a structured success criteria document — typically 3–5 measurable outcomes the
  customer commits to achieving by the end of onboarding. Reads your criteria format,
  review cadence, and methodology from your onboarding profile. Use --define (default)
  to facilitate a criteria definition session from scratch, --refine to adjust existing
  criteria after a scope change, --review to assess current progress against confirmed
  criteria, or --export to produce a clean customer-facing criteria summary without
  internal notes.
argument-hint: "[<account-name-or-ID>] [--define | --refine | --review | --export]"
version: "1.0.0"
deployment_target: plugin
---

# /onboarding:success-criteria

Define and track onboarding success criteria.

---

## Pre-flight

Read both configuration files before running any success criteria work:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- Success criteria format (outcome-based / metric-based / milestone-based — determines
  how criteria are structured and what counts as "confirmed")
- Success criteria review cadence (when to formally review with the customer —
  populates the review schedule section)
- Milestone framework (M4 First value and M5 Handoff ready dates — criteria must map
  to at least one milestone)
- CS methodology (TARO / SuccessCOACHING / Custom — affects language used when
  facilitating the definition session)
- Graduation criteria (what signals the customer is ready to move post-onboarding —
  overlaps with M5 success criteria)

Fields read from company profile:
- Product capability categories (helps anchor criteria to actual product outcomes —
  prevents criteria the product cannot deliver)

If success criteria format is `[PLACEHOLDER]` or missing:
> "Success criteria format isn't configured. Run
> `/onboarding:cold-start-interview --section success-criteria` to set your preferred
> format before facilitating a criteria session. I'll use outcome-based criteria by
> default."

Proceed with outcome-based format as default.

---

## Trigger Precision

**Use when:**
- Defining 3–5 success criteria for a new account at or before kickoff (`--define`)
- Refining existing success criteria after a kickoff call reveals different priorities (`--refine`)
- Reviewing success criteria achievement status at a milestone review or QBR (`--review`)
- Producing a customer-facing success criteria summary for sharing or sign-off (`--export`)

**Do NOT use for:**
- Tracking milestone completion — success criteria and milestones are distinct (use `/onboarding:milestone-tracker`)
- Generating the full onboarding plan (use `/onboarding:onboarding-plan`)
- Handoff graduation readiness checks (use `/onboarding:handoff-doc --readiness`)

**Typical activation:**
- "Define success criteria for [Account]"
- "We need to refine the success criteria after the kickoff call"
- "Review success criteria achievement for [Account]'s QBR"
- "Export the success criteria for [Account] to share with the customer"
- `/onboarding:success-criteria [account] --define`
- `/onboarding:success-criteria [account] --refine`
- `/onboarding:success-criteria [account] --review`
- `/onboarding:success-criteria [account] --export`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of success criteria request is this?
   - **Greenfield Definition**: No existing criteria; starting from scratch with sales context and customer goals. Optimize for customer-anchored discovery and the 3-5 ceiling.
   - **Scope-Triggered Refinement**: Existing criteria need revision due to scope change, stakeholder shift, product capability adjustment, or date shift. Isolate affected criteria; preserve confirmed ones.
   - **Progress Review**: Criteria are confirmed; CSM needs a progress assessment against a milestone checkpoint. Diagnose at-risk criteria, don't just report status.
   - **Customer-Facing Export**: Criteria are confirmed and need clean formatting for the customer. Zero internal labels, flags, or reviewer notes in output.

2. **CONSTRAINTS**: What limits the solution space?
   - G2: Criteria must be confirmed with the customer before driving milestone tracking — CSM-only criteria are hypotheses, not commitments.
   - G4: Each criterion must have a specific observable measure — vague criteria ("team is comfortable") cannot be confirmed as achieved.
   - G5: `--export` is quiet mode — no internal labels, confidence signals, pending-confirmation flags, or reviewer notes reach the customer.
   - G7: Flag any CRM or account data used that is stale relative to the configured staleness threshold — never silently present outdated context as current.
   - Criteria anchor to milestones (M2/M3/M4/M5) — orphaned criteria without a milestone anchor cannot drive review conversations.

3. **EXPERT CHECK**: What would a veteran onboarding CSM verify first?
   - Is the M4 anchor criterion named and concrete? If the single most important Day 30 outcome is missing or vague, the criteria set is misaligned regardless of how polished the other criteria are.
   - Are criteria anchored to what the customer said they wanted (sales echo), or are they CSM projections of what the product can do? Customer words first, CSM judgment second.
   - Is there a confirmation gap? How many criteria are confirmed with the customer vs. pending? Unconfirmed criteria must be flagged, never treated as final.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Drafting criteria from product capabilities instead of customer-stated goals — produces criteria the customer never asked for and won't prioritize.
   - Accepting more than 5 criteria without forcing prioritization — dilutes focus and creates tracking overhead that outlasts onboarding.
   - Reporting at-risk criteria without diagnosing the block type (customer / technical / CSM) — status without diagnosis is not actionable.
   - Revising criteria after a scope change without marking them `[Requires re-confirmation]` — the CSM treats revised criteria as agreed when they are not.
   - Running `--export` on criteria that include unconfirmed items — the customer receives hypotheses presented as commitments.
   - Writing an M4 anchor criterion that is aspirational rather than observable ("customer sees value" instead of "zero manual exports in the last two weeks").

**After execution**, verify:
- Does the output match the mode requested (--define / --refine / --review / --export)?
- Are all criteria anchored to a milestone and confirmable with an observable measure?
- Is the confirmation status explicit for every criterion (confirmed vs. pending)?
- Confidence: [High] if criteria are customer-confirmed with observable measures and milestone anchors / [Medium] if CSM-confirmed but pending customer validation / [Low] if inferred from sales notes without direct customer input — state which.

## Mode

`--define` (default): Facilitate a structured success criteria definition session.
Asks the CSM a sequence of discovery questions designed to elicit 3–5 measurable
outcomes from the customer. Produces a draft criteria document for CSM review before
sharing with the customer.

`--refine`: Revise existing criteria after a scope change, stakeholder change, or
product capability adjustment. Ask what changed and which criteria are affected.
Preserves confirmed criteria and flags revised ones for re-confirmation with the
customer.

`--review`: Assess current progress against previously confirmed criteria. Asks the
CSM for status on each criterion (on track / at risk / achieved). Produces a progress
assessment with confidence signals and recommended actions for at-risk criteria.

`--export`: Customer-facing criteria summary — clean format, no internal labels,
no confidence signals, no at-risk flags. Produces the criteria document ready for
sharing in the customer's preferred format.

---

## Account identification

Ask: "Which account are we defining success criteria for?"

If CRM connector available, pull:
- Account name, segment, and ARR
- Product tier (higher tiers typically unlock capabilities that anchor criteria)
- Industry vertical (calibrates which outcome types are most relevant)
- Sales notes / use cases captured during discovery

Confirm:
> "[CRM]: [account name] · [segment] · [industry] · data as of [timestamp]"

If no CRM: "Tell me the account name, their industry, and the primary use cases they
described during the sales process — that context helps anchor criteria to real
outcomes."

---

## Criteria format reference

### Outcome-based (default)

Each criterion is a stated business outcome the customer will achieve:

```
Criterion: [Customer role/team] will [accomplish X] by [M4/M5 date].
Measure: [How they'll know it happened — observable behavior or artifact]
Owner: [Customer name or role]
```

Example:
```
Criterion: The operations team will process weekly reports using [product] without
           manual data export by M4 (Day 30).
Measure: Zero manual exports in the last two weeks of the M4 period.
Owner: Jordan Smith (Ops Lead)
```

### Metric-based

Each criterion is tied to a quantified target:

```
Criterion: [Metric] will reach [target value] by [date].
Baseline: [Current value if known]
Owner: [Customer name or role]
Data source: [Where this metric lives]
```

### Milestone-based

Each criterion is the completion of a defined deliverable:

```
Criterion: [Deliverable] will be complete by [milestone] ([date]).
Definition of complete: [Specific observable state]
Owner: [Customer name or role]
```

Use the format configured in `../../CLAUDE.md`. If multiple formats fit the
customer's context, note the primary format used.

---

## `--define` mode: Discovery sequence

Facilitate this sequence in order. Each question produces a draft criterion or
eliminates a direction. The goal is 3–5 confirmed criteria — not more.

### Step 1: Anchor to the sales conversation

Ask the CSM:
> "What problem was the customer solving when they bought [product]? What did they say
> they wanted to accomplish in the first 30–60 days?"

Probe for: named use cases, explicit commitments made during sales, any ROI or
time-saving claims the AE made.

Draft 1–2 candidate criteria from this input. Present them and ask: "Do these match
what the customer told you they wanted? Anything to add or adjust?"

### Step 2: Identify the first measurable outcome

Ask:
> "What's the single most important thing that needs to be true at Day 30 for this
> customer to feel like onboarding was worth it?"

This becomes M4 (First value) — the anchor criterion. Every other criterion either
leads to this one or follows from it.

Draft the M4 criterion. Apply the configured criteria format.

### Step 3: Identify the handoff-ready outcome

Ask:
> "What would 'fully onboarded' look like at Day 60? What does the customer need to
> be doing independently before you hand them to your post-onboarding team or reduce
> CSM involvement?"

This becomes the M5 graduation criterion. It must align with the graduation criteria
in the config.

Draft the M5 criterion.

### Step 4: Fill in the gap criteria

Ask:
> "What needs to happen between kickoff and Day 30 for the Day 30 outcome to be
> achievable? Think about technical setup, team training, first workflow completion."

These intermediate criteria map to M2 and M3 milestones. Typically 1–2 criteria per
intermediate milestone. Keep them specific and ownable — vague criteria ("team is
comfortable with the product") are not confirmable.

Draft M2 and M3 criteria.

### Step 5: Confirm the criteria set

Present all drafted criteria as a numbered list:

> "Here's the draft criteria set for [account name]. Before we finalize:
> 1. Can each criterion be confirmed as met — is there a clear observable measure?
> 2. Is each criterion realistic given their team size and bandwidth?
> 3. Are any criteria outside what [product] can deliver in the onboarding window?
> 4. Does the customer know about these criteria, or do we need to confirm them on
>    the next call?"

Revise based on CSM input. Flag any criterion the CSM marks as unconfirmed with the
customer as `[Pending customer confirmation]`.

---

## `--refine` mode

Ask: "What changed? (a) Scope change, (b) stakeholder change, (c) product capability
adjustment, (d) date shift."

For each change type:

**Scope change:** Identify which criteria are affected. Revise the criterion text and
re-evaluate the measure. If the scope expands, add a candidate criterion — don't
stretch an existing one. Mark revised criteria `[Requires re-confirmation with customer]`.

**Stakeholder change:** Update the Owner field. If the new owner was not part of the
original criteria conversation, flag: "New owner [name] may not be aligned on this
criterion — confirm at the next touchpoint."

**Product capability adjustment:** If a criterion references a capability that is
unavailable or delayed, flag: "This criterion may not be achievable within the
onboarding window — recommend revising or replacing it before the next review."

**Date shift:** Recalculate which milestone a criterion maps to based on updated dates.
If a criterion mapped to M4 but M4 shifted past a contractual renewal event, escalate
to the CSM for judgment.

---

## `--review` mode

Ask: "What milestone are we reviewing against? (M2 / M3 / M4 / M5)"

For each confirmed criterion, ask the CSM for status:
- On track: Customer is progressing; no intervention needed
- At risk: Progress exists but the target is in doubt
- Achieved: Criterion is met — provide evidence (artifact, observation, customer statement)
- Blocked: No progress; root cause needed

**At-risk response protocol:**

For each at-risk criterion:
1. Ask: "What's blocking progress?" — surface the root cause
2. Classify the block: customer-side (adoption, bandwidth, priority) / technical
   (integration, configuration) / CSM-side (unclear ask, missing resource)
3. Recommend action:
   - Customer-side: escalation sequence (champion → exec sponsor if white-glove),
     or simplification of the criterion's scope
   - Technical: route to implementation engineer or support
   - CSM-side: name the specific action the CSM should take before the next touchpoint
4. Flag if the at-risk criterion is the M4 or M5 anchor — those are highest priority

Output format for `--review`:

```
Success Criteria Review — [Account Name]
Milestone: [M#] · Target date: [date] · Review date: [today]

[Criterion 1] ✓ Achieved / ⚠ At risk / ● On track / ✗ Blocked
  Evidence / Note: [brief]
  Recommended action: [if at risk or blocked]

[Criterion 2] ...

Summary: [X] of [Y] criteria on track or achieved.
[If any at risk:] Recommended immediate action: [highest-priority action]
```

---

## Output format

### `--define` and `--refine` — internal review version

```
**Success Criteria — [Account Name]**
*Draft — CSM review required before sharing*
*Criteria format: [configured format]*
*Review cadence: [from config]*

---

[Criterion 1]
  Milestone: [M#] · Target date: [date]
  Measure: [observable confirmation]
  Owner: [name/role]
  Status: [Confirmed with customer | Pending customer confirmation]

[Criteria 2–5 in same format]

---

⚠️ Internal notes:
- Unconfirmed criteria: [list or "none"]
- Criteria outside M5 window: [flag or "none"]
- Capability concerns: [any criteria that may exceed product scope]

[Reviewer note]
```

### `--export` output (quiet mode — customer-facing)

```
**[Account Name] — Onboarding Success Criteria**
*Defined: [date] · Owner: [CSM name]*

By the end of onboarding ([M5 date]), we're working toward:

1. [Criterion 1 — outcome statement only, no internal labels]
   How we'll know: [measure]
   Owner: [customer name/role]

2-5. [Same format]

We'll review progress against these criteria at [review cadence].
Questions? [CSM name] · [contact]
```

---

## Reviewer note (internal — `--define`, `--refine`, `--review` only)

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ | manual input | sales notes]
> - **Config fields read:** criteria format ([value]), review cadence ([value]),
>   graduation criteria ([summary])
> - **Criteria count:** [N] defined; [N] confirmed with customer; [N] pending
> - **M4 anchor criterion:** [brief description]
> - **M5 graduation alignment:** [confirmed matches graduation criteria | gap noted]
> - **Capability concerns:** [criteria flagged against product capability | none]
> - **Flagged for your judgment:** [unconfirmed criteria / scope concerns | none]
> - **Before sharing:** Remove internal notes section and this reviewer note.
>   Confirm all criteria have been discussed with the customer, not just the CSM.
>   Replace `[Pending customer confirmation]` markers before the export.

---

## Security & Permissions

This skill operates read-only against configuration files and connected MCP data sources.
No filesystem writes, no subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

Customer-facing outputs (`--export` mode) apply quiet mode — internal confidence signals, reviewer notes, and CSM assessment flags are suppressed.
Success criteria achievement status is based on customer-confirmed evidence only — CSM assumption is explicitly flagged as unverified.
The 3–5 criteria ceiling is enforced — skill will not define more than 5 criteria regardless of input.
CSM review is required before sharing any exported success criteria with the customer.

## Guardrails

**Criteria require customer confirmation.** Success criteria defined only in a CSM
internal session are CSM hypotheses, not confirmed criteria. Every criterion must be
confirmed with the customer contact before it drives milestone tracking. Flag
unconfirmed criteria explicitly — do not treat them as final.

**3–5 criteria maximum.** More than 5 criteria dilutes focus and creates tracking
overhead that outlasts the onboarding period. If the CSM has 8 candidate criteria,
facilitate prioritization — don't output all 8. The 3–5 most important outcomes
are more valuable than a comprehensive list.

**Each criterion must be confirmable.** Vague criteria ("the team is more confident,"
"adoption improves") cannot be confirmed as achieved. Every criterion must have a
specific observable measure. If the CSM cannot name how they'll know a criterion is
met, the criterion needs revision before it's added to the set.

**Criteria anchor to milestones.** Every criterion maps to a specific milestone (M2,
M3, M4, or M5). Criteria that float without a milestone anchor cannot drive review
conversations. If a criterion doesn't fit any milestone, it may belong in the
post-onboarding relationship, not the onboarding plan.

**`--export` is quiet mode.** The customer-facing export contains no internal labels,
confidence signals, "pending confirmation" flags, or reviewer notes. Run `--export`
only after all criteria are confirmed with the customer.

**`--review` is diagnostic — not a report.** The review output is for the CSM's
internal assessment, not for sharing with the customer as-is. At-risk signals and
root cause analysis are internal planning tools. Format for customer communication
separately.

**Capability concerns are a guardrail, not a blocker.** If a criterion references
a capability that is unavailable or unclear, flag it for CSM judgment. Do not silently
remove the criterion — the CSM may know something about product roadmap or workarounds
that makes it valid. Raise the concern; don't resolve it unilaterally.
