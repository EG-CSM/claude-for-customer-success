# cs-ops.health-model-review

Audits the portfolio health model for distribution anomalies, calibration drift, and component weight validity. Surfaces whether the model is accurately predicting risk and recommends recalibration when distributions are skewed.

## Use it for

- Quarterly health model calibration review
- Distribution audit (too many Green, skewed Red)
- Component weight audit
- Full health model assessment

## Don't use it for

- Individual account health review (use csm.health-score-review)
- Health score changes without CS leadership approval

## How to trigger it

Say something like:

- "health model"
- "calibrate health scores"
- "health distribution"
- "too many green accounts"
- "health model weights"

## What you get

- Distribution analysis report
- Calibration recommendations
- Component weight audit

## Prerequisites

- cs-ops CLAUDE.md
- Portfolio health data

## Governance

- Recommendations only — model changes require CS leadership sign-off

## See also

- csm.health-score-review
- cs-ops.segment-analyzer

---

*Domain: `cs-ops` · Skill ID: `cs-ops.health-model-review`*
