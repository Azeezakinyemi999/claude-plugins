# research-tools

Claude Code plugins for auditing and maintaining research codebases, and for
building more skills like them.

| Plugin | What it does |
| --- | --- |
| [technical-debt](plugins/technical-debt/skills/technical-debt/SKILL.md) | Read-only audit of a git repo for abandoned threads: code, parameters, config keys, notebook cells and files that were planned or once used, then dropped, but still exist. |
| [create-claude-skill](plugins/create-claude-skill/skills/create-claude-skill/SKILL.md) | Create, update and publish Claude Code skills end to end: write a portable skill, package it in your plugin marketplace, lint and validate it, test-install it, link it for local use, and push only after you say yes. |
| [idea-to-market](plugins/idea-to-market/) | Evaluate an idea with four due-diligence checks and a one-page decision memo, then plan commercialization (MVP, customer validation, go-to-market, operational readiness) only after the team approves. |
| [learning-strategy](plugins/learning-strategy/skills/learning-strategy/SKILL.md) | Tutors you through learning any topic with ten study strategies (ELI5, 80/20, mind map, schematic, first principles, Socratic questioning, Feynman technique, visual study guide, quiz me, sticky notes), one at a time or as a ten-step sequence that ends in spaced review. |
| [research-plots](plugins/research-plots/skills/research-plots/SKILL.md) | House style for every data figure: white background, black text, thick black frame and lines, large fonts, a few colour-blind-safe Okabe-Ito colours that keep one meaning across a project, labels next to the data instead of legends, real data only, and PDF plus 600 dpi PNG at final print size. |

## Install

You need [Claude Code](https://docs.claude.com/en/docs/claude-code) (terminal,
desktop app or IDE extension), git, and Python 3.7 or newer.

Add the marketplace once:

```bash
claude plugin marketplace add Azeezakinyemi999/claude-plugins
```

Then install the plugins you want:

```bash
claude plugin install technical-debt@research-tools
```

```bash
claude plugin install create-claude-skill@research-tools
```

```bash
claude plugin install idea-to-market@research-tools
```

```bash
claude plugin install learning-strategy@research-tools
```

Inside a `claude` session the same commands are `/plugin marketplace add …`
and `/plugin install …`. Restart Claude Code after installing.

Plugin skills are called as `/<plugin>:<skill>`, e.g.
`/technical-debt:technical-debt`, or just ask for the task in plain words.

## idea-to-market

Two skills for deciding on, and then developing, an idea: software, a
physical product, a service or a funded initiative. They share one
versioned handoff record.

**`/idea-to-market:idea-due-diligence`.** Give it a paragraph and any
materials, e.g. *"Evaluate this idea for a small pilot. Here is our
one-paragraph description and customer evidence."*

- Builds a business brief and runs four checks: customer problem, market
  opportunity, strategic fit, feasibility and economics.
- Writes `ideas/<idea>/report.md`. A one-page decision memo leads it, with
  one of five recommendations: Advance, Test further, Reshape, Hold or Stop.
- Also writes an evidence log with qualitative strength and reasons, test
  cards, and `handoff.md`.
- The handoff stays **pending** until the team explicitly approves a defined
  commitment.
- Answers follow-ups, compares "what if" scenarios without touching the
  approved record, and versions the handoff when evidence changes.
- Says which research paths ran: public research, configured read-only
  data access, or supplied evidence. It never invents numbers.

**`/idea-to-market:idea-commercialization`.** This one runs only when you
invoke it, e.g. *"Use this approved handoff to plan the capped paid pilot and
define what would justify a limited launch."*

- Reads the latest handoff and **stops** unless an approved commitment
  exists.
- Then plans a roadmap across MVP, customer validation, go-to-market and
  operational readiness, plus a detailed plan for the approved next step,
  with a fresh gate before any launch.
- It plans only. It never launches, contacts customers, spends money or
  publishes.

