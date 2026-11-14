---
name: idea-due-diligence
description: Evaluate a software, physical-product, service or funded-initiative idea before the team commits more resources. Builds a business brief from a paragraph and any supplied materials, researches claims where tools allow, runs four checks (customer problem, market opportunity, strategic fit, feasibility and economics), and writes a one-page decision memo recommending Advance, Test further, Reshape, Hold or Stop, with an evidence log, test cards and a versioned handoff whose approval stays pending until the team approves. Also answers follow-up and what-if questions against the report and revises findings when evidence changes. Use when the user asks to evaluate, vet, screen, sanity-check or do due diligence on an idea, asks whether an idea is worth pursuing or piloting, approves a commitment for an evaluated idea, or asks a what-if about an existing idea report.
argument-hint: "[idea paragraph] [paths to materials]"
---

# Idea due diligence

Turn an idea (one paragraph, plus any materials) into evidence for a team
decision: **should we commit more resources, and how much?** The skill
recommends; the team decides. It never contacts customers, spends money,
publishes, or treats its own recommendation as approval.

## Hard rules

1. **Write only under `ideas/<idea-id>/`** at the project root (the git
   root, else the working directory): `report.md`, `evidence-log.md`,
   `test-cards.md`, `handoff.md`, `handoff-history/`, `scenarios/`, and
   `coaching.md` (coaching mode only). Never edit supplied materials.
2. **No fabricated evidence.** Every number is sourced, a labelled estimate
   with its calculation, or a labelled assumption. Never invent an
   interview, a purchase, a dataset or a result. Your own memory is not a
   source: without web tools, public research did not run, and external
   figures stay as named variables (see [sources.md](references/sources.md)).
3. **The recommendation is not approval.** The handoff's approval status is
   `pending` unless the user explicitly approves a *defined* commitment
   (owner, scope, time or budget limit, success criteria), or supplies an
   equivalent documented team decision. Rules in [handoff.md](references/handoff.md).
4. **"What if" never edits the approved record.** Scenarios go in
   `scenarios/`. Only real new evidence revises the handoff, with a version
   bump and a delta.
5. **Nothing outward without a yes:** no customer contact, surveys, spending,
   publishing, or sending confidential files to third parties. Search the
   web with generic terms only.
6. **Say which research paths actually ran.** Public research, structured
   access, direct evidence: none is implied if it didn't run.

## Files

References, read when the step needs them (in the folder this SKILL.md is
in):

- [references/worksheets.md](references/worksheets.md): the report layout,
  the decision memo, the four check worksheets, the test card, the scenario
  comparison and the evidence delta.
- [references/sources.md](references/sources.md): the three access paths,
  source choice, evidence classes, strength, log fields, and the MCP setup
  note.
- [references/handoff.md](references/handoff.md): the shared handoff
  definition and template (identical in `idea-commercialization`).
- [references/coaching.md](references/coaching.md): the business brief,
  question batches, thinking tools, and the ten-step coaching mode.
- [references/examples.md](references/examples.md): short examples. They are
  not defaults.
- [references/methods.md](references/methods.md): method sources.

The idea comes from the invocation arguments (`ARGUMENTS:` below, if any)
and the conversation. Read every supplied file first.

## Workflow

### 0 — Route the request

