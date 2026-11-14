# Templates

## SKILL.md

`skillkit.py new` writes this skeleton. Use it directly for a local-only
skill (`~/.claude/skills/<name>/` or `<repo>/.claude/skills/<name>/`).

```markdown
---
name: <name>
description: <What it does, in one or two sentences>. Use when the user asks to <trigger words>.
---

# <Title>

<One paragraph: what this skill does, and what it never does.>

## Hard rules

1. <Which files it may write. Everything else is read-only.>
2. <Which actions need the user's yes in this run.>
3. <What counts as proof / when to report instead of guessing.>

## Files

Everything the skill needs is in the folder this SKILL.md is in (called
`<skill>` below).

- [references/<topic>.md](references/<topic>.md) — <when to read it>
- [scripts/<tool>.py](scripts/<tool>.py) — <what it does; `-h` for options>

In the user's project:

- reads: <…>
- writes: <exact paths>
- profile: `<repo>/.claude/<name>-profile.md` (only if it needs repo-specific knowledge)

## Workflow

### Phase 0 — Prepare
<root via `git rev-parse --show-toplevel`; read the profile, or build it and ask once>

### Phase 1 — <…>
<exact commands>

### Phase 2 — <…>

## Verify

- <checks the skill runs on its own output>

## Hand-off

Tell the user <what was produced, where, what is not done or not verified,
what they decide next>.
```

## Per-repo profile

For skills that need repo-specific knowledge. The skill writes it on its first
run in a repo, shows it to the user once, and reads it on every later run.

```markdown
# <skill-name> profile — <repo name>

Read by the `<skill-name>` skill at the start of every run. Edit it to steer
the next run. Written <date> at commit `<sha>`. Paths are relative to the git
root, so the profile works in any clone.

## Project
- **Scope:** `<folder>/`
- **Summary:** <2–4 lines on what the code does>
- **Python:** `python3` (or a full path, used only where it exists)

## <Skill-specific sections>
<what counts as live / entry points / units / exclusions / outputs …>

## Assumptions to check
- <anything inferred rather than confirmed>
```

## Hand-off message for other people

```text
Install the <name> skill for Claude Code:

  claude plugin marketplace add <github-user>/<repo>
  claude plugin install <name>@<marketplace-name>

Restart Claude Code, then run /<name>:<name> — or just ask for it in plain
words. Updates: claude plugin marketplace update <marketplace-name>, then
claude plugin update <name>@<marketplace-name>.
```

## Commit message

```text
Add <name>: <one-line what it does>

<2–4 lines: what it reads and writes, what needs a yes, how to call it.>
```

For an update: `<name> <old> → <new>: <what changed>`.
