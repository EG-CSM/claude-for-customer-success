# rev-ops.cold-start-interview

Meta-skill. Conducts structured intake interview to populate the rev-ops domain CLAUDE.md profile when it is absent or contains unfilled placeholders. All domain peers check for this profile at startup and route here when missing. Produces the completed CLAUDE.md; does not execute any domain task itself.

## Use it for

- Collect rev-ops domain configuration via structured interview
- {'Populate CLAUDE.md with': 'ARR baseline, pipeline structure, CRM source of truth, forecast cadence, comp plan details, territory structure, data authority hierarchy'}
- Validate completeness before writing profile

## Don't use it for

- Executing rev-ops domain tasks (routes to domain skill after profile is written)
- Making strategic decisions about the configuration values

## How to trigger it

Say something like:

- "Rev-ops CLAUDE.md is absent"
- "Rev-ops CLAUDE.md contains placeholder values"
- "set up rev-ops"
- "configure rev-ops profile"
- "run the rev-ops intake"

## What you get

- Completed rev-ops domain CLAUDE.md

## Governance

- Must not execute domain tasks before profile is complete
- Must validate all required fields before writing CLAUDE.md

## See also

- rev-ops.customize (peer config skill)
- All rev-ops domain skills (consumers of the profile)

---

*Domain: `rev-ops` · Skill ID: `rev-ops.cold-start-interview`*
