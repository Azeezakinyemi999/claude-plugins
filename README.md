# research-tools

Claude Code plugins for auditing and maintaining research codebases, and for
building more skills like them.

| Plugin | What it does |
| --- | --- |
| [technical-debt](plugins/technical-debt/skills/technical-debt/SKILL.md) | Read-only audit of a git repo for abandoned threads: code, parameters, config keys, notebook cells and files that were planned or once used, then dropped, but still exist. |
| [create-claude-skill](plugins/create-claude-skill/skills/create-claude-skill/SKILL.md) | Create, update and publish Claude Code skills end to end: write a portable skill, package it in your plugin marketplace, lint and validate it, test-install it, link it for local use, and push only after you say yes. |

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

Inside a `claude` session the same commands are `/plugin marketplace add …`
and `/plugin install …`. Restart Claude Code after installing.

Plugin skills are called as `/<plugin>:<skill>`, e.g.
`/technical-debt:technical-debt`, or just ask for the task in plain words.

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

## Update

```bash
claude plugin marketplace update research-tools
```

```bash
claude plugin update <plugin>@research-tools
```

## License

[MIT](LICENSE)
