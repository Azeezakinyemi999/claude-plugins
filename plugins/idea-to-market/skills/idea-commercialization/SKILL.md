---
name: idea-commercialization
description: Plan commercialization for an idea the team has already approved. Reads the latest due-diligence handoff, confirms an approved commitment exists (and stops, naming the missing decision and evidence, if approval is pending, vague, conflicting or needs re-review), then builds a roadmap across MVP, customer validation, go-to-market and operational readiness, plus a detailed plan for the approved next step (for example a capped paid pilot) with owner, scope and timing, spend limit, evidence needed and the next approval gate. Plans only, and never launches, contacts customers, spends or publishes. Use when the user explicitly runs /idea-commercialization with an approved handoff to plan an MVP, pilot, go-to-market test or limited launch.
argument-hint: "[path to handoff.md or idea name] [request]"
disable-model-invocation: true
---

# Idea commercialization

Take an idea that the team has **approved** through due diligence, and plan
how to turn it into a usable offering. The plan covers four phases (MVP,
customer validation, go-to-market and operational readiness), and the next
step gets a detailed plan, inside the approved scope only. Planning is not
authorization: the skill never launches, contacts customers, spends funds or
publishes.

This skill runs only when invoked explicitly (`/idea-commercialization`).
The approval check below applies on every run, including manual ones.

## Hard rules

1. **No approved commitment, no plan.** Read the latest handoff first and
   apply the approval gate in [roadmap-worksheets.md](references/roadmap-worksheets.md).
   If approval is pending, vague, not granted, conflicting or needs
   re-review, stop. Don't produce an active workflow, a roadmap or a plan.
2. **Stay inside the approved scope.** The approved owner, scope, limit and
   success criteria come from the handoff verbatim. Anything beyond them is
   a later gate, described as such.
3. **Planning is not authorization.** No launch, customer contact,
   recruitment messages sent, spending or publishing. Drafts of messages are
   fine if they are labelled as drafts.
4. **Reuse the handoff.** Build on its findings, evidence-log IDs and test
   cards. Research only the gaps this step needs, following
   [sources.md](references/sources.md), with no fabricated numbers. Your own
   memory is not a source.
5. **Write only under `ideas/<idea-id>/commercialization/`.** The handoff
   changes only as [handoff.md](references/handoff.md) allows: recording an
   explicit approval, or a real evidence change, with a version bump. Never
   change the approved scope yourself: send material changes back to the
   team.
6. **Label thresholds the team hasn't set as *proposed*.**

## Files

References, read when the step needs them (in the folder this SKILL.md is
in):

- [references/roadmap-worksheets.md](references/roadmap-worksheets.md): the
  approval gate table, the roadmap, the MVP test card, the validation
  scorecard, go-to-market with the acquisition scorecard, operational
  readiness, and the next-step plan.
- [references/handoff.md](references/handoff.md): the shared handoff
  definition (identical in `idea-due-diligence`).
- [references/sources.md](references/sources.md): the access paths,
  evidence classes and strength, the log fields, and the MCP setup note.
- [references/coaching.md](references/coaching.md): question batches,
  thinking tools, and the ten-step coaching mode.
- [references/examples.md](references/examples.md): short examples. They are
  not defaults.
- [references/methods.md](references/methods.md): method sources.

The idea or handoff path comes from the invocation arguments
(`ARGUMENTS:` below, if any) and the conversation.

## Workflow

### 1 — Find the latest handoff

Use the path given. Otherwise use `ideas/<idea-id>/handoff.md` at the
project root (the git root, else the working directory). If several ideas
exist and none is named, ask which one. Read `handoff.md` (the highest
version), its Change log, `report.md`, `evidence-log.md` and
`test-cards.md`. Look for any other decision record the user supplied
(minutes, email).

### 2 — Approval gate

Apply the gate table. Outcomes:

- **Proceed:** approved, with a defined owner, scope, time or budget limit,
  and success criteria. Quote the commitment exactly.
- **Stop, pending:** say what the team must decide (the commitment and its
  four elements) and which evidence would inform it (from the handoff's
  biggest unknowns). If the user explicitly approves a defined commitment
  now, record it in the handoff as [handoff.md](references/handoff.md)
  describes (version bump, approver, date), then proceed.
- **Stop, re-review or not approved:** report the reason from the Change
  log or the decision.
- **Ask:** if approvals conflict, ask which scope is current.

### 3 — Roadmap

Write `commercialization/roadmap.md` across the four phases, at a depth
matched to the stakes and reversibility:

1. **MVP:** the smallest usable offer that tests one specific risk; the
   real customer task, scope, comparison, measurement, thresholds and next
   decision.
2. **Customer validation:** actual purchase or another appropriate
   commitment, activation, repeated use where relevant, outcome,
   reliability and cost. Report the denominators, the comparison and the
   missing data.
3. **Go-to-market:** the first buyer, positioning against the alternatives,
   price or funding model, sales process, and **one** initial acquisition
   test. Include funnel definitions, acquisition cost, economics, and how
   repeatability will be tested.
4. **Operational readiness:** delivery, support coverage, peak capacity,
   applicable obligations, monitoring, incident response, pause triggers,
   limited launch scope and post-launch review.

Mark each phase as **in scope now** (the approved step) or **later gate**.

### 4 — Plan the approved next step

Write `commercialization/<step>-plan.md` with the next-step plan in the
worksheets: the owner, scope and timing, the spend or resource limit, the
workplan, the evidence needed (measures, denominators, baselines,
thresholds), the pause conditions, and the **next approval decision**. For an
approved **pilot**, define the evidence that would justify a later
limited-launch review, and state that the review is a **fresh gate**.

### 5 — Follow-ups and changes

- **What if** (a different buyer, price or channel for the plan): write
  `commercialization/scenarios/<date>-<slug>.md` comparing it with the
  plan. Say what stays valid, what needs retesting, and whether the
  approved scope would change, in which case it goes back to the team. The
  plan and handoff stay as they are.
- **New results** (pilot data, costs): log them with an evidence class and
  strength, update the validation scorecard, and summarize the delta. If
  they change the approved scope or a key assumption, mark the handoff
  `needs re-review` (version bump) and stop at the gate.
- **Coaching** only when explicitly asked to teach
  ([coaching.md](references/coaching.md)). Otherwise do the work directly.

## Verify

Before you hand off, confirm that:

- The gate outcome is stated first. When it isn't *proceed*, nothing under
  `commercialization/` was created except a note of the gate result, if
  helpful.
- The plan's owner, scope, limit and criteria match the handoff exactly.
  Nothing exceeds them.
- Every metric names its denominator. Thresholds the team hasn't set say
  *proposed*. No number is invented.
- The plan names the next approval decision. A pilot has explicit criteria
  for the launch review.

## Hand-off

Tell the user:

- the gate outcome, and the handoff version and approval it relied on;
- the paths of the files written;
- the approved next step in one paragraph: owner, scope, limit, evidence and
  review date;
- the proposed thresholds the team must confirm;
- what this plan does **not** authorize;
- what the next approval decision is.

## Method sources

Built on Stage-Gate (launch reviews), Eric Ries (MVP), Strategyzer (Test
Card, evidence strength, pricing experiments), MIT Disciplined
Entrepreneurship (first buyer, pricing, acquisition), April Dunford
(positioning) and the AWS Operational Readiness Review (digital services).
Links are in [methods.md](references/methods.md).
