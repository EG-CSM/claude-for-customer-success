# rev-ops.non-standard-terms-detection

Detects non-standard contract terms across four pattern categories: payment schedule deviations, liability/indemnification modifications, SLA commitments outside standard tier, and IP or data provisions. Routes findings to Legal or Finance; creates Linear issues for tracking. Sub-component of deal-desk-workflow-management.

## Use it for

- Scan contract or deal terms for non-standard patterns
- Classify finding by category (payment/liability/SLA/IP)
- Route to Legal or Finance based on category
- Create Linear issue for tracking and approval record

## Don't use it for

- Approving non-standard terms (routes to Legal/Finance)
- Full deal desk workflow (use deal-desk-workflow-management)
- Discount monitoring (use discount-threshold-monitoring)

## How to trigger it

Say something like:

- "non-standard terms"
- "contract terms review"
- "unusual terms"
- "terms deviation"
- "contract red flags"

## What you get

- Non-standard terms finding report with category and routing (Markdown)
- Linear issue for each finding requiring approval

## Prerequisites

- Contract or deal terms text
- Standard terms baseline (from domain CLAUDE.md)

## Governance

- {'G1': 'never approves non-standard terms autonomously'}
- Routing to Legal/Finance is required for all findings

## See also

- rev-ops.deal-desk-workflow-management
- rev-ops.discount-threshold-monitoring
- rev-ops.revenue-leakage-scanning

---

*Domain: `rev-ops` · Skill ID: `rev-ops.non-standard-terms-detection`*
