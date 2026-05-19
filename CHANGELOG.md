# Changelog

All notable changes to `claude-for-customer-success` are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.1.0] — 2026-05-18

### Added
- 80 per-skill README files co-located with each SKILL.md (`README.md` in each skill directory)
- Root `README.md` sections: License, Disclaimer, Contributing, Bugs and Issues, Support, Security, Changelog
- `CHANGELOG.md` (this file)

### Changed
- Expanded Disclaimer to cover all artifact types: skills, plugins, managed agent cookbooks, commands, Claude Code hooks, MCP configurations, connectors, and methodology frameworks

### Deprecated
- `rev-ops/skills/territory-optimization/` — marked deprecated with migration note; not removed (see skill README for details)

---

## [1.0.0] — 2026-04-01

### Added
- Initial release: six plugins across 81 skills covering the full Customer Success lifecycle
  - `csm/` — Core CSM workflows: health scoring, QBR prep, executive engagement, expansion, TARO plays
  - `renewals/` — Renewal pipeline: risk briefing, renewal call prep, negotiation prep, post-renewal retrospective
  - `cs-ops/` — CS operations: tech stack audit, tooling ROI, metrics framework, capacity planning
  - `rev-ops/` — Revenue operations: territory optimization, capacity planning, pipeline intelligence, compensation modeling
  - `onboarding/` — Customer onboarding: kickoff facilitation, implementation tracking, adoption acceleration
  - `auq-resilience/` — Claude Code hooks for AUQ fallback resilience (PreToolUse + PostToolUse)
- Managed agent cookbooks in `managed-agent-cookbooks/`
- Machine-readable capability registry: `docs/claude-for-cs-agent-capability-model.yaml`
- Extended documentation: capability model, lifecycle guide, integrated journey value realization guide
