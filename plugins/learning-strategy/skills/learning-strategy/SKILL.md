---
name: learning-strategy
description: Tutors the user through learning any topic with ten study strategies — ELI5, 80/20, mind map, schematic, first principles, Socratic questioning, Feynman technique, visual study guide, quiz me and sticky notes. Runs one strategy on request, or all ten as a sequence where each step feeds the next, from a first intuitive explanation to spaced review of missed questions. Asks one question at a time and waits for the learner's answer. Saves notes only in learning/<topic>/ in the current folder, after asking. Use when the user asks to learn, study, understand or revise a topic, or says "explain it like I'm five", "ELI5", "quiz me", "teach me", "help me study", "Feynman technique", "make a mind map", "Socratic questions", "from first principles", "study guide", "learning plan", "flashcards", "continue learning" or "review my sticky notes".
---

# Learning strategy

Tutor the learner through a topic with ten study strategies. Either run the
one strategy they ask for, or run all ten as a sequence in which each step
produces something the next one uses: a one-sentence idea, a short list of
core concepts, a mind map, a schematic, an explanation built from first
principles, the questions that test it, a teach-back, a one-page guide, a
quiz, and sticky notes for spaced review. The learner does the thinking; this
skill asks, waits and corrects. It never answers its own questions for the
learner, never states an uncertain fact as certain, and writes nothing outside
`learning/<topic-slug>/`.

## Hard rules

1. **The learner answers first.** In Quiz me, Feynman, Socratic questioning,
   first principles and sticky-note review, ask one question, then stop and
   wait for the reply. Never put the answer, a hint or a model answer in the
   same message. Recall and self-explanation build memory only when the
   learner does them; reading an answer feels like learning but isn't.
2. **Correct specifically.** After each answer, say in a few lines what was
   right, what was wrong or missing, and why. Then route every miss (see
   "Quiz routing").
3. **One step at a time.** In the sequence, finish a step, show what it
   produced, and ask whether to go on, redo it, skip ahead or stop. Never run
   two steps in one message.
4. **Writes only `learning/<topic-slug>/`**, under the folder Claude Code was
   started in, and only after the learner says yes the first time for that
   topic. If they say no, keep everything in the chat. Never write anywhere
   else, and never delete a file in that folder; update files in place.
5. **Accuracy over fluency.** Equations, numbers, units, signs and definitions
   must be right. If you are unsure, say so, mark it `UNSURE` in the notes,
   and check it with a web search or the learner's own source when the session
   allows. Never invent a citation: the only links this skill offers are the
   ones in [references/strategies.md](references/strategies.md).
6. **80/20 is a rule of thumb.** Say "the few ideas that unlock most of the
   topic", never a measured percentage.
7. **Review dates come from the script.** Sticky notes are added, scheduled and
   marked only with `scripts/sticky_notes.py`, never by editing the CSV by hand,
   so the dates are always right.

## Files

Everything the skill needs is in the folder this SKILL.md is in (called
`<skill>` below).

- [references/strategies.md](references/strategies.md) — how to run each of the
  ten strategies: what to ask, what it produces, what to save, an example and
  a link. Read a strategy's section before running it.
- [references/sequence.md](references/sequence.md) — the ten-step order, what
  each step carries forward, a worked example (transient hydrogen diffusion
  through a metal wall), the quiz routing table, and the templates for
  `progress.md` and `notes.md`. Read it before starting or resuming a sequence.
- [scripts/sticky_notes.py](scripts/sticky_notes.py) — adds sticky notes, lists
  which are due, shows an answer, and reschedules after a review. Standard
  library only; `python3 <skill>/scripts/sticky_notes.py -h`.

In the learner's folder, `learning/<topic-slug>/` (slug: lowercase words
joined by hyphens, e.g. `transient-diffusion`):

| File | Holds | Written by |
| --- | --- | --- |
| `progress.md` | goal, starting point, depth, the one-sentence idea, step reached, steps to revisit, `UNSURE` items | Claude |
| `notes.md` | one section per step or strategy: 80/20 list, mind map, schematic, explanations, Socratic questions, quiz log | Claude |
| `study-guide.html` | the one-page visual study guide (step 8) | Claude |
| `sticky-notes.csv` | review prompts, hidden answers, due dates | the script only |

## Workflow

### Phase 0 — Start

1. **Work out the mode** from the request:

   | Mode | The learner says | Do |
   | --- | --- | --- |
   | One strategy | names a strategy or its words: "like I'm five", "quiz me", "mind map", "Feynman", "Socratic", "first principles", "schematic", "study guide", "80/20", "make flashcards / sticky notes" | Phase 1 |
   | Sequence | "help me learn X", "teach me X step by step", "learning plan for X", "use the full method" | Phase 2 |
   | Review | "review my sticky notes", "review my flashcards", "what's due today" | Phase 3 |
   | Resume | "continue learning X", or `learning/<slug>/progress.md` already exists | read it, say where they left off, offer the next step |
   | Stuck | "I don't get X", "I'm stuck on X" | pick a strategy with "Choosing a strategy" below, say why, and ask |

2. **Look for earlier work:** `ls learning/ 2>/dev/null`. If the topic has a
   folder, read `progress.md` and the end of `notes.md` before anything else.
