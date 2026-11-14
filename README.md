# research-tools

Claude Code plugins for auditing and maintaining research codebases.

| Plugin | What it does |
| --- | --- |
| [technical-debt](plugins/technical-debt/skills/technical-debt/SKILL.md) | Read-only audit of a git repo for abandoned threads: code, parameters, config keys, notebook cells and files that were planned or once used, then dropped, but still exist. |

## Install

You need [Claude Code](https://docs.claude.com/en/docs/claude-code) (terminal,
desktop app or IDE extension), git, and Python 3.7 or newer.

In a `claude` session:

```text
/plugin marketplace add Azeezakinyemi999/claude-plugins
/plugin install technical-debt@research-tools
```

Or from your shell:

```bash
claude plugin marketplace add Azeezakinyemi999/claude-plugins
claude plugin install technical-debt@research-tools
```

Restart Claude Code after installing.

## Use

Open any git repo in Claude Code and run:

```text
/technical-debt:technical-debt
```

or just ask: *"find the technical debt in this repo"*.

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

## Update

```bash
claude plugin marketplace update research-tools
claude plugin update technical-debt@research-tools
```

## License

[MIT](LICENSE)