- **Pick the idea ID:** a short kebab-case slug of the idea name. If
  `ideas/<idea-id>/` already exists, read `handoff.md`, `report.md` and
  `evidence-log.md`, then route:
  - a **question** about the report → answer it from the report, citing
    sections and log IDs;
  - a **"what if"** → [Scenarios](#scenarios-and-evidence-changes);
  - **new evidence** → [Evidence changes](#scenarios-and-evidence-changes);
  - an **approval** → [Approval](#approval).
- **Coaching vs doing:** run the ten-step coaching mode in
  [coaching.md](references/coaching.md) only when the user explicitly asks to
  be taught or coached. Otherwise deliver the business work directly.

### 1 — Business brief

Start from the user's decision: what are they being asked to commit? Fill
in the brief table from [coaching.md](references/coaching.md) using the
materials first, labelling each item supplied, researched, assumed or
unknown. Keep going provisionally where items are missing.

### 2 — Four checks, three lenses

For each check, apply **(a) understand** the concept and its constraints,
**(b) evidence**: check external and direct evidence, and **(c) challenge**
the case from the customer's side and the delivery side. Use the worksheets.

1. **Customer problem:** the user, the buyer or funder, the current
   alternative, frequency, severity, and evidence from **actual behavior**.
2. **Market opportunity:** the first segment; a count of **unique**
   plausible buyers or accounts; spend or funding; alternatives. Keep
   **market potential** separate from a **forecast** constrained by reach,
   conversion and delivery capacity.
3. **Strategic fit:** goals, access, strengths, ownership, capability and
   capacity gaps, build / buy / partner options, and opportunity cost.
4. **Feasibility and economics:** technical and operational risks, plus
   regulatory, safety, IP and data risks where they apply. Estimate unit
   contribution and break-even where meaningful. Document the inputs and
   scenarios, and flag any constraint that could block the next commitment.

**Research:** follow [sources.md](references/sources.md). Run public
research where web tools exist, choosing sources from the segment,
geography and question. Use structured access only if it is already
configured. Use direct evidence from the team. Log every material claim in
`evidence-log.md`, with its class and its qualitative strength and reason.

### 3 — Questions

Prepare **one batch** of at most five questions whose answers could change
the next investment or test. For each, give what you understand, the
question, and the decision it affects (format in
[coaching.md](references/coaching.md)). Ask about past behavior. Where an
interview, an experiment or a dataset is needed, propose it as a test card.
Ask in chat when someone can answer. Always list the batch in the report
too.

### 4 — Write the outputs

1. `report.md`: the **decision memo first** (one page), then the questions,
   the four checks, the calculations and the brief
   ([worksheets.md](references/worksheets.md)).
2. `evidence-log.md`, and `test-cards.md` for every assumption that the
   next decision depends on and that desk research can't settle.
3. `handoff.md` from the [template](references/handoff.md), **always
   produced**, with status `pending` unless approval exists.
4. In chat, the short decision brief: the recommendation, the strongest
   evidence, the biggest unknown, the next test or decision, and the
   questions.

### Approval

Upgrade the handoff to `approved` **only** when the user explicitly approves
a defined commercialization commitment (owner, scope, time or budget limit,
success criteria, ideally with pause conditions and a review date), or
supplies a documented team decision. If any element is missing, ask for
it: the status stays `pending`. On approval, bump the version, archive the
old handoff, fill in the Team decision and Approved scope sections, and add
a Change log row. Claude's recommendation stays as written.

### Scenarios and evidence changes

- **What if** (a changed buyer, price, segment or channel): write
  `scenarios/<date>-<slug>.md` using the comparison in
  [worksheets.md](references/worksheets.md). Show the recalculated numbers,
  what stays valid, what needs retesting, whether the recommendation
  changes, and whether the approval scope would change. The handoff stays
  untouched.
- **Evidence changed** (new data, results or facts): add the log rows,
  revise the affected findings, and write the evidence delta. Bump and
  archive the handoff. If the approved scope or a key assumption materially
  changes, set status `needs re-review` and say what the team must decide.

## Verify

Before you hand off, confirm that:

- The memo fits about one page and leads the report. The recommendation is
  one of the five options, with its reason.
- Every number in the report is sourced, an estimate with its calculation,
  or an assumption. Nothing is invented, and no external figure comes from
  memory. The research paths that actually ran are stated.
- Each check has a finding, its evidence (IDs), its strength with a reason,
  and its main uncertainty.
- Every test card has all its fields. Thresholds the team hasn't set are
  marked *proposed*.
- The handoff matches the template. Its status follows the approval rule,
  and the recommendation and team-decision fields are separate.
- Coaching mode only: `coaching.md` has all ten steps in order, each
  ending with its **How this informs the decision** line.

## Hand-off

Tell the user:

- the recommendation and the one-line reason;
- the strongest evidence and the biggest unknown;
- the next test or decision;
- the questions (if not already asked);
- which research paths ran;
- the paths of the files written;
- that approval is pending, with what the team must define to approve
  (owner, scope, limit, success criteria);
- that `/idea-commercialization` starts only after approval.

## Method sources

The four checks and the decision step are the team's own process. They
borrow from Stage-Gate (gates), MIT Disciplined Entrepreneurship (first
market, sizing, pricing), NSF I-Corps and YC (customer discovery), SBA
(market research, break-even) and Strategyzer (Test Card, evidence
strength). Links are in [methods.md](references/methods.md).
