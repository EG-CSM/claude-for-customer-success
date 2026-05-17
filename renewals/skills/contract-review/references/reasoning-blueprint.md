---
title: "Reasoning Blueprint: Contract Review for Renewals"
type: reasoning-blueprint
skill: contract-review
version: 1.0.0
---

# Reasoning Blueprint: Contract Review for Renewals

Load this blueprint when Tier 3 reasoning is activated for contract review work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level extraction and risk flagging of renewal-relevant contract terms.

---

## Problem Classification Taxonomy

### Type A: Standard Renewal Extraction
**Characteristics**: Executed MSA with no amendments, standard terms, auto-renewal with adequate notice window. Contract source is verified (contract system or uploaded signed document).
**Primary Risk**: Complacency — skipping categories because "it's standard" and missing a buried non-standard clause.
**Expert Focus**: Even standard contracts deserve a full eight-category pass; non-standard terms hide in exhibits and addenda.

### Type B: Amended or Multi-Document Contract
**Characteristics**: MSA plus one or more amendments, order forms, or SOWs that modify original terms. Amendment language governs where it conflicts with MSA.
**Primary Risk**: Reviewing the MSA without amendments — producing a risk register that reflects superseded terms.
**Expert Focus**: Build a consolidated term view; flag any category where amendment and MSA conflict and confirm which governs.

### Type C: Price-Constrained Renewal
**Characteristics**: Contract contains price caps, CPI linkage, MFN provisions, or rate locks that limit the commercial motion.
**Primary Risk**: Issuing a price increase that exceeds a contractual ceiling — a breach, not a negotiation misstep.
**Expert Focus**: Extract the exact constraint mechanics (cap %, index, measurement period) and validate against the proposed increase before any commercial action.

### Type D: Time-Critical or Deadline-Pressured Review
**Characteristics**: Auto-renewal notice window, renewal quote obligation, or price increase notification deadline is inside 60 days.
**Primary Risk**: Missing a hard contractual deadline that locks renewal terms or forfeits commercial opportunity for the cycle.
**Expert Focus**: Surface every date-sensitive obligation first, calculate days remaining, and escalate any inside 30 days before completing the full extraction.

### Type E: Incomplete or Unverified Source
**Characteristics**: No executed contract available — working from notes, summaries, verbal accounts, or partial uploads.
**Primary Risk**: Producing a risk register that the CSM treats as authoritative when it is built on unverified inputs.
**Expert Focus**: Flag every output `[Low Confidence]`, suppress action recommendations that assume contract accuracy, and block any commercial decision until the signed document is obtained.

---

## Domain Heuristics

1. **The Amendment-First Rule**: Always pull and read amendments before extracting MSA terms. An amendment can silently replace entire categories. If amendments are unavailable, flag the full output as potentially unreliable.

2. **The 60-Day Alarm**: Any auto-renewal notice deadline, renewal quote obligation, or price increase notification inside 60 days gets surfaced in the first paragraph of the output — before the full extraction. Inside 30 days triggers immediate escalation.

3. **The MFN Blast Radius Rule**: An MFN clause is never a single-account issue. It constrains pricing decisions across the entire book. Route to Legal and Head of CS immediately — do not treat as a standard yellow flag.

4. **The Price Cap Before Price Increase Rule**: Never run price-increase-prep on an account without first confirming whether a price protection clause exists. The sequence is non-negotiable: contract-review then price-increase-prep.

5. **The Executed-Only Rule**: Contract review on anything other than the signed, executed agreement produces unreliable output. Notes, proposals, and term sheets are not contracts. Flag confidence accordingly.

6. **The Feature Commitment Trap**: Roadmap or feature commitments buried in contracts are material liabilities that surface during renewal negotiation. Always cross-check Category 7 before the renewal call — an unmet commitment changes the entire negotiation dynamic.

7. **The CSM-Is-Not-Legal Rule**: When a clause is ambiguous or non-standard, the response is always "let me confirm with our team" — never an on-the-spot interpretation. Route to Legal, then respond.

---

## Common Failure Modes by Classification Type

### Standard Renewal Extraction Failures
- **Category skip**: Skipping Category 7 (non-standard terms) or Category 8 (governing law) because the contract "looks standard."
  -> Fix: Run all eight categories regardless of initial impression; non-standard terms hide in exhibits.
- **Stale review reuse**: Using a prior extraction without re-reviewing against the current contract version.
  -> Fix: Check contract version date and amendment count against prior review; re-extract if anything changed.

### Amended Contract Failures
- **MSA-only review**: Extracting from the MSA without incorporating amendments.
  -> Fix: Confirm amendment count before extraction; build consolidated term view where amendment governs.
- **Conflict miss**: Failing to identify where amendment language conflicts with MSA.
  -> Fix: For each extracted term, explicitly check whether any amendment addresses the same category.

### Price-Constrained Failures
- **Cap math error**: Misidentifying the price cap percentage, CPI index, or measurement period.
  -> Fix: Extract the exact contract language (verbatim for critical clauses) and validate the math before stating the ceiling.
- **Expansion pricing omission**: Checking the cap for existing seats but missing whether expansion pricing is also protected.
  -> Fix: Always check whether price protections extend to new seats, usage tiers, or expanded scope.

### Time-Critical Failures
- **Buried deadline**: Identifying the notice period but failing to calculate the actual calendar deadline.
  -> Fix: Convert every notice period to a specific calendar date and days-remaining count.
- **Escalation delay**: Surfacing a deadline inside 30 days in the body of the report instead of escalating immediately.
  -> Fix: Any deadline inside 30 days triggers escalation before the full extraction is completed.

### Unverified Source Failures
- **Confidence inflation**: Producing crisp, structured output from unverified sources that reads as authoritative.
  -> Fix: Flag every section `[Low Confidence]` and prepend a warning that blocks commercial decisions.

---

## Expert Judgment Patterns

### Scope Decisions
- If the contract has 0 amendments and standard terms across all categories, a `--summary` output may suffice. If any amendment exists, default to `--extract` regardless of the request.
- When time is short, extract Categories 1-4 (auto-renewal, price protection, termination, notice obligations) first — these are the categories that create legal risk if missed.

### Routing Decisions
- Any red flag routes to Legal before the CSM responds to the customer on that term. No exceptions, no judgment calls.
- Yellow flags with approaching deadlines get treated as red flags for routing purposes — the deadline removes the luxury of monitoring.
- When multiple red flags coexist, route as a single consolidated Legal request, not individual queries.

### Confidence Decisions
- Verified contract from contract system: `[Verified]` on extraction, `[High Confidence]` on implications.
- Uploaded document, not cross-referenced: `[Moderate]` — the document may not be the most current version.
- Notes or verbal input: `[Low Confidence]` across all outputs — block commercial decisions.

### Sequencing Decisions
- Always complete contract-review before negotiation-prep or price-increase-prep. The contract constrains what those skills can recommend.
- If the account is at-risk and has a transition assistance obligation, flag for Finance and Head of CS simultaneously — the cost obligation affects churn economics.

---

*Reasoning Blueprint: Contract Review for Renewals v1.0*
*For use with contract-review when Tier 3 reasoning is activated*
