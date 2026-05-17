---
title: "Reasoning Blueprint: CSM Plugin Customization"
type: reasoning-blueprint
skill: customize
version: 1.0.0
---

# Reasoning Blueprint: CSM Plugin Customization

Load this blueprint when Tier 3 reasoning is activated for customization work.

## Problem Classification Taxonomy

| Type | Characteristics | Primary Risk | Expert Focus |
|------|----------------|--------------|--------------|
| **Full Configuration** | First install or major practice change; all 8 interview sections required; produces both config files from scratch | Incomplete answers propagate placeholder gaps to every downstream skill | Ensure every section has real values — no silent placeholders |
| **Section Reconfiguration** | Single section update (e.g., health model weights changed); existing config must be preserved around the edit | Overwriting adjacent sections or breaking cross-section dependencies (e.g., churn signals reference health thresholds) | Validate that the changed section remains consistent with unchanged sections |
| **Motion Change** | CS motion shift (tech-touch → high-touch, or new segment introduced); cascading impact on engagement model, escalation matrix, and playbook | Under-scoping — user says "update the motion" but doesn't realize escalation SLAs, cadences, and account loads also change | Surface all downstream sections affected and confirm scope before writing |
| **Integration Swap** | Replacing a CS platform or CRM; tooling section changes but data source assumptions in health model and churn signals may also shift | Config says "Gainsight" but the org moved to Vitally — health score source is now wrong, and skills querying the old platform fail silently | Audit health model source, churn signal data dependencies, and integration priority order |
| **Reset and Rebuild** | Destructive clear of all config; requires explicit confirmation; equivalent to a fresh install afterward | Accidental data loss — user runs reset without realizing all four CS plugins share company-profile.md | Double-confirm intent; warn about cross-plugin impact before clearing |

## Domain Heuristics

**The Downstream Propagation Rule**: Every config value written by customize is read by 10+ downstream skills. Verify each value as if it were a shared constant — because it is.

**The Placeholder Poison Rule**: A `[PLACEHOLDER]` marker in config is better than a wrong value, but both are failures. If the user can't answer a question, mark it as placeholder AND surface it in the post-setup checklist. Never invent a default silently.

**The Cross-Plugin Blast Radius Rule**: `company-profile.md` is shared across csm, cs-ops, renewals, and onboarding plugins. Any edit to company-level fields must include a warning about the other three plugins. Threshold: always warn when touching Section 1 or value framework fields.

**The Segment-Motion Cascade Rule**: When a customer segment definition changes, the CS motion, escalation routing, account load, and engagement cadence for that segment likely also change. Ask explicitly — don't assume the old values still hold.

**The Health Model Source Rule**: Health score components are only meaningful if the data source is configured and accessible. When a user lists health components, confirm where each data point comes from (CS platform API, CRM field, manual entry). An unconfigured source makes the component decorative.

**The Escalation Owner Validation Rule**: An escalation matrix with role titles but no named owners is incomplete. Every row must have a contactable person, not just "VP of CS." If a name isn't available, mark the row as `[OWNER TBD]` and flag it.

**The Playbook Exclusion Rule**: Knowing which plays are NOT used is as important as knowing which are. Explicitly excluded plays prevent downstream skills from suggesting actions the org has consciously rejected.

## Common Failure Modes by Request Type

### Full Configuration
| Failure Mode | Fix |
|-------------|-----|
| User gives partial answers and says "I'll fill in the rest later" — config ships with hidden gaps | After interview, scan every field; list all placeholders in a numbered checklist before writing |
| Health model components listed without weights — defaults to equal weighting silently | Require explicit weights that sum to 100%; reject "I'll figure out weights later" without a placeholder marker |
| Escalation matrix has roles but no names or contact methods | Reject rows missing a named owner; mark as `[OWNER TBD]` with a post-setup action item |

### Section Reconfiguration
| Failure Mode | Fix |
|-------------|-----|
| Updated section contradicts unchanged sections (e.g., new churn signal references a health component that was removed) | After writing the updated section, validate cross-references against the full config |
| User updates health model but forgets to update churn signal thresholds that depend on health scores | Surface dependent sections and ask: "Your churn signals reference health score thresholds — should those update too?" |

### Motion Change
| Failure Mode | Fix |
|-------------|-----|
| Only the cs-motion section is updated; engagement cadences and escalation SLAs remain configured for the old motion | Treat motion change as a multi-section update — surface all affected sections before proceeding |
| New segment added but no escalation owner assigned for that tier | Scan escalation matrix for coverage gaps against the updated segment list |

### Reset and Rebuild
| Failure Mode | Fix |
|-------------|-----|
| User resets without realizing other plugins reference company-profile.md | Before clearing, list all plugins that share the file and require explicit confirmation for each |
| Reset completes but user doesn't re-run the full interview — all skills fail on missing config | After reset, block the confirmation message behind a prompt to start the full interview immediately |

## Expert Judgment Patterns

### When to push back on user answers
- User provides a health model with 8+ components → suggest consolidating to 4-5 for signal clarity
- User lists churn signals that are all "High" weight → challenge: if everything is high priority, nothing is
- User describes a motion as "high-touch" but sets account loads at 150+ → that's scaled, not high-touch; surface the mismatch

### When to expand scope beyond the stated request
- `--section health-model` but churn signals reference health thresholds → offer to review churn signals too
- `--section integrations` and the new platform has different data fields → offer to review health model source mapping

### When to simplify
- User has no formal health model → offer the standard 4-component template (usage, engagement, support, outcomes) rather than forcing a custom design
- User has no playbook → default to standard TARO library and note it can be customized later
- User is unsure about escalation SLAs → offer industry-standard defaults (critical: 4h, high: 24h, medium: 48h) as a starting point
