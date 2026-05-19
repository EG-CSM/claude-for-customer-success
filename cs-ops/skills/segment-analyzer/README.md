# cs-ops.segment-analyzer

Analyzes the book of business by segment — ARR distribution, health distribution, coverage ratios, and at-risk account identification. Surfaces reclassification candidates when accounts no longer fit their current segment criteria.

## Use it for

- Segment-level ARR and health analysis
- Coverage ratio by segment
- At-risk account identification by segment
- Reclassification candidate surfacing

## Don't use it for

- Individual account health review (use csm.health-score-review)
- Capacity modeling (use cs-ops.capacity-planner)

## How to trigger it

Say something like:

- "segment analysis"
- "segment distribution"
- "ARR by segment"
- "at-risk by segment"
- "reclassification"

## What you get

- Segment distribution report
- Reclassification candidate list
- At-risk account list by segment

## Prerequisites

- cs-ops CLAUDE.md

## Governance

- Reclassification recommendations require CS leadership approval

## See also

- cs-ops.capacity-planner
- csm.health-score-review

---

*Domain: `cs-ops` · Skill ID: `cs-ops.segment-analyzer`*
