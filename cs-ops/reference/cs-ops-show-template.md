# CS-Ops Configuration Display Template

*Used by `/cs-ops:customize --show` — render all sections from CLAUDE.md in this format.*

---

**CS-Ops Plugin Configuration**
*`~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`*
*Retrieved: [timestamp]*

---

### Configuration health

| Section | Status | Issues |
|---------|--------|--------|
| Segments | [✅ Configured / ⚠️ Partial / ❌ Placeholder] | [Issues if any] |
| Ratios | [✅ / ⚠️ / ❌] | |
| Health model | [✅ / ⚠️ / ❌] | |
| Playbook | [✅ / ⚠️ / ❌] | |
| Escalation matrix | [✅ / ⚠️ / ❌] | |
| Data quality | [✅ / ⚠️ / ❌] | |
| Reporting | [✅ / ⚠️ / ❌] | |
| Team | [✅ / ⚠️ / ❌] | |

**Overall configuration completeness:** [N/8 sections fully configured]

[If any sections have ❌ Placeholder status:]
> ⚠️ [N] sections still contain placeholder values. Skills that depend on
> unconfigured sections will prompt for `/cs-ops:cold-start-interview` or
> ask for session-level input. Run `/cs-ops:customize --section <name>` to
> configure each section, or `/cs-ops:cold-start-interview` to complete all
> at once.

---

### Current configuration — full display

[Display all configured values from CLAUDE.md in readable format, organized by
section. Do not display raw CLAUDE.md markdown — render values as human-readable
configuration. Replace `[PLACEHOLDER]` markers with ⚠️ PLACEHOLDER — not configured.]

**Segments:**
| Segment | ARR floor | ARR ceiling | Motion | Reclassification threshold |
|---------|----------|------------|--------|--------------------------|
| [Name] | $[floor] | $[ceiling] | [motion] | $[threshold] |

**Target ratios:**
| Segment | Motion | Target accounts/CSM |
|---------|--------|-------------------|
| [Name] | [motion] | [N] |

**Health model:**
| Tier | Score range | Action threshold |
|------|------------|-----------------|
| 🟢 Green | [range] | — |
| 🟡 Yellow | [range] | CTA triggered |
| 🔴 Red | [range] | Immediate CSM action |

*Staleness threshold:* [N] days

**Playbook:** [N plays configured — list names only in --show mode]
*Full play details: use `/cs-ops:playbook-auditor --full`*

**Escalation matrix:**
| Tier | Definition | Response SLA | Owner |
|------|-----------|-------------|-------|
| S1 | [definition] | [SLA] | [owner] |
| S2 | [definition] | [SLA] | [owner] |
| S3 | [definition] | [SLA] | [owner] |

**Data quality:**
*Required fields:* [list] · *Staleness threshold:* [N] days · *Consistency rules:* [N configured]

**Reporting:**
*Primary KPI:* [GRR / NRR / Logo retention] · *Reporting cadence:* [Weekly / Monthly] ·
*Dashboard default:* [--weekly / --monthly / --quarterly]

**Team:** [N CSMs configured — use `/cs-ops:capacity-planner` for full roster view]
