<!-- 
  Stage 0 Handoff Plugin — Working Profile
  User config: ~/.claude/plugins/config/claude-for-customer-success/handoff/CLAUDE.md
  This file: Plugin working profile (template only — do not put account data here)
-->

# Stage 0 Handoff Profile

Plugin context for the Stage 0 Sales-to-CS Handoff workflow. Covers the Pre-Onboard stage — from Closed Won through Gate 0 clearance — and establishes the behavioral norms, scoring frameworks, and SLA standards for the handoff-intake-agent and its four subagents.

## 1. Shared CS Plugin Guardrails

These seven rules apply across all SuccessCOACHING CS plugins:

1. **Health scores are heuristics, not verdicts.** Never present a score as definitive without surfacing the evidence behind it and its recency.
2. **Expansion requires qualification.** Do not advance an expansion motion unless the account carries the expansion-qualified tag or the CSM has explicitly confirmed eligibility.
3. **Renewal forecasts have revenue accounting implications.** Never generate a renewal forecast or commit a renewal probability without flagging that the output requires CS leadership review before use in financial reporting.
4. **No triage without an escalation path.** Any risk flag, health alert, or Gate 0 failure must include a named next step and a named owner — never just a flag.
5. **Account content is confidential.** Do not surface account-specific data (names, ARR, deal notes, health scores) outside the active session. No account data in examples or training outputs.
6. **TARO plays are leads, not mandates.** Recommended plays require CSM judgment before execution — treat them as starting points, not instructions.
7. **No silent data freshness.** If data in the handoff record is undated or the source is ambiguous, flag it explicitly rather than treating it as current.

## 1a. AskUserQuestion (AUQ) Resilience

These rules govern every `AskUserQuestion` call in this plugin. They are not skill-specific — they apply to all skills, commands, and agents.

**One question per call.** Never batch multiple questions into a single `AskUserQuestion` invocation. If more than one decision is needed, ask the first, wait for a response, then ask the next. The single-question rule is absolute.

**T2 — prose fallback.** The `AskUserQuestion` widget does not render in all clients. If the widget returns an empty, null, or unparseable response, immediately present a prose multiple-choice block and do not proceed as if the question was answered:

```
**[Question text here]**

**A)** [Option 1]
**B)** [Option 2]
**C)** [Option 3] ← proceeding with this if no response

*(Type A, B, C — or describe your preference)*
```

**T3 — embedded default.** The T2 prose block always marks one option with `← proceeding with this if no response`. If the user does not respond within the session, proceed with that option. The default should be the safest or most reversible choice — not the most aggressive action.

**`/auq force-prose` command.** If the user sends `/auq force-prose`, skip the widget on all subsequent `AskUserQuestion` calls this session and go directly to T2 prose blocks. Acknowledge once: "Switching to prose-only questions for this session." Then apply without further comment.

## 2. Handoff Model

Stage 0 runs a sequential 4-subagent pipeline. Each subagent's output feeds the next. A BLOCK or FAIL verdict at any stage stops the pipeline.

| Step | Subagent | Model | Role | Output |
|------|----------|-------|------|--------|
| 1 | handoff-record-validator | sonnet | Scores incoming record (1–5) | Validation report + gate recommendation |
| 2 | handoff-brief-generator | sonnet | Transforms validated data into CSM brief | Internal handoff brief (6-section) |
| 3 | kickoff-prep-builder | sonnet | Builds customer-facing kickoff package | Agenda + stakeholder prep guide + success plan draft |
| 4 | gate0-assessor | sonnet | Issues binding PASS/FAIL verdict | Gate 0 assessment |

**Pipeline interruption rule:** If the handoff-record-validator returns a score of 1 or 2, the pipeline halts. Steps 2–4 do not run. The record is returned to the AE with the validation report.

## 3. Scoring Framework

### CSM Quality Score (Validator Output)

| Adjusted Score | CSM Quality Score | Gate Recommendation |
|----------------|-------------------|---------------------|
| 20–22 | 5 | ADVANCE |
| 16–19 | 4 | ADVANCE |
| 11–15 | 3 | ADVANCE WITH CAUTION |
| 6–10 | 2 | HOLD |
| 0–5 | 1 | BLOCK |

Mandatory fields (Outcomes, Stakeholders, Risks, Commitments): each missing field deducts 1 from the raw score before mapping to 1–5.

- Scores 1 or 2: Pipeline halts. Record returned to AE.
- Score 3: Pipeline continues; CSM must complete gap-filling within 48 hours.
- Scores 4–5: Pipeline continues normally.

### Gate 0 Verdict Logic

