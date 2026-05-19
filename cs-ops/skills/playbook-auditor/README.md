# cs-ops.playbook-auditor

Audits CS playbook coverage, trigger definitions, adoption rates, and dead plays. Surfaces gaps where motion types lack playbooks, identifies under-adopted plays, and flags plays that haven't been executed in a configurable lookback window.

## Use it for

- Quarterly playbook coverage audit
- Dead play identification and retirement
- Adoption rate analysis by play and CSM
- Single play deep-dive

## Don't use it for

- Play execution (use csm.taro-play-runner)
- Writing new playbooks

## How to trigger it

Say something like:

- "playbook audit"
- "playbook coverage"
- "dead plays"
- "play adoption"
- "which plays aren't being used"

## What you get

- Playbook coverage gap report
- Adoption scorecard
- Dead play retirement candidates

## Prerequisites

- cs-ops CLAUDE.md
- Playbook registry

## Governance

- Audit only — no play retirement without CS leadership approval

## See also

- csm.taro-play-runner

---

*Domain: `cs-ops` · Skill ID: `cs-ops.playbook-auditor`*
