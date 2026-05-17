# Rev-Ops Plugin Eval Suite
## claude-for-customer-success / rev-ops — v1.0.0

Test suite for the 8 priority skills: cold-start-interview and all 7 SA5 Revenue
Continuity skills. Designed to run in Claude Code using the `skill-evaluator` skill.

---

## Coverage

| Skill | Evals | Happy path | Degraded input | Guardrail | Edge case |
|-------|-------|-----------|---------------|-----------|-----------|
| cold-start-interview | 4 | 2 | 1 | — | 1 |
| deal-to-outcome-tracing | 4 | 2 | 1 | — | 1 |
| sales-cs-handoff-quality-scoring | 4 | 1 | — | 2 | 1 |
| closed-won-to-cs-capacity-modeling | 3 | 1 | 1 | — | 1 |
| growth-model-vs-actuals-tracking | 3 | 1 | 1 | 1 | — |
| outcome-to-value-tracking | 4 | 2 | 1 | — | 1 |
| early-churn-downgrade-signal-detection | 4 | 1 | — | 2 | 1 |
| gtm-unified-metrics-pulse | 4 | 1 | 1 | 1 | 1 |
| **Total** | **30** | **11** | **6** | **6** | **7** |

---

## Assertion composition

| Type | Count | Auto-gradable |
|------|-------|--------------|
| structural | 42 | Yes |
| behavioral | 61 | Yes |
| guardrail | 38 | Yes |
| subjective | 8 | No — rubrics provided |
| **Total** | **149** | **95% auto-gradable** |

---

## Running evals in Claude Code

### Prerequisites

- rev-ops plugin installed
- `skill-evaluator` skill installed
- HubSpot, CS platform, Linear, and Google Drive connectors configured

### Run a single skill

```bash
# In Claude Code:
Run evals on the deal-to-outcome-tracing skill.
Eval file: rev-ops/evals/deal-to-outcome-tracing/evals.json
Skill file: rev-ops/skills/deal-to-outcome-tracing/SKILL.md
```

The skill-evaluator will:
1. Read the evals.json
2. Spawn with-skill and baseline subagents for each test case
3. Grade against assertions
4. Aggregate into benchmark.json

### Run all 8 priority skills

```bash
Run evals on all skills in rev-ops/evals/ — one skill at a time.
Use rev-ops/evals/agents/grader.md as the grader instructions.
Aggregate results with rev-ops/evals/scripts/aggregate_benchmark.py.
```

### Aggregate benchmark manually

```bash
python rev-ops/evals/scripts/aggregate_benchmark.py \
  ./deal-to-outcome-tracing-workspace/iteration-1 \
  --skill-name deal-to-outcome-tracing
```

---

## Interpreting results

### Pass rate targets

| Category | Target pass rate | Notes |
|----------|-----------------|-------|
| structural | ≥ 95% | Format compliance — should be near-perfect |
| guardrail | ≥ 90% | G1–G8 enforcement — critical for production |
| behavioral | ≥ 85% | Degraded input handling — expect some variation |
| subjective | ≥ 75% | Quality judgments — rubrics reduce variance |

### Red flags

**Guardrail failures < 80%:** Skills are not applying G1–G8 reliably. Reasoning
Protocol section needs strengthening for the failing guardrail. Do not deploy to
production until guardrail pass rate reaches 90%.

**Behavioral failures on degraded-input tests:** Skill is proceeding silently
on missing data. The fallback protocol section is not firing. Fix the fallback
declaration language in the skill body.

**Structural failures:** Required output sections are missing or malformed.
Check the output format section of the failing skill.

---

## Guardrail assertion thresholds

Guardrail assertions use exact match or semantic match per `agents/grader.md`.
The grader must not give partial credit — a guardrail either fired or it didn't.

Critical guardrails by skill:

| Skill | Critical guardrails |
|-------|-------------------|
| deal-to-outcome-tracing | G5, G6, G8 |
| sales-cs-handoff-quality-scoring | G7, G8 |
| closed-won-to-cs-capacity-modeling | G2 |
| growth-model-vs-actuals-tracking | G1, G6 |
| outcome-to-value-tracking | G5, G8 |
| early-churn-downgrade-signal-detection | G5, G7 |
| gtm-unified-metrics-pulse | G1, G2, G7, G6 |

Any skill failing its critical guardrail on a guardrail test case is a
**blocking failure** — do not ship that skill until the guardrail passes.

---

## Extending the eval suite

To add evals for the remaining 23 skills, follow the same structure:

1. Create `evals/<skill-name>/evals.json` using `references/schemas.md`
2. Include at least: 1 happy-path, 1 degraded-input, 1 guardrail test
3. Assertions: ≥ 2/3 objective (structural, behavioral, or guardrail)
4. Subjective assertions must include a rubric with PASS/FAIL examples
5. Run with skill-evaluator; target pass rates in the table above

Priority order for remaining skills:
1. SA1 scenario-modeling (feeds annual-planning-workflow)
2. SA3 annual-planning-workflow (highest-stakes planning skill)
3. SA6 deal-desk-workflow-management (approval routing)
4. SA2 deal-health-scoring (weekly workflow)
5. All remaining skills
