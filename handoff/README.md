# Handoff — Stage 0 Sales-to-CS Handoff Plugin

Automates the complete Stage 0 Sales-to-CS Handoff workflow for the SuccessCOACHING Customer Lifecycle. Validates incoming accounts, generates internal meeting materials, builds customer-facing kickoff packages, and runs the Gate 0 quality assessment before advancing an account to Stage 1 Onboarding.

---

## What This Plugin Does

When a deal closes, the handoff from Sales to Customer Success is one of the highest-risk moments in the customer lifecycle. Poor handoffs produce misaligned expectations, missing stakeholder relationships, undocumented commitments, and early churn signals. This plugin operationalizes the SuccessCOACHING Stage 0 standard so that every new account goes through a consistent, documented process before onboarding begins.

The plugin orchestrates four specialist agents in sequence:

1. **Validate** — Score the incoming handoff record against the 11-section standard and 4 mandatory fields
2. **Brief** — Generate the internal CS brief for the 30-minute internal handoff meeting
3. **Kickoff** — Build the customer-facing kickoff package (agenda, stakeholder prep guide, success plan draft)
4. **Gate 0** — Run the quality assessment and issue a binding PASS / CONDITIONAL PASS / FAIL verdict

A passing account exits Stage 0 with a complete internal brief, a customer-ready kickoff package, a success plan skeleton, and a documented quality gate clearance.

---

## Quick Start

```
/run-handoff [account name]
```

Have the following ready before running:

- Account name and deal tier (SMB / Mid-Market / Enterprise)
- Closed Won date
- Handoff record content (paste, upload, or describe)
- Assigned CSM name (or "TBD")

---

## Agents

### `handoff-intake-agent` (Orchestrator)

The primary agent. Manages the end-to-end Stage 0 workflow, dispatches subagents in sequence, and delivers the complete output package. Start here — the orchestrator runs everything else.

### `handoff-record-validator` (Subagent)

Scores the incoming handoff record section by section against the 11-section standard. Calculates a CSM Quality Score (1–5) and issues a gate recommendation (ADVANCE / ADVANCE WITH CAUTION / HOLD / BLOCK). A score of 1 or 2 returns the record to the AE before any downstream work begins.

**Scoring framework:**
- 11 sections scored 0 (Missing) / 1 (Incomplete) / 2 (Complete) — max raw score: 22
- Each missing mandatory field deducts 1 from the raw score
- Mapped to 1–5: 20–22 = 5 | 16–19 = 4 | 11–15 = 3 | 6–10 = 2 | 0–5 = 1

**Mandatory fields (blocking):** Outcomes · Stakeholders · Risks · Commitments

### `handoff-brief-generator` (Subagent)

Transforms validated handoff data into a meeting-ready internal brief for the CSM and Onboarding Lead. Structured around the six agenda items of the 30-minute internal handoff meeting. Surfaces commitments, flags relationship risks, and ends Section 3 with the account's north star statement.

### `kickoff-prep-builder` (Subagent)

Produces three artifacts:

| Artifact | Audience | Purpose |
|---|---|---|
| Kickoff Agenda | Customer-facing | Sendable meeting agenda; sized and toned by deal tier |
| Stakeholder Prep Guide | CSM internal | Per-attendee briefing; power dynamics; tone guidance |
| Success Plan Skeleton | Draft — kickoff discussion | Six-section first draft with outcomes, milestones, risks, commitments |

Meeting duration by tier: SMB = 45 min · Mid-Market = 50 min · Enterprise = 60 min

### `gate0-assessor` (Subagent)

Issues a binding verdict on the complete handoff package across five quality dimensions.

| Dimension | Auto-FAIL Trigger |
|---|---|
| Completeness | Any dimension score = 0 |
| Stakeholder Coverage | Neither Exec Sponsor nor Champion identified |
| Outcome Clarity | No outcomes stated or outcomes too vague to act on |
| Risk Identification | "No known risks" without attribution |
| Ownership Clarity | CSM not assigned past the SLA window |

**Verdict options:**
- **PASS** — All dimensions ≥ 2; no zeros; account advances to Stage 1
- **CONDITIONAL PASS** — One dimension scores 1; account may advance with a documented 5-day remediation commitment
- **FAIL** — Any dimension scores 0, or two or more dimensions score 1

---

## Commands

### `/run-handoff [account name]`

Launches the `handoff-intake-agent` to run the complete Stage 0 workflow. See `commands/run-handoff.md` for full usage details.

---

## SLA Reference

| Tier | Internal Handoff SLA | Customer Kickoff SLA |
|---|---|---|
| SMB | 1–2 business days after Closed Won | 5–7 days after internal handoff |
| Enterprise | 3–5 business days after Closed Won | 5–7 days after internal handoff |

SLA breaches are flagged in the Gate 0 assessment and escalated to CS leadership. A breach does not automatically fail Gate 0 but is always documented.

---

## Output Package

A completed Stage 0 workflow delivers five artifacts:

1. **Validation Report** — Section scores, mandatory field status, gap list, extracted commitments, stakeholder coverage assessment
2. **Internal CS Brief** — Meeting-ready document for the 30-minute internal handoff meeting
3. **Kickoff Agenda** — Customer-facing; sendable immediately
4. **Stakeholder Prep Guide** — Internal CSM briefing for kickoff preparation
5. **Success Plan Skeleton** — Draft v0.1; ready to populate with the customer in or after the kickoff meeting
6. **Gate 0 Assessment** — Formal PASS / CONDITIONAL PASS / FAIL verdict with dimension scores and carry-forward watch items

---

## Integration

This plugin is designed for use within the `claude-for-customer-success` plugin collection.

**Plugin directory placement:**

```
claude-for-customer-success/
└── handoff/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── agents/
    │   ├── handoff-intake-agent.md
    │   ├── handoff-record-validator.md
    │   ├── handoff-brief-generator.md
    │   ├── kickoff-prep-builder.md
    │   └── gate0-assessor.md
    ├── commands/
    │   └── run-handoff.md
    └── README.md
```

---

## Lifecycle Position

This plugin covers **Stage 0: Pre-Onboard** of the SuccessCOACHING 7-stage Customer Lifecycle.

```
Closed Won → Stage 0 (this plugin) → Gate 0 → Stage 1 Onboarding
```

Stage 0 begins at Closed Won and ends when Gate 0 issues a PASS or CONDITIONAL PASS verdict. A FAIL verdict returns the account to the AE for remediation before Stage 1 can begin.

---

*SuccessCOACHING · Customer Success Infrastructure · Stage 0 Handoff v1.0*
