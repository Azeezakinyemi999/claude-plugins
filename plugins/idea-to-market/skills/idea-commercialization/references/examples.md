# Short examples

These are illustrations only. **Their numbers and segments are not
defaults.**

## Approval pending: no active workflow

> **Handoff v1 (bike-repair van): approval status `pending`.** Claude
> recommended *Advance* to a pilot, but no team decision is recorded.
>
> I won't start a commercialization plan yet. To approve, the team needs to
> record:
>
> - an **owner**;
> - the **scope** (e.g. "one park, rider-paid");
> - a **time or budget limit**;
> - the **success criteria**.
>
> Before deciding, the team may also want evidence on E5 (willingness to
> pay at the pilot price), which is still an assumption. Record the decision
> with `/idea-due-diligence <idea> approve …`, or attach the minutes.

## Approved pilot: the plan's shape

- **Approved commitment (handoff v2, approved by the ops lead on
  2026-03-02):** a capped paid pilot at two parks, at most 40 riders, 6
  weeks, ≤ $1,200 spend.
- **Objective:** retire R1 (paid demand at the pilot price) and R2 (labor
  per repair within budget).
- **Evidence needed:**
  - paid bookings ÷ unique riders who saw the offer;
  - repeat bookings ÷ first-time customers;
  - labor minutes per repair (median and peak day);
  - defects ÷ repairs.
- **Thresholds (proposed, team to confirm):** ≥ 4% booking; ≤ 35 labor
  minutes per repair; 0 safety incidents.
- **Next approval decision:** a limited-launch review on 2026-04-20. This is
  a **fresh gate**: the pilot results go back to the team, and the plan
  doesn't authorize a launch.

## Conflicting approvals

> The handoff (v3) approves a **one-park pilot**, but the supplied minutes
> dated a week later mention a **three-park launch**. Which scope is
> current? I'll plan against that one, and the handoff should be updated to
> match.
