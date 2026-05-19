# csm.account-research

Generates pre-call account briefs with stakeholder intelligence, product usage signals, support history, and relationship context. Works standalone via web search; enriched with CRM and CS Platform connectors.

## Use it for

- Pre-call account brief (standard depth)
- Deep account research with all available signals
- Stakeholder mapping for a specific account

## Don't use it for

- Call agenda construction (use csm.call-prep)
- Portfolio-level analysis (use cs-ops.segment-analyzer)

## How to trigger it

Say something like:

- "research [account]"
- "account brief"
- "tell me about [company]"
- "who are the stakeholders"

## What you get

- Account brief (markdown)
- Stakeholder list

## Prerequisites

- csm CLAUDE.md company profile
- Account name or ID

## Governance

- Brief content from training data is [Moderate] confidence without connectors

## See also

- csm.call-prep
- csm.stakeholder-map

---

*Domain: `csm` · Skill ID: `csm.account-research`*
