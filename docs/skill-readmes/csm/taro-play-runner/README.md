# csm.taro-play-runner

Selects and executes TARO (Trigger-Action-Resource-Outcome) plays for a given situation. Produces execution-ready outputs — email drafts, meeting agendas, talking points — calibrated to the play and customer context.

## Use it for

- Situation-based play selection
- Full play execution with customer-ready outputs

## Don't use it for

- Playbook auditing (use cs-ops.playbook-auditor)
- Play creation or editing

## How to trigger it

Say something like:

- "run a play"
- "which play should I use"
- "TARO play"
- "play for [situation]"
- "execute play"

## What you get

- Play execution brief
- Email draft / agenda / talking points

## Prerequisites

- csm CLAUDE.md
- Playbook registry with TARO plays
- Account and situation context

## Governance

- Customer-facing outputs require CSM review before sending

## See also

- cs-ops.playbook-auditor
- csm.call-prep

---

*Domain: `csm` · Skill ID: `csm.taro-play-runner`*
