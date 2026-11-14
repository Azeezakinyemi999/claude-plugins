# Due diligence worksheets

These worksheets are adapted from the team's *Idea Evaluation and
Commercialization Template*. Complete only the parts that the next
commitment depends on. Write *N/A — <reason>* when a part doesn't apply, and
record unknowns explicitly.

## report.md layout

```text
# <Idea name> — due diligence (v<N>, <date>)
Research paths: <which of the three paths ran>        ← sources.md
## Decision memo                                        ← one page, first
## Questions for the team                               ← the batch, with reasons
## 1 Customer problem                                   ← findings, then the three lenses
## 2 Market opportunity
## 3 Strategic fit
## 4 Feasibility and economics
## Calculations                                         ← every formula, with inputs and their log IDs
## Business brief                                       ← coaching.md table, with statuses
```

Organise each check through the **three lenses**:

- **(a) Understand:** the concept and its constraints, as the team states
  them.
- **(b) Evidence:** what external and direct evidence shows, citing log IDs.
- **(c) Challenge:** the case from the customer's side and from the
  delivery side.

Then give the check's finding and its evidence strength, with the reason.

## Decision memo (one page)

| Field | Content |
| --- | --- |
| Idea and version | <name, v<N>, date, owner> |
| Decision requested | <e.g. approve discovery, pilot, limited launch, expansion> |
| Idea in one sentence | <for whom, what problem or outcome, what offer> |
| Customer problem | <workaround, consequence, strongest evidence (ID)> |
| Market opportunity | <first segment, reachable unique buyers, spend or funding, source> |
| Strategic fit | <goal served, advantage, capability gap, competing priority> |
| Feasibility and economics | <can we deliver safely and reliably? price or funding, cost to serve, critical constraint> |
| Strongest evidence | <what was observed (ID)> |
| Biggest unknown | <what could change the decision> |
| **Claude recommendation** | **Advance / Test further / Reshape / Hold / Stop**: <one-line reason> |
| Next test or decision | <test card ID, or the decision the team must make> |
| Team decision | <pending, or the recorded decision (see handoff)> |

The five options:

- **Advance:** the evidence supports the next planned commitment.
- **Test further:** a targeted experiment can resolve a key unknown.
- **Reshape:** change the customer, the offer or the approach, because the
  evidence points elsewhere.
- **Hold:** timing or resources prevent action now.
- **Stop:** the case is too weak to justify more work.

## 1. Customer problem

- **User and buyer:** who experiences the problem, and who decides, pays,
  approves or funds it.
- **Problem statement:** *<specific group> struggles to <job> when
  <trigger>, leading to <consequence>. Today they <workaround>.*
- **Frequency and severity:** how often it happens, and what it costs when
  it happens.
- **Evidence from actual behavior:** workarounds people already pay for or
  spend time on, incidents and outcomes. Keep stated interest separate.
- **Interview scope**, if evidence is thin: whom to recruit, how to reach
  them, and which recent occurrence to ask about.

| Claim or question | Evidence and source | Strength and next check |
| --- | --- | --- |
| <claim> | <observation or quote, segment, date, log ID> | <hypothesis / early signal / repeated evidence; next check> |

## 2. Market opportunity

- **Scope and unit:** geography, segment, period, and the count of
  **unique** buyers or accounts. Count buyers, not transactions; if only
  transactions are known, state the per-buyer assumption.
- **Market potential:** `eligible unique buyers × plausible spend per buyer
  per period`, with sources.
- **Serviceable and initial market:** which buyers the offer can serve, and
  which first group shares a need, a buying process and a reachable
  channel.
- **First-period forecast (separate from potential):**
  `min(qualified offer exposure × paid conversion, delivery capacity) × net price`.
- **Sensitivity:** low / base / high cases, overlapping reach (count unique
  people), alternatives, growth, and the assumptions to verify first.

Potential is not a forecast. Reach, conversion and capacity constrain the
forecast, and conversion from another offer or cohort doesn't transfer.

## 3. Strategic fit

| Criterion | Assessment and evidence | Action |
| --- | --- | --- |
| Goal alignment | <goal served; brand fit> | |
| Customer access | <permission and channel to reach the first segment> | |
| Strengths and ownership | <assets, expertise, IP, who owns the result> | |
| Capability and capacity gaps | <capability, owner, availability, peak load> | build / buy / partner, cost |
| Opportunity cost | <what is delayed or displaced, and its value> | time budget |

A gap is critical when it threatens the central customer promise or
on-time delivery.

## 4. Feasibility and economics

**Risk register:**

| Risk or constraint | Applies? | Evidence or next test | Owner and decision trigger |
| --- | --- | --- | --- |
| Technical or delivery | | <proof required, dependencies, capacity> | |
| Operational (support, peak load, supply) | | | |
| Regulatory, legal or safety | | <the applicable rules and checks> | |
| IP | | | |
| Data and privacy | | <required fields, access, retention, deletion> | |
| Other critical unknown | | <test, mitigation> | |

Mark any constraint that could **block the next commitment**.

**Unit economics**, where meaningful:

| Field | Value and source |
| --- | --- |
| Unit and period | <order, account, customer, project or funded outcome> |
| Net revenue or funding per unit | <price less discounts and refunds> |
| Variable cost per unit | <materials, labor (including founder or volunteer time), fulfilment, fees, attributable acquisition. Count each cost once.> |
| Contribution per unit | `net revenue − variable cost` |
| Break-even volume | `fixed costs ÷ positive contribution`, rounded up; compare with attainable volume and capacity |

Show low / base / high scenarios when the inputs are uncertain. If
contribution is zero or negative, say so, and test a change in cost, scope,
price or funding before any volume plan.

## Test card (`test-cards.md`)

Write one card for each assumption that the next decision depends on and
that desk research can't settle.

| Field | Content |
| --- | --- |
| ID | T1 |
| Assumption | We believe <specific customer> will <action or outcome>. |
| Method | <interview, landing page, concierge or paid pilot, pre-order, observation …> |
| Sample or population | <who, how recruited, and how many> |
| Measure and denominator | <metric> out of <the people it is measured against> |
| Baseline | <current workaround performance, where appropriate> |
| Success threshold | <value>: *proposed, team to confirm* unless the team set it |
| Failure threshold | <value or condition> |
| Owner | <name, or TBD> |
| Limits | <scope, cost ceiling, time box> |
| Next decision | if met → <X>; if missed or inconclusive → <Y> |

## Scenario comparison (`scenarios/<date>-<slug>.md`)

A scenario is a **working comparison**. It never changes the handoff.

| Item | Baseline (handoff v<N>) | Scenario | Change |
| --- | --- | --- | --- |
| <changed input: buyer, price, segment …> | | | |
| <recalculated outputs: potential, forecast, contribution, break-even> | | | |

Then answer four questions:

- **Still valid:** which findings and evidence (IDs) still apply unchanged?
- **Needs retesting:** which findings depend on evidence that no longer
  applies? For example, conversion measured with a different buyer or price.
- **Recommendation:** does it change, and why?
- **Approval scope:** would the approved commitment change? If yes, it goes
  back to the team.

## Evidence delta (when evidence really changes)

| What changed | Source (ID) | Findings affected | Evidence still applying | Recommendation effect | Approval-scope effect |
| --- | --- | --- | --- | --- | --- |