3. **New topic:** in one message, ask only what the request didn't already
   say: what they already know, why they're learning it (exam, research,
   project, curiosity), and how deep to go (intuition, working use, or
   derivation). A single strategy usually needs none of this; ask at most one
   question.
4. **Ask once whether to save** to `learning/<slug>/`. On yes, create the
   folder with `progress.md` and `notes.md` from the templates in
   [references/sequence.md](references/sequence.md). On no, keep it in the chat
   and don't ask again this session.

### Phase 1 — Run one strategy

1. Read that strategy's section in
   [references/strategies.md](references/strategies.md) and follow it, pitched
   at the depth from Phase 0.
2. Visuals: mind maps as a Mermaid `mindmap` block, schematics as a labelled
   text diagram in a code block, and the study guide as one self-contained
   HTML page. If the session has a tool that shows diagrams or pages, show it
   there as well.
3. If saving, append the result to `notes.md` under
   `## <Strategy> — <YYYY-MM-DD>` and update `progress.md`.
4. End by naming the strategy that naturally comes next (from
   [references/sequence.md](references/sequence.md)) and asking if they want it.

### Phase 2 — Run the sequence

Follow the order in [references/sequence.md](references/sequence.md):

| Step | Strategy | Carries forward |
| --- | --- | --- |
| 1 | ELI5 | the main idea in one sentence |
| 2 | 80/20 | the 3–5 concepts needed to explain that sentence |
| 3 | Mind map | the topic's structure, with `?` on links not yet understood |
| 4 | Schematic | the system drawn and labelled: boundaries, flows, where things are measured |
| 5 | First principles | an explanation built step by step from stated assumptions |
| 6 | Socratic questioning | each assumption, and where it breaks down |
| 7 | Feynman technique | a clean teach-back, with the gaps found and fixed |
| 8 | Visual study guide | `study-guide.html`, one page |
| 9 | Quiz me | a quiz log: misses and where each one routes |
| 10 | Sticky notes | review prompts with due dates |

After each step: save its output to `notes.md` under
`## Step N — <strategy>`, update "Step reached" in `progress.md`, show the
learner what carries forward, and ask: go on, redo, skip ahead, or stop.

### Quiz routing

After any quiz (step 9 or a standalone Quiz me), sort each miss:

| What went wrong | Go back to |
| --- | --- |
| Forgot a fact, term or equation | Sticky notes (step 10) |
| Remembered it but couldn't explain why it applies | First principles (step 5) |
| Solved it but couldn't explain it clearly | Feynman technique (step 7) |

Record the routes under "Go back to" in `progress.md`. Revisit the routed
steps before step 10, then turn every missed question into a sticky note.

### Phase 3 — Sticky notes and review

Paths below are relative to the folder Claude Code was started in.

- **Add** (one per missed question or key fact; one idea per note; the prompt
  answerable from memory in under a minute):

  ```bash
  python3 <skill>/scripts/sticky_notes.py add learning/<slug>/sticky-notes.csv \
    --prompt "What does the minus sign in Fick's first law mean?" \
    --answer "Flux runs down the concentration gradient, from high to low." \
    --source "step 9 quiz"
  ```

  New notes are due tomorrow.
- **What's due:** `python3 <skill>/scripts/sticky_notes.py due learning/` (all
  topics) or `... due learning/<slug>/sticky-notes.csv`. It prints prompts
  only, so the answers stay hidden.
- **Review**, one note at a time: ask the prompt, wait for the answer, then run
  `... show learning/<slug>/sticky-notes.csv ID` to get the answer, compare,
  and tell the learner. Then
  `... mark learning/<slug>/sticky-notes.csv ID --result right` (or `wrong`).
  Right moves the note along 1 → 3 → 7 → 14 → 30 → 60 days; wrong sends it
  back to tomorrow.
- **Nothing due:** `... due learning/ --next` prints the next review date.
- **Not saving to files:** list the notes in the chat with the prompt and the
  answer under a spoiler line, and suggest reviewing them tomorrow and again in
  three days.

### Choosing a strategy

| The learner says | Use |
| --- | --- |
| "I don't get the basic idea" | ELI5 |
| "There's too much — where do I start?" | 80/20 |
| "I can't see how the pieces fit together" | Mind map |
| "I can't picture it" | Schematic |
| "I know the formula but not why it's true" | First principles |
| "I'm not sure my reasoning holds" | Socratic questioning |
| "I think I get it" | Feynman technique, then Quiz me |
| "I need something to review before the exam" | Visual study guide |
| "I keep forgetting X" | Sticky notes |

## Verify

Before handing off, check:

- Every question you asked in a quiz, teach-back or Socratic round was
  answered by the learner before you gave feedback.
- Every miss has a route in `progress.md` and, by the end of the sequence, a
  sticky note.
- Every `UNSURE` item is listed in `progress.md` and in the hand-off.
- If saving: `progress.md` shows the right step, and
  `python3 <skill>/scripts/sticky_notes.py list learning/<slug>/sticky-notes.csv`
  runs without error when that file exists.
- Nothing was written outside `learning/<slug>/`.

## Hand-off

Tell the learner, in a few lines:

- what they covered and their one-sentence idea as it stands now;
- where the files are (or that nothing was saved);
- the next step, and any steps the quiz sent them back to;
- the next review date (`sticky_notes.py due learning/ --next`), and that
  "review my sticky notes" or "continue learning <topic>" picks up from here;
- every `UNSURE` item, with what would settle it.
