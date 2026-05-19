# Downgrade Driver Taxonomy

**Used by:** `renewals:downgrade-analysis`
**Purpose:** Authoritative definitions, signal vocabulary, diagnostic questions, and mixed-signal handling for the 5 downgrade driver categories.

---

## Driver Category Definitions

### 1. `budget_pressure`

**Definition:** The customer is contracting primarily because of cost constraints, budget reductions, or a need to demonstrate spend reduction. The value of the product may be acknowledged, but the spend cannot be justified in the current financial environment.

**Key characteristic:** The driver is financial — not product-driven. The customer would likely retain the full contract if budget were not a constraint.

**Signal vocabulary:**
- "cutting costs," "reducing spend," "budget freeze," "CFO mandate"
- "too expensive," "overpaying," "can't justify the price," "price increase"
- "ROI question," "need to show savings," "renegotiate pricing"
- "financial pressure," "cost reduction initiative," "belt tightening"
- "afford," "budget cuts," "budget cycle," "fiscal constraints"

**Diagnostic questions to confirm or refine:**
1. Is this a time-bounded constraint (e.g., 90-day freeze, Q2 cut) or an ongoing budget change?
2. Is the budget driver a mandate from finance/CFO, or is the champion choosing to reduce spend?
3. Has the customer expressed satisfaction with the product itself, separate from cost?
4. Is there a specific budget number they need to hit, or is it "as low as possible"?
5. Have pricing or payment terms been discussed as an alternative to a tier change?

---

### 2. `reduced_scope`

**Definition:** The customer's legitimate need for the product has contracted. Fewer users, reduced volume, smaller team size, or organizational restructuring means they no longer need the same scale of product.

**Key characteristic:** The driver is organizational — not dissatisfaction or budget. The customer is trying to right-size to actual usage, not avoid paying for value they receive.

**Signal vocabulary:**
- "team shrank," "headcount reduction," "layoffs," "restructuring"
- "fewer users," "less volume," "reduced seats needed," "smaller team"
- "department eliminated," "project ended," "use case went away"
- "we only need X users now," "half the team is gone"
- "org change," "merger," "acquisition," "reorganization"

**Diagnostic questions to confirm or refine:**
1. Is the headcount reduction permanent or temporary (e.g., hiring freeze)?
2. Are there other teams or departments that could absorb the unused licenses?
3. Is this a company-wide contraction or limited to the team using this product?
4. Would a seat-level adjustment (partial reduction) satisfy their need, or are they looking for tier/module changes?
5. Is there a growth scenario on the horizon (new hire plan, expansion plan) that makes a temporary accommodation better than a full downgrade?

---

### 3. `feature_underutilization`

**Definition:** The customer believes they are paying for capabilities they are not using and sees no path to using them. The product may be functioning correctly, but adoption is low and the full value proposition has not been realized.

**Key characteristic:** The driver is adoption/complexity — not budget or org change. The customer's contract scope exceeds their actual consumption.

**Signal vocabulary:**
- "not using all the features," "only using a fraction of it"
- "too complex," "we don't need everything," "paying for things we don't use"
- "our team only uses X," "the rest of the features don't apply to us"
- "overpowered for our needs," "simpler tool would work"
- "adoption has been low," "not getting full value"

**Diagnostic questions to confirm or refine:**
1. Which specific features or modules are they not using? Were those ever in scope?
2. Was there a plan to expand usage to those features? If so, what blocked adoption?
3. Is the underutilization a training/onboarding gap, or is the use case genuinely absent?
4. Has the CSM done a feature audit with the champion in the last 90 days?
5. Are there alternative use cases within their organization that could absorb the unused capacity?

---

### 4. `competitive_pressure`

**Definition:** The customer is considering or actively evaluating a competing product, often citing lower cost or specific feature gaps. The downgrade may be a negotiating tactic, or a transition step before full churn.

**Key characteristic:** This category has the highest churn escalation risk. A "downgrade" motivated by competitive pressure may become full churn if the competitor wins.

**Signal vocabulary:**
- "competitor," "alternative," "evaluating other vendors," "comparing tools"
- "switching," "looking at other options," "demo with another provider"
- "cheaper tool," "does the same thing for less," "market alternatives"
- "your competitor," "we've been approached by," "looking at X platform"
- "vendor consolidation," "rationalizing our stack"

**Diagnostic questions to confirm or refine:**
1. Is the competitive evaluation already underway, or is it a threat/negotiating position?
2. Which competitor is being considered? What is the primary attraction (price, features, brand)?
3. Is this a champion-level decision or has it reached economic buyer/procurement?
4. What would it take to keep the account at current scope?
5. Has there been a trigger event (contract renewal, new leadership, budget review) that opened the door to competitive evaluation?

**Escalation note:** If the customer names a specific competitor and is already in an evaluation, this warrants immediate escalation to leadership and/or an exec sponsor engagement.

---

### 5. `dissatisfaction`

**Definition:** The customer is contracting because they are unhappy with the product, the service, or outcomes delivered. The downgrade reflects loss of confidence and may precede full churn if not addressed.

**Key characteristic:** This is the highest-urgency driver category from a retention risk perspective. Unresolved dissatisfaction typically escalates to churn.

**Signal vocabulary:**
- "problems," "issues," "bugs," "broken," "not working properly"
- "unhappy," "frustrated," "disappointed," "let down"
- "support is slow," "no one responds," "escalation not resolved"
- "promised X and didn't deliver," "expectations not met"
- "not what we were sold," "implementation was rough," "poor experience"
- "lost confidence," "trust issue," "management is questioning the tool"

**Diagnostic questions to confirm or refine:**
1. What specific incident(s) drove the dissatisfaction — product, support, CSM, or implementation?
2. Has a formal complaint or escalation already been filed?
3. Is the dissatisfaction coming from the end users, the champion, or the economic buyer?
4. Has anything been done to address the issue? If so, was the customer satisfied with the response?
5. Is the customer open to a remediation path, or have they already decided?

---

## Mixed-Signal Handling

Real downgrade requests often contain signals from more than one driver category. This section defines how to identify primary vs secondary drivers and how to report mixed signals.

### Identification rules

**Primary driver:** The driver category with the strongest, most explicit, or most actionable signal in the `downgrade_request`. "CFO mandate to cut all software spend by 20%" is a strong explicit budget_pressure signal even if the request also mentions low adoption.

**Secondary driver:** Any additional category with meaningful signal presence. Report secondary drivers as contributing factors, not co-equal causes.

### Common mixed-signal combinations

| Combination | Interpretation |
|-------------|---------------|
| budget_pressure + feature_underutilization | Budget is the forcing function; low adoption gives the champion justification to agree. Address adoption gap even if budget relief is the primary lever. |
| feature_underutilization + dissatisfaction | Low adoption likely caused by a product/support failure, not genuine lack of use case. Treat as dissatisfaction with adoption-failure evidence. |
| competitive_pressure + dissatisfaction | High churn risk. Competitor is filling a gap created by dissatisfaction. Escalate immediately. |
| reduced_scope + budget_pressure | Org change created natural right-sizing opportunity that budget constraints are accelerating. Both drivers are independent and real. |
| competitive_pressure + budget_pressure | Competitive evaluation opened because budget pressure created a "good reason to look." Address budget first; competitive threat may resolve. |

### Reporting format for mixed signals
In the analysis output, report: "Primary driver: [category]. Secondary signal: [category] — [brief rationale for why it is secondary]."
