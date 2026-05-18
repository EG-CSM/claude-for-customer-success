# Onboarding Skills — Configuration Impact Map

_Which skills read each configuration section and what changes when values are updated._

---

## Required Fields Per Section

The `--validate` mode checks these required fields. Missing required fields = FAIL.

| Section | Required fields |
|---------|----------------|
| milestones | Day target and completion criteria for M1–M5; at-risk signals for each |
| ttv-targets | At least one segment target (Enterprise, Mid-Market, or SMB) |
| onboarding-models | At least one model defined; default model set |
| success-criteria | Criteria format; review cadence |
| escalation | At least the self-resolve threshold and first escalation contact |
| graduation | At least 5 graduation criteria |
| methodology | Primary methodology named |
| integrations | All three connector fields present (even if set to None) |

---

## Internal Consistency Rules

Consistency violations = WARN (skill will still run but may produce unexpected results).

- M1 < M2 < M3 < M4 < M5 day targets (strict ascending order)
- TtV targets ≥ M4 day target for each segment
- Graduation criteria reference completion of M5 at minimum
- If white-glove model is listed, escalation section includes executive sponsor path
- If partner-led model is listed, escalation section includes partner contact path
- If any connector is set to a named tool (not None), the tool name must be one of the
  recognized connectors (flag typos or unrecognized names)

---

## Downstream Skill Impact Map

Which skills read each configuration section and what behavior changes when values are updated.

| Config Section | Skills that read it | What changes when updated |
|----------------|--------------------|-----------------------------|
| milestones | `/onboarding:plan`, `/onboarding:milestone-tracker`, `/onboarding:blocker-review` | Day targets, completion criteria, and at-risk signals used in account plans and milestone assessments |
| ttv-targets | `/onboarding:ttv-analysis`, `/onboarding:plan` | Benchmark values used to flag at-risk accounts and generate TtV forecasts |
| onboarding-models | `/onboarding:plan`, `/onboarding:kickoff-doc`, `/onboarding:handoff-doc` | Model-specific play sequences, escalation paths, and handoff checklists |
| success-criteria | `/onboarding:success-criteria`, `/onboarding:milestone-tracker` | Criteria format and review cadence applied when generating or reviewing account success criteria |
| escalation | `/onboarding:blocker-review` | Named contacts substituted into escalation path recommendations; placeholder contacts cause fallback to generic descriptions |
| graduation | `/onboarding:handoff-doc` | Graduation checklist used in `--readiness` and `--draft` modes; missing graduation section blocks handoff doc generation |
| methodology | `/onboarding:kickoff-doc`, `/onboarding:handoff-doc`, `/onboarding:plan` | Methodology references and play citations in onboarding documents |
| integrations | `/onboarding:plan`, `/onboarding:kickoff-doc`, all skills with CRM/PM pulls | Controls whether skills attempt connector pulls or fall back to manual input mode |

---

## `--view` Mode Output Template

Full template for the `--view` mode display. Render each section with a header bar,
current values, and a completeness indicator.

```
Onboarding Profile — Current Configuration
Last modified: [file modification date if detectable | unknown]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Milestone Framework                                     [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  M1 Kickoff:        Day [X] — [completion criteria summary]
  M2 Tech setup:     Day [X] — [completion criteria summary]
  M3 First use:      Day [X] — [completion criteria summary]
  M4 First value:    Day [X] — [completion criteria summary]
  M5 Handoff ready:  Day [X] — [completion criteria summary]

  At-risk signals configured: [Yes — [N] signals | No — using generic defaults]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: TtV Targets [review — internal planning target]         [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Enterprise:   [X] days
  Mid-Market:   [X] days
  SMB:          [X] days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Onboarding Models                                       [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Default model:     [model name]
  Available models:  [list of models in use]
  Model assignments: [how accounts are assigned to models, e.g., by segment]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Success Criteria                                        [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Criteria format:        [outcome-based | metric-based | milestone-based]
  Review cadence:         [e.g., at M2, M4, and M5]
  Minimum criteria count: [N]
  Maximum criteria count: [N]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Escalation Matrix                                       [⚠ Partial]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1–3 days overdue:  CSM self-resolve
  4–7 days overdue:  [AE name — PLACEHOLDER]
  8+ days overdue:   [Manager name — PLACEHOLDER]
  Executive sponsor: [white-glove model only — PLACEHOLDER]
  Partner contact:   [partner-led model only — not configured]

  ⚠ 2 escalation contacts are [PLACEHOLDER]. Run --update escalation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Graduation Criteria                                     [✗ Missing]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✗ Graduation criteria are [PLACEHOLDER]. Run --update graduation or
    /onboarding:cold-start-interview --section handoff to configure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: CS Methodology                                          [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Methodology:      [TARO | SuccessCOACHING | Custom]
  Play references:  [N plays referenced in onboarding workflow]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION: Integrations                                            [✓ Complete]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  CRM connector:    [Salesforce | HubSpot | None]
  PM connector:     [Asana | Linear | Jira | Monday | None]
  Document storage: [Notion | Google Drive | Confluence | None]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Sections complete:   [N] / 8
  Sections partial:    [N] — have placeholder values or missing fields
  Sections missing:    [N] — required for core skills to function

  Sections requiring attention:
  - [section] — [specific issue]

  Run --validate for a full consistency check, or --update <section>
  to fix a specific section.
```

**Completeness indicators:**
- `[✓ Complete]` — no `[PLACEHOLDER]` values; required fields present
- `[⚠ Partial]` — some fields configured; some still `[PLACEHOLDER]`
- `[✗ Missing]` — entire section is `[PLACEHOLDER]` or absent
- `[— Optional]` — not required for core skills; shown when not configured

---

_Loaded on demand by `/onboarding:customize` — not front-loaded at session start._
