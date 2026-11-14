# Shared handoff

The handoff is the one record that carries an idea from due diligence to
commercialization. This file is **identical in both skills**
(`idea-due-diligence` and `idea-commercialization`). Change both copies
together.

## Where it lives

- Current version: `ideas/<idea-id>/handoff.md` at the project root (the git
  root, else the working directory).
- Every replaced version is kept unchanged as
  `ideas/<idea-id>/handoff-history/v<N>.md`.

## Rules

1. **One current version.** Increment `Version` (v1, v2, …) whenever a
   finding, evidence link, assumption, scope or approval field changes.
   Copy the old file to `handoff-history/` first, then add a row to the
   Change log.
2. **Claude's recommendation and the team's decision are separate fields.**
   Never fill a team-decision field from Claude's own recommendation.
3. **Approval status** takes exactly one of these values:
   - `pending`: no team decision is recorded yet. This is the default, and a
     handoff is still produced.
   - `approved`: the user explicitly approved a *defined* commercialization
     commitment in the conversation (owner, scope, time or budget limit,
     success criteria), or supplied an equivalent documented team decision
     (minutes, email, signed memo), cited under Decision evidence. "Looks
     good", or approval with no defined commitment, stays `pending`.
   - `not approved`: the team decided Hold, Stop or Reshape.
   - `needs re-review`: evidence changed the approved scope or a key
     assumption after approval. Commercialization must not proceed on the
     old approval.
4. **"What if" scenarios never change this file.** They are working
   comparisons saved in `ideas/<idea-id>/scenarios/`.
5. **When evidence changes**, summarize the delta in the Change log, revise
   the affected findings, and list which evidence still applies. If the
   change materially alters the approved scope or a key assumption, set
   status to `needs re-review` and state what the team must decide again.
6. **Keep it small and human-readable.** Cite evidence-log IDs (E1, E2 …)
   instead of copying evidence into the handoff.

## Template

````markdown
# Handoff — <Idea name>

| Field | Value |
| --- | --- |
| Idea ID | <idea-id> |
| Version | v<N> |
| Owner | <name, or TBD> |
| Date | <YYYY-MM-DD> |
| Evidence cutoff | <YYYY-MM-DD: latest evidence considered> |

## Claude recommendation
- **Recommendation:** Advance | Test further | Reshape | Hold | Stop
- **Rationale:** <2–4 lines citing evidence-log IDs>

## Team decision
- **Decision:** <the team's decision, or "none recorded">
- **Approval status:** pending | approved | not approved | needs re-review
- **Approver:** <name and role, or —>
- **Decision date:** <YYYY-MM-DD, or —>
- **Decision evidence:** <"approved by <name> in session on <date>", or a link to minutes or email, or —>
- **Exact next commitment:** <e.g. "capped paid pilot: 30 participants, 6 weeks, ≤ $1,500", or "none until approved">

## Agreed target
- **Segment and geography:** …
- **User:** …
- **Buyer or funder:** …
- **Problem:** …
- **Offer hypothesis:** …

## Due diligence findings
| Check | Finding | Evidence (log IDs, links) | Strength (reason) | Main uncertainty |
| --- | --- | --- | --- | --- |
| Customer problem | | | | |
| Market opportunity | | | | |
| Strategic fit | | | | |
| Feasibility and economics | | | | |

## Open assumptions, blocking risks and constraints
- **Open assumptions:** …
- **Blocking risks:** …
- **Applicable constraints** (regulatory, safety, IP, data, contractual): …

## Approved scope
<Filled only when Approval status is `approved`; otherwise "Not approved yet".>
- **Scope:** …
- **Time or budget limit:** …
- **Owner:** …
- **Success criteria:** …
- **Pause conditions:** …
- **Review date:** …

## Change log
| Version | Date | Change | Evidence still applying | Effect on recommendation or approval |
| --- | --- | --- | --- | --- |
| v1 | <date> | Created from due diligence | — | — |
````
