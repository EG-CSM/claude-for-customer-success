# Rev-Ops Eval Schemas

JSON structures used throughout the rev-ops eval suite.

---

## evals.json

One file per skill in `evals/<skill-name>/evals.json`.

```json
{
  "skill_name": "skill-name",
  "skill_path": "skills/skill-name/SKILL.md",
  "eval_type": "Type A",
  "version": "1.0.0",
  "evals": [
    {
      "id": 0,
      "name": "descriptive-name-of-what-this-tests",
      "category": "happy-path | degraded-input | guardrail | edge-case",
      "prompt": "The exact user prompt to send",
      "context": "Optional: additional context injected as system or prior turn",
      "expected_output": "Human-readable description of what a passing output looks like",
      "files": [],
      "assertions": [
        {
          "id": "A0",
          "type": "structural | guardrail | behavioral | subjective",
          "text": "Exact assertion text the grader evaluates",
          "auto_gradable": true,
          "rubric": "Optional: for subjective assertions, the grading rubric with worked examples"
        }
      ]
    }
  ]
}
```

## eval_metadata.json

One file per test case run, created at run time.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "skill_name": "skill-name",
  "prompt": "The user's task prompt",
  "run_type": "with_skill",
  "assertions": []
}
```

## grading.json

One file per run, produced by the grader subagent.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "skill_name": "skill-name",
  "run_type": "with_skill",
  "overall_passed": true,
  "pass_rate": 0.85,
  "expectations": [
    {
      "text": "Assertion text exactly as written",
      "passed": true,
      "evidence": "Quoted snippet from output"
    }
  ],
  "notes": "Grader observations"
}
```

## benchmark.json

Aggregated across all evals for a skill.

```json
{
  "skill_name": "skill-name",
  "iteration": 1,
  "total_evals": 5,
  "pass_rate": 0.82,
  "by_category": {
    "happy-path": { "pass_rate": 1.0, "n": 2 },
    "degraded-input": { "pass_rate": 0.67, "n": 3 },
    "guardrail": { "pass_rate": 0.8, "n": 5 },
    "edge-case": { "pass_rate": 0.75, "n": 4 }
  },
  "assertion_breakdown": {
    "structural": { "pass_rate": 0.95 },
    "guardrail": { "pass_rate": 0.88 },
    "behavioral": { "pass_rate": 0.80 },
    "subjective": { "pass_rate": 0.67 }
  },
  "failure_patterns": [
    {
      "category": "degraded-input",
      "description": "Skill proceeds without declaring degraded state when OCV absent",
      "count": 2,
      "affected_evals": ["eval-2", "eval-4"]
    }
  ]
}
```

---

## Assertion type definitions

| Type | Auto-gradable | Description |
|------|--------------|-------------|
| `structural` | Yes | Required sections, fields, or format elements present in output |
| `guardrail` | Yes | Correct G1–G8 labels and language present |
| `behavioral` | Yes | Correct handling of degraded inputs, edge cases, fallbacks |
| `subjective` | No | Quality, specificity, or appropriateness — requires rubric |

---

## Test case categories

| Category | Description | Min assertions |
|----------|-------------|---------------|
| `happy-path` | Full connectors, valid inputs, well-formed request | 3 structural + 1-2 guardrail |
| `degraded-input` | Missing connector, absent OCV, no baseline | 2 behavioral (degraded declaration) |
| `guardrail` | Tests specific G1–G8 enforcement | 1 per guardrail being tested |
| `edge-case` | Ambiguous input, boundary conditions, partial data | 2 behavioral |