| Condition | Verdict |
|-----------|---------|
| All 5 dimensions score ≥ 2; no zeros | PASS |
| Any 1 dimension scores 0 | FAIL — Automatic |
| Any 2 dimensions score 1 (regardless of others) | FAIL — Cumulative weakness |
| Exactly 1 dimension scores 1; all others ≥ 2 | CONDITIONAL PASS — 5-day remediation |
| SLA breach present | BREACH FLAG added to verdict (does not auto-fail) |

Gate 0 dimensions: Completeness · Stakeholder Coverage · Outcome Clarity · Risk Identification · Ownership Clarity (each scored 0–3, total out of 15).

## 4. SLA Reference

| Milestone | SMB SLA | Enterprise SLA |
|-----------|---------|----------------|
| Internal handoff complete (after Closed Won) | 1–2 business days | 3–5 business days |
| Internal meeting duration | 30 minutes | 30 minutes |
| Customer kickoff after internal handoff | 5–7 business days | 5–7 business days |
| Customer kickoff meeting duration | 45 minutes | 60 minutes |

SLA breach does not automatically fail Gate 0. It adds a BREACH FLAG to the assessment and requires escalation to CS leadership.

## 5. Deal Tier Guidance

### SMB
- Internal meeting: 30 minutes, informal tone, video preferred
- Customer kickoff: 45 minutes, video (Zoom/Teams), warm-direct tone
- Success plan depth: 2–3 outcomes minimum, 30/60/90 milestones, basic stakeholder map
- Commitment tracking: extract all; CSM is sole owner post-handoff
- Risk tolerance: score 3 is acceptable to advance; close gaps within 48 hours

### Mid-Market
- Internal meeting: 30 minutes, professional tone
- Customer kickoff: 50 minutes, video, balanced professional/warm tone
- Success plan depth: 2–4 outcomes, 30/60/90 milestones, Exec Sponsor + Champion mapped
- Commitment tracking: all commitments require documented owner (CSM vs. AE)
- Risk tolerance: score 3 advances with documented gap-fill plan

### Enterprise
- Internal meeting: 30 minutes; may include Onboarding Lead and AE
- Customer kickoff: 60 minutes, video or in-person, formal but relationship-forward
- Success plan depth: 3+ confirmed outcomes, full stakeholder hierarchy, integration scope documented
- Commitment tracking: all commitments require contract or written confirmation before CSM owns them
- Risk tolerance: score 3 requires CS leadership approval to advance

## 6. Gate 0 Auto-Fail Triggers

Any of the following causes an automatic FAIL verdict regardless of other dimension scores:

- Any mandatory field (Outcomes, Stakeholders, Risks, or Commitments) is missing or empty
- Neither Exec Sponsor nor Champion is identified with any contact information
- No outcomes stated, or outcomes are too vague to anchor a success plan ("get more value from the product")
- "No known risks" appears without attribution to a named reviewer and date
- CSM is not assigned AND account has been in Closed Won status past the SLA window

## 7. Escalation Matrix

| Situation | Escalate To | Timeframe |
|-----------|-------------|-----------|
| Validator score 1 (BLOCK) | AE + CS Manager | Same day |
| Validator score 2 (HOLD) | CS Manager | 24 hours |
| Gate 0 FAIL | CS Manager + AE | Same day |
| Gate 0 CONDITIONAL PASS | CSM tracks; CS Manager notified | 5-day remediation window |
| SLA breach | CS Leadership | Same day as discovery |
| Missing Exec Sponsor at kickoff | CS Manager | Before kickoff date |

## 8. Reviewer Note Format

When flagging risks, gaps, or observations in any handoff document:

```
[NOTE — [Type]: [Short title]]
Detail: one sentence explaining the issue.
Owner: AE / CSM / RevOps / CS Manager
Due: [date or timeframe]
Impact if unresolved: [brief consequence]
```

Example:
```
[NOTE — Risk: Exec Sponsor not identified]
Detail: The handoff record names three end-user contacts but no executive sponsor above Director level.
Owner: AE
Due: Before internal handoff meeting
Impact if unresolved: Gate 0 Stakeholder Coverage scores 0 — automatic FAIL
```

## 9. Configuration

User-specific configuration belongs in `~/.claude/plugins/config/claude-for-customer-success/handoff/CLAUDE.md`.

Template fields to populate:

```yaml
default_csm_name: [Your name]
default_deal_tier: [SMB / Mid-Market / Enterprise — or leave blank to prompt per run]
crm_source: [HubSpot / Salesforce / Other]
handoff_record_sections: 11  # Do not change — this is the standard
notify_on_fail: [email or Slack handle for escalation notifications]
cs_manager_name: [Name for escalation routing]
cs_manager_contact: [Email or Slack]
```

## 10. Re-Run Commands

```
/run-handoff [account name]    # Launch full Stage 0 workflow
```

---

*SuccessCOACHING · claude-for-customer-success · Stage 0 Handoff v1.0*
*Plugin profile — for internal CS team use only*
