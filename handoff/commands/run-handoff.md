# Run Handoff

Launches the `handoff-intake-agent` to run the complete Stage 0 Sales-to-CS Handoff workflow for a new account.

## Usage

```
/run-handoff [account name]
```

**Example:**
```
/run-handoff Acme Corp
```

## What This Command Does

Initiates the `handoff-intake-agent` orchestrator, which runs the full Stage 0 workflow in sequence:

1. **Validates** the incoming handoff record against 11 sections and 4 mandatory fields
2. **Generates** the internal CS brief for the 30-minute internal handoff meeting
3. **Builds** the customer-facing kickoff package (agenda, stakeholder prep guide, success plan draft)
4. **Assesses** Gate 0 readiness across 5 quality dimensions and issues a binding verdict

## When to Use

Run this command when:
- A deal has just reached Closed Won and the AE is ready to submit the handoff record
- A CSM needs to assess an existing handoff for Gate 0 readiness
- You want to generate kickoff materials for an account that has already been internally briefed

## What You'll Need

Have the following ready before running:

| Item | Required? | Notes |
|---|---|---|
| Account name | Yes | Used to identify and label all outputs |
| Deal tier | Yes | Determines SLA windows, meeting durations, and tone |
| Closed Won date | Yes | Used to calculate SLA status |
| Handoff record content | Yes | Paste, upload, or describe — the agent will prompt |
| Assigned CSM | Recommended | If TBD, flag for immediate assignment |
| AE name | Recommended | For brief and escalation routing |

## SLA Reminder

| Tier | Internal Handoff SLA | Customer Kickoff SLA |
|---|---|---|
| SMB | 1–2 business days after Closed Won | 5–7 days after internal handoff |
| Enterprise | 3–5 business days after Closed Won | 5–7 days after internal handoff |

If the account has already passed its internal handoff SLA window, the agent will flag a breach. This does not block the workflow but will add a BREACH FLAG to the Gate 0 assessment and trigger escalation to CS Leadership.
