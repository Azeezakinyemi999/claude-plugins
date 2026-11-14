# Commercialization worksheets

These worksheets are adapted from the team's *Idea Evaluation and
Commercialization Template*. Match the depth to the stakes and how
reversible the step is. Mark a part that doesn't apply *N/A — <reason>*.
Any threshold the team hasn't set is written as ***proposed: team to
confirm***.

## Approval gate (run first, every time)

| Handoff state | What to do |
| --- | --- |
| `approved` with a defined commitment (owner, scope, limit, success criteria) | Plan **only** that commitment. If it is a pilot, also define the evidence that would earn a later launch review. |
| `approved` but the commitment is vague (missing owner, scope, limit or criteria) | Treat it as pending. Name the missing elements, and stop. |
| `pending` | Stop. State the missing decision and evidence, and what the approval must specify. Produce no roadmap or plan. |
| `not approved` | Stop. Report the team's decision. |
| `needs re-review` | Stop. List what changed (Change log), and what the team must decide again. |
| Conflicting approvals (handoff vs another record, or two scopes) | Ask which scope is current. Don't pick one. |
| No handoff found | Stop, and point to `/idea-due-diligence`. |

## Roadmap (`commercialization/roadmap.md`)

| Phase | Output and evidence to review | Owner and review date | Status |
| --- | --- | --- | --- |
| 1 MVP | <smallest usable offer, core task, riskiest assumption, threshold> | | planned / in scope now / later gate |
| 2 Customer validation | <purchase or commitment, activation, continued use, outcome, reliability, cost> | | |
| 3 Go-to-market | <initial buyer, positioning, price or funding, channel, funnel, acquisition cost> | | |
| 4 Operational readiness | <delivery, support, capacity, obligations, monitoring, incidents, pause triggers> | | |

Recruiting a pilot can also test a channel. Operational constraints can
shrink the MVP scope. Update the roadmap as evidence changes.

## 1. MVP and its test card

| Field | Content |
| --- | --- |
| Risk tested | <the specific riskiest assumption> |
| Real customer task | <the job, performed under realistic conditions> |
| MVP scope | <core task, simplest usable offer, excluded features> |
| Comparison | <the current workaround, a baseline or a control> |
| Experiment | <recruitment, method, sample, dates, owner> |
| Measures and thresholds | <metric, its denominator, success threshold, critical failure conditions> |
| Next decision | if met → <X>; if missed or inconclusive → <Y>; budget and time cap |

## 2. Customer validation scorecard

| Measure | Target / actual | Denominator and interpretation |
| --- | --- | --- |
| Demand or commitment | / | purchases or costly commitments ÷ qualified people offered |
| Activation (first value) | / | reached first valuable action ÷ buyers |
| Continued use (where relevant) | / | active at <time> ÷ activated |
| Customer outcome | / | against the baseline or comparison |
| Reliability | / | incidents, defects, errors that matter to the customer |
| Cost to serve | / | labor and other variable cost per unit, including peak |

Report the **missing data**, any differences from the planned test, sample
limits, and alternative explanations. Report each metric with its own
denominator, and report end-to-end rates as well.

## 3. Go-to-market

| Field | Content |
| --- | --- |
| Initial buyer and trigger | <who buys first, who influences, what makes the need timely> |
| Current alternatives | <what the buyer would do or buy today> |
| Positioning and proof | For <buyer>, the offer delivers <outcome> relative to <alternative>. Evidence: <IDs>. |
| Offer and price or funding | <scope, terms, price or funding mechanism; pricing test> |
| Sales process | <how buyers discover, evaluate, approve, buy and start> |
| Initial acquisition test | <audience, message, timing, owner, budget, threshold, second cohort to test repeatability> |

**Acquisition scorecard.** Name the denominator at every step.

| Funnel stage | Definition | Target / actual |
| --- | --- | --- |
| Qualified exposure | unique eligible buyers who actually saw the offer | / |
| Evaluation | buyers taking a meaningful next action | / |
| Purchase or commitment | new paying or committed buyers | / |
| Activation | buyers reaching first value | / |
| Acquisition cost | attributable spend + labor ÷ new buyers | / |
| Economics | contribution after acquisition = net price − variable cost − acquisition cost | / |

A channel is **repeatable** when a second, separate cohort reaches suitable
buyers at an acquisition cost the unit economics can support.

## 4. Operational readiness

For each row, mark **Ready**, **Open** or **N/A (reason)**. Flag the
launch-critical rows.

| Check | Evidence to provide | Owner, status, date |
| --- | --- | --- |
| Delivery and quality | critical workflows, acceptance checks, defects, supply or service capacity | |
| Support coverage | primary and backup owners, hours, escalation | |
| Peak capacity | load in the busiest period vs available hours; cohort or volume cap | |
| Applicable obligations | safety, legal, privacy, security, sector, supplier | |
| Monitoring | customer outcomes, fulfilment, issues, refunds, cost; decision thresholds | |
| Incident response | detection, escalation, containment, recovery or rollback, communications | |
| Pause triggers | the failure, incident or workload that pauses enrolment, and who acts | |
| Limited launch scope | cohort or volume cap, start date, approver | |
| Post-launch review | date, metrics, owners, evidence expected | |

For digital services, adapt the
[AWS Operational Readiness Review](https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_ready_to_support_const_orr.html).

## Next-step plan (`commercialization/<step>-plan.md`)

| Field | Content |
| --- | --- |
| Approved commitment | quoted exactly from the handoff (version, approver, date) |
| Objective | the risk this step retires |
| Owner | from the handoff |
| Scope and timing | what is in and out; start, milestones, end |
| Spend or resource limit | from the handoff; the plan stays inside it |
| Workplan | the steps, each with an owner and a date |
| Evidence needed | the measures, denominators, baselines and thresholds (*proposed* where unset) |
| Pause conditions | from the handoff, plus any found while planning |
| Next approval decision | what the team decides at the end, on which evidence, and the date. For a pilot: the criteria for a **limited-launch review**, which is a fresh gate |
| Not authorized by this plan | launch, customer contact, spend or publishing beyond the approved scope |

## Business model snapshot (optional)

| Block | Content |
| --- | --- |
| Customer segments and value | first user and buyer, job, offer, why switch |
| Channels and relationships | how buyers find, buy, receive and get support |
| Activities, resources, partners | the critical work, people, tools, suppliers |
| Revenue and cost structure | who pays, how much and how often; the cost drivers |
| Key assumptions | the claims that could invalidate the model, linked to tests |

## Gate review record

At each review, record the evidence, the unresolved risks, the decision,
the owner, the review date, and the maximum resources committed. The team
records the decision in the handoff (through `/idea-due-diligence`, or
directly as a documented decision).
