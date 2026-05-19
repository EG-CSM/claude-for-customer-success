# renewals.cold-start-interview

Configuration skill (config_skill). Conducts the renewals domain onboarding interview, populates renewals/CLAUDE.md, and optionally updates the shared company-profile.md. All other renewals skills read CLAUDE.md at startup; this skill creates and maintains that file.

## Use it for

- First-time renewals domain setup
- Updating specific CLAUDE.md sections without full redo
- Checking current configuration state
- Validating integration connector status

## Don't use it for

- Non-renewals domain configuration (each domain has its own cold-start-interview)
- Executing any renewals workflow (configure first, then run skills)

## How to trigger it

Say something like:

- "set up renewals"
- "configure the renewals domain"
- "run renewals onboarding"
- "update renewals config"
- "--check-integrations"
- "--redo-company-profile"

## What you get

- renewals/CLAUDE.md (created or updated)
- company-profile.md (created or updated, if --redo-company-profile or first run)

## Prerequisites

- None required at invocation — skill elicits all needed context via interview
- Checks for existing company-profile.md before asking company-level questions

## Governance

- Must complete before any other renewals skill can execute reliably
- --redo overwrites CLAUDE.md; warn user before executing
- Company-profile.md changes affect all domains — confirm scope before writing

## See also

- renewals.customize (targeted updates post-interview)
- All other renewals skills (consume CLAUDE.md produced here)

---

*Domain: `renewals` · Skill ID: `renewals.cold-start-interview`*