Optional live data: connect a read-only MCP server with `claude mcp add`
(see [sources.md](plugins/idea-to-market/skills/idea-due-diligence/references/sources.md)).
The skills work with public research and supplied files alone.

## technical-debt

Open any git repo in Claude Code and run `/technical-debt:technical-debt`, or
ask: *"find the technical debt in this repo"*.

**First run in a repo.** The skill reads the README, packaging files, CI and
entry points, and writes a short profile to
`.claude/technical-debt-profile.md`: what the code does, what counts as
*live* (the chain from entry points down), how the code splits into units,
and which folders to skip. It shows you the profile and asks once before
starting the audit agents. Edit the profile at any time to steer later runs.

**Every run.** One read-only auditor agent per unit, then defender agents
that try to prove each DELETE candidate is still in use. The result is a
register (by default `audits/technical_debt_register.md`) with, per item:

- a DELETE / KEEP / DECIDE recommendation and confidence;
- every caller, with the exact command that found it;
- what deleting it would touch (code, tests, notebooks, docs);
- a blank **Decision** column for you.

Every location in the register is a link that opens the file at that line.

**What it never does.** It never edits code, tests, notebooks, docs or
config: it writes only the profile and the register. Acting on your decisions
is a separate step you start yourself.

## create-claude-skill

Run `/create-claude-skill:create-claude-skill`, or ask: *"make a skill that
checks my LAMMPS input files"*, *"add this skill to my marketplace"*,
*"update the technical-debt skill and publish it"*.

**First run.** It asks where your plugin marketplace repo is, or creates a new
one for you, and remembers it in `~/.claude/create-claude-skill.json`.

**Every run.**

1. Pins down the skill in one round of questions: what it does, the words
   people will use to ask for it, which files it may write, and what needs
   your yes.
2. Writes a portable `SKILL.md` (no personal paths; repo-specific facts go
   in a per-repo profile), plus `references/` and `scripts/` where useful.
3. Packages it as `plugins/<name>/`, with both manifests and a README row.
4. Checks it: lint, `claude plugin validate`, and a test install in a
   throwaway config.
5. Links it into `~/.claude/skills/` so you can use `/<name>` straight away,
   with the repo as the only copy you edit.
6. Commits and pushes only after you say yes. For updates, it bumps the
   version first.

Its helper, `scripts/skillkit.py` (standard library only), does the
mechanical steps and can be run by hand: `python3 skillkit.py -h`.

## learning-strategy

Run `/learning-strategy:learning-strategy`, or just ask: *"explain diffusion
like I'm five"*, *"quiz me on Fick's law"*, *"help me learn transient
diffusion step by step"*, *"review my sticky notes"*.

**One strategy, or all ten in order.** ELI5 → 80/20 → mind map → schematic →
first principles → Socratic questioning → Feynman technique → visual study
guide → quiz me → sticky notes. Each step produces something the next one
uses, and the skill pauses after every step.

- In quizzes, teach-backs and Socratic rounds it asks **one question at a
  time** and waits for your answer before correcting you.
- The quiz sends each miss back to the right step: forgot it → sticky note;
  couldn't say why → first principles; couldn't explain it clearly → teach it
  back again.
- It flags anything it isn't sure of as `UNSURE` rather than guessing.

**What it saves.** Only after you say yes, and only in
`learning/<topic>/` in the current folder: `progress.md`, `notes.md`,
`study-guide.html` and `sticky-notes.csv`. Say no and it stays in the chat.
"Continue learning <topic>" picks up where you stopped.

**Spaced review.** Its helper, `scripts/sticky_notes.py` (standard library
only), schedules each note 1 → 3 → 7 → 14 → 30 → 60 days out, sends a missed
note back to tomorrow, and keeps answers hidden until you've answered.

## Update

```bash
claude plugin marketplace update research-tools
```

```bash
claude plugin update <plugin>@research-tools
```

## License

[MIT](LICENSE)
