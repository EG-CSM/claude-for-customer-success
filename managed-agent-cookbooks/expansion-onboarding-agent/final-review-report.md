# Expansion Onboarding Agent Cookbook — Final Publication Review

**Verdict:** PUBLISH WITH NOTES
**Review date:** 2026-05-18
**Specialist agents:** Technical Accuracy (A), Internal Consistency (B), Security & Governance (C), Operational Completeness (D), Publishability (E)
**All agents returned:** PASS WITH NOTES (zero BLOCKs across all five)

---

## Consolidated Findings

### BLOCK findings

None

### WARN findings

**WARN-C01: Inline self-contradiction in Scanner qualifying condition**
The Scanner section contains an uncleaned drafting artifact: "Qualifying: no existing plan found, or only plan has status=closed → Wait — closed plans are NOT qualifying." The inline correction directly contradicts the condition above it, creating an irreconcilable ambiguity about whether closed-plan accounts qualify for onboarding plan creation.
*Raised by: Agent A (WARN-03), Agent B (NOTE-3)*

**WARN-C02: `plan_status` skip-set / Creator output mismatch**
The Scanner's idempotency skip condition lists `active`, `in_progress`, `pending` as states to skip. The Creator produces plans in `pending_activation` and `initializing` states — neither of which appears in the Scanner's skip set. A plan created by one sweep could be re-processed by a subsequent sweep, breaking idempotency and potentially creating duplicate onboarding plans.
*Raised by: Agent A (WARN-02), Agent D (NOTE-5)*

**WARN-C03: `scan_summary` passthrough to Notification Composer undocumented**
The orchestrator's STEP 4 pass list does not include `scan_summary`, but the Notification Composer requires it to populate footer fields (`won CSQLs found`, `qualifying`, `skipped`, `failed`). An implementer following the STEP 4 spec will produce a Composer invocation missing required inputs.
*Raised by: Agent A (NOTE-06), Agent B (WARN-3)*

**WARN-C04: `skip_log` union ownership undocumented**
STEP 4 instructs the orchestrator to "pass skip_log" without specifying that this must be the union of Scanner-phase skips and Creator-phase skips. An implementer will likely discard Scanner skips when assembling the Creator output, producing an incomplete skip log in the Notification Composer.
*Raised by: Agent B (WARN-1)*

**WARN-C05: Empty qualifying_csqls path — Scanner skip_log silently dropped**
When no qualifying CSQLs exist and STEP 4 bypass is triggered, the spec does not confirm that the Scanner's accumulated skip_log is still forwarded to the Composer. Skips from the scan phase are silently lost, producing an inaccurate notification.
*Raised by: Agent B (WARN-2), Agent D (WARN-2)*

**WARN-C06: Race condition across concurrent sweep invocations**
Two simultaneous scheduled sweeps can both pass the idempotency check before either creates a plan. No locking or deduplication mechanism is documented. This is a realistic failure mode for daily scheduled invocations and could result in duplicate onboarding plans.
*Raised by: Agent C (WARN-1)*

**WARN-C07: `config_override` in webhook body is unbounded**
No field allowlist is defined for `config_override`. A caller can set `dry_run=false`, an arbitrarily large `look_back_hours`, or redirect the output channel. The absence of an allowlist is an implementation-level security gap that will not be caught by any guardrail described in the cookbook.
*Raised by: Agent C (WARN-2)*

**WARN-C08: Scanner and Notification Composer subagents have no explicit NEVER rules**
Behavioral constraints for these two subagents are expressed as guidance only. Without hard behavioral prohibitions, a misconfigured or directly-invoked subagent has no declared constraint boundary. The Notification Composer could send live notifications if invoked directly without the orchestrator's dry_run guardrail.
*Raised by: Agent C (WARN-3), Agent B (NOTE-1)*

**WARN-C09: Malformed CSQL data (wrong type) handling unspecified**
Field validation covers missing fields but not type errors. A CSQL with `arr_uplift` as a string instead of a number passes the missing-field check and will likely cause a downstream failure with no specified handling path.
*Raised by: Agent D (WARN-1)*

**WARN-C10: All-records-fail behavior in STEP 3 unspecified**
When every CSQL in `qualifying_csqls` fails Creator invocation, the spec does not define whether the orchestrator proceeds to the Notification Composer or halts entirely. An implementer must choose behavior not specified by the cookbook, with no stated preference.
*Raised by: Agent D (WARN-3)*

**WARN-C11: On-demand invocation scan window undefined**
On-demand (recovery) invocations have no specified `look_back_hours`. An operator manually triggering recovery after an outage has no defined scan window — the cookbook does not state whether the default applies, or whether the operator must supply the value explicitly.
*Raised by: Agent D (WARN-4)*

**WARN-C12: Audience demarcation absent; terminology undefined for mixed readership**
CSM-facing and implementer-facing sections are interleaved with no labels or visual separation. Key terms used without definition for a mixed audience include `arr_uplift`, `M1 kickoff`, `four-milestone scaffold`, `idempotency`, and `look_back_hours`. An implementer unfamiliar with the domain may misapply core constructs.
*Raised by: Agent E (WARN-1, WARN-2)*

**WARN-C13: `csm:expansion-onboarding operation=status` underdocumented**
The status operation has no documented request parameters, no response schema, and no specification of what "null plan" means in context. Implementers must infer expected behavior from behavioral description alone.
*Raised by: Agent A (WARN-01)*

---

### NOTE findings

**NOTE-C01: `account_id_format` config field silently ignored**
STEP 3's hardcoded `onboarding_id` format validation ignores the `account_id_format` config field. Custom formats silently fail with no error surfaced to the operator.
*Raised by: Agent A (NOTE-01)*

