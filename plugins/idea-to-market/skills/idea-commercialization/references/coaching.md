# Questions, thinking tools and coaching

This file is **identical in both skills**. Change both copies together.

## The business brief

Start from the user's decision ("Should we fund a small pilot?") and from
the materials they gave. Build the brief from what is already there, and
label each item **supplied**, **researched**, **assumed** or **unknown**:

| Item | Content | Status |
| --- | --- | --- |
| Idea | one sentence: for whom, what problem or outcome, what offer | |
| User | who experiences the problem | |
| Buyer or funder | who decides, pays, approves or funds | |
| Problem and alternatives | the trigger, the consequence, and the current workaround | |
| Initial segment and geography | the first group that shares a need, a buying process and a reachable channel | |
| Offer | what is delivered, and how | |
| Business model | who pays, how much, how often | |
| Team resources | people, time, money, access and assets | |
| Constraints | deadlines, budget, regulation, safety, IP, data, contracts | |

Do useful provisional work while inputs are missing. Don't block on
unknowns: label them and carry on.

## Asking better questions

Ask **one short batch** (at most five questions), and only for answers that
could change the next investment or test. For each question, state:

1. **What Claude understands so far**, restated in plain language.
2. **The question.**
3. **The decision the answer affects.**

Also:

- Ask for **past behavior** when it's relevant: "Walk me through the last
  time…".
- If the uncertainty needs an **interview, an experiment or a dataset**
  rather than an answer, say so and propose that as the next action, as a
  test card.
- **Reuse** answers that are already in the materials. Don't ask again.
- Ask a follow-up only when it resolves a meaningful ambiguity.
- If nobody can answer (for example, a non-interactive run), put the batch
  in the report under *Questions for the team* and finish the provisional
  work.

Examples:

- "The portal confirms letter receipt and the tracker displays what the
  applicant records. Who updates that status, and when? The answer changes
  the MVP workflow and the staff-cost estimate."
- "Walk me through the last time someone handled this problem. What did
  they do, and what was the consequence? This helps choose the first
  customer problem to test."

Interview prompts that elicit behavior:

- "Walk me through the last time this happened."
- "Tell me about the closest you came to <failure>. What happened?"
- "How did you decide <the key choice>?"
- "What have you tried to make it easier? What did that cost?"

Record observed behavior separately from interpretation. Log stated
interest as stated interest, not as demand.

## Thinking tools (default mode: do the work)

By default, deliver the business work directly. Use these tools inside the
work only where they help, without labelling them as a lesson:

- **80/20:** start with the one question per check whose answer would
  change the commitment.
- **Socratic probes:** what survives the current workaround? What would
  have to be true?
- **Plain-language restatement:** say the idea or the finding the way the
  buyer would.
- **First principles:** break the value, the cost or the risk into the
  steps it really depends on.
- **Schematic:** a small Mermaid or text diagram of the workflow or the
  decision point, when a picture clarifies where the value or the risk sits.

## Coaching mode (only when explicitly asked to teach)

When the user explicitly asks to **learn, be taught or be coached**, run all
ten strategies **in this order**, on the current business question (never
on a canned example). **Every one of the ten**, the last included, ends
with one line: **How this informs the decision or worksheet.**

1. **ELI5:** the idea and the decision in words a child would follow.
2. **80/20:** the few questions or inputs that drive most of the decision.
3. **Mind map:** the idea, its checks, and the open questions under each
   (a Mermaid `mindmap` or a nested list).
4. **Schematic:** the workflow or value chain, highlighting where value or
   risk arises.
5. **First principles:** what must be true for the offer to work, built up
   from the basics.
6. **Socratic questions:** three to five probing questions, each with the
   answer the evidence supports so far.
7. **Feynman teach-back:** a short plain explanation of the case, as the
   learner would give it, and any gaps it reveals.
8. **Visual study guide:** a table, with one row per check, listing what to
   collect before the next decision.
9. **Quiz with worked answers:** two or three questions on this case's
   numbers or decisions, with worked answers.
10. **Sticky notes:** front/back recall cards for the key points.

Write every step in this shape:

```markdown
## <n>. <Strategy name>

<the step, applied to this business>

**How this informs the decision:** <one line naming the decision, check or worksheet field it feeds>
```

Save the result as `ideas/<idea-id>/coaching.md`. **Before saving, check
that all ten `## <n>.` sections exist, in order, and that each one ends
with the `**How this informs the decision:**` line.** Add any that are
missing. Still update the memo and handoff if the work produced new
findings.

A request to **do** the work ("evaluate this", "plan the pilot") gets the
business deliverable directly, not the ten steps.
