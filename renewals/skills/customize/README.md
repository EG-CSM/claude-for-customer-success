# renewals.customize

Configuration skill (config_skill). Makes targeted updates to renewals/CLAUDE.md or company-profile.md without running the full cold-start-interview. Includes a validate mode that runs consistency checks across configuration fields.

## Use it for

- Update a single CLAUDE.md field (e.g., discount floor, escalation SLA)
- Edit company-profile.md company-level fields
- Validate current configuration for internal consistency
- Show current configuration without editing

## Don't use it for

- First-time setup (use cold-start-interview)
- Executing renewals workflows (this is config-only)

## How to trigger it

Say something like:

- "update the renewals config"
- "change the discount floor"
- "update my escalation SLA"
- "show current config"
- "validate config"
- "--show"
- "--edit"
- "--validate"

## What you get

- Updated renewals/CLAUDE.md (--edit mode)
- Updated company-profile.md (--edit company fields)
- Consistency report (--validate mode)

## Prerequisites

- renewals/CLAUDE.md (must exist; routes to cold-start-interview if not found)
- company-profile.md (for company-level field edits)

## Governance

- {'--validate checks four consistency rules': 'GRR/NRR inversion, discount floor vs anchor, escalation SLA vs renewal window, strategic threshold vs deal size'}
- Edits to company-profile.md affect all domains — confirm scope before writing
- Cannot create CLAUDE.md if missing — routes to cold-start-interview

## See also

- renewals.cold-start-interview (full setup; prerequisite)
- All renewals skills (consume updated CLAUDE.md)

---

*Domain: `renewals` · Skill ID: `renewals.customize`*