**NOTE-C02: `m1_kickoff_date_source` absent from output schema**
This field appears in derivation logic but is not present in the output schema.
*Raised by: Agent A (NOTE-02)*

**NOTE-C03: dry_run behavior for `operation=status` calls unspecified**
The spec does not confirm that `operation=status` calls should still proceed in dry_run mode. An implementer may suppress status calls, breaking the idempotency check.
*Raised by: Agent A (NOTE-03)*

**NOTE-C04: `would_create` list schema undefined**
The dry_run output field `would_create` has no documented field schema.
*Raised by: Agent A (NOTE-04)*

**NOTE-C05: Config injection defense scope ambiguous**
The spec does not confirm that config injection defenses apply to both config files and subagent stubs.
*Raised by: Agent C (NOTE-1)*

**NOTE-C06: String field content not validated in schema check**
Schema validation verifies field presence and type but not string content. A malformed connector name or erroneous ID string passes as valid.
*Raised by: Agent C (NOTE-2, NOTE-4)*

**NOTE-C07: `arr_uplift` data sensitivity not flagged**
Exposure of `arr_uplift` in the CS Slack channel is a data sensitivity decision that is not flagged or discussed in the cookbook.
*Raised by: Agent C (NOTE-3)*

**NOTE-C08: Connector operation surface defined by absence, not allowlist**
Unreferenced connector operations are not explicitly prohibited; the surface is bounded only by what is documented.
*Raised by: Agent C (NOTE-5)*

**NOTE-C09: Cron timezone unspecified**
The scheduling section does not specify timezone for cron expressions, creating potential window drift in non-UTC deployments.
*Raised by: Agent D (NOTE-6)*

**NOTE-C10: Slack partial-delivery recovery path incomplete**
When running in "both" output mode, the recovery path for a Slack success / file write failure is not fully specified.
*Raised by: Agent D (NOTE-7)*

**NOTE-C11: `stage=won` vs. `csql_stage=won` terminology inconsistency**
These two forms appear across sections without clarification that they refer to the same condition.
*Raised by: Agent B (NOTE-2)*

**NOTE-C12: Sample output `close_date` source ambiguous**
The derivation source for M1 kickoff date in the sample output (CSQL close_date field vs. plan creation date) is not made explicit.
*Raised by: Agent E (WARN-3) — re-tiered to NOTE; cosmetic clarity issue in sample only*

**NOTE-C13: No prerequisite setup sequence for first-time deployers**
Connectors, config files, and scheduling must be assembled without a "start here" guide.
*Raised by: Agent E (NOTE-4)*

**NOTE-C14: "What it does not do" section missing explicit exclusions**
CSQL record write-back and milestone progress tracking are not called out as explicit exclusions.
*Raised by: Agent E (NOTE-5)*

**NOTE-C15: Scheduling section lacks operational context**
The section does not state where cron expressions are entered or how the webhook connects to Rev-Ops tooling.
*Raised by: Agent E (NOTE-6)*

**NOTE-C16: Three ambiguous phrases**
"Authoritative fallback" (meaning unclear), "logs a skip and notifies the CSM" (channel vs. DM unspecified), "CSM handles re-initiation explicitly" (no action specified).
*Raised by: Agent E (NOTE-7)*

---

## Verdict Rationale

All five specialist agents returned PASS WITH NOTES with zero BLOCK findings, confirming that no single finding would cause incorrect behavior or data loss in a production deployment as the cookbook currently stands. However, thirteen consolidated WARN findings remain — several of which cluster around consequential implementation paths: the idempotency skip-set mismatch (WARN-C02), the `scan_summary` passthrough gap (WARN-C03), the concurrent invocation race condition (WARN-C06), and the all-records-fail halt/continue decision (WARN-C10). A careful implementer can navigate these ambiguities, but will need to make undocumented design decisions at each. The PUBLISH WITH NOTES verdict reflects this pattern: the cookbook is structurally sound and safe to publish, but the WARN cluster is dense enough that it cannot be released without drawing the reader's attention to the open specification gaps.

---

## Publication Recommendation

The cookbook should be published with an accompanying errata or "known implementation gaps" callout visible at the point of first use — not buried in an appendix. Implementers should be directed to pay particular attention to four WARNs before beginning deployment: the `plan_status` skip-set / Creator output mismatch (WARN-C02), which poses the highest risk of silent duplicate plan creation; the `scan_summary` and `skip_log` passthrough gaps (WARN-C03, WARN-C04), which will produce incorrect Notification Composer output if not resolved at integration time; and the concurrent invocation race condition (WARN-C06), which requires an external locking or deduplication mechanism not specified in the cookbook. The remaining WARNs are resolvable by a competent implementer exercising judgment, but should be tracked as a post-publication revision backlog with priority on WARN-C01 (the inline self-contradiction) and WARN-C10 (the all-records-fail halt/continue gap), both of which currently leave implementers with no specified correct behavior.

---

## Review Metadata

| Field | Value |
|-------|-------|
| Cookbook path | `managed-agent-cookbooks/expansion-onboarding-agent/cookbook.md` |
| Cookbook length | 681 lines, 12 sections |
| Review type | Pre-publication critical gate — parallel 5-agent specialist review + synthesis |
| Forcing-function markers | FOXTROT-3381-CONDOR (A), GOLF-6627-PELICAN (B), HOTEL-9943-IBIS (C), INDIA-1156-EGRET (D), JULIET-7782-CURLEW (E), KILO-4417-SNIPE (Synthesis) |
| All markers verified | ✓ at position 1 in each agent output |
| BLOCK findings | 0 |
| WARN findings | 13 (consolidated from 5-agent parallel review) |
| NOTE findings | 16 (consolidated from 5-agent parallel review) |
| Final verdict | **PUBLISH WITH NOTES** |
