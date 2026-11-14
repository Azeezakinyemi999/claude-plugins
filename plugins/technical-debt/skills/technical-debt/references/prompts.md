# Search rules, row schema, prompts, register template

Placeholders in `<ANGLE_CAPS>` come from the repo profile
(`<root>/.claude/technical-debt-profile.md`), except `<ROOT>`: the absolute
git root found at run time with `git rev-parse --show-toplevel`.

## Search rules (paste into every agent prompt)

- Run every command from the git root `<ROOT>`. Use `git grep`, not recursive
  `grep`: it is fast and skips untracked and ignored files (data, results).
- Caller search: `git grep -n -w <name> <SEARCH_PATHSPEC>`.
  **Never** `git grep -E "\b<name>\b"`: on macOS git grep's extended regex
  has no `\b` and silently returns nothing. Use `-w` or `-P`.
- Files git doesn't track (generated scripts, local copies) are invisible to
  `git grep`. Reason about them from whatever generates them.
- Template strings count as real code when they are rendered into scripts
  that run: a call or import inside one is live.
- Notebooks: `git grep` searches `.ipynb` JSON text, which is enough to find a
  call. To read a cell, parse the JSON with `<PYTHON>`.
- Indirect use: `**cfg` / dict unpacking into calls; `getattr`, string
  lookups, `importlib` / `__import__`; registries and decorators; entry points
  in `pyproject.toml` / `setup.cfg`; `__init__` re-exports and `__all__`;
  config files (YAML/JSON/TOML) that name a class, function or key; CLI parsers
  that wire a flag to code; CI workflows, Makefile targets, job and shell
  scripts; docs code snippets; `__main__` blocks.
- For other languages the same idea holds: exported symbols, dynamic
  `import()`, build targets, and every reader of a config key.
- A passing test is not proof that code works on the live path: tests that
  `exec`, mock or monkeypatch can inject what the real path lacks.
- History helps: `git log --oneline -S <name> -- <SCOPE>` finds the commit
  that added or removed a name; commit messages often say what replaced what.
- Then the repo's own rules, from the profile's *Search rules for this repo*:
  <REPO_SEARCH_RULES>

## What counts as an abandoned thread

Code, a parameter, a setting, a config or JSON key, a CLI flag, a declared
dependency, a template block, a notebook cell, a script or a file that was
planned or once used, and that no live path uses now. "Live" is defined in the
profile: <LIVE_DEFINITION>. Strong signals:

- only `tests/`, legacy folders, a `__main__` block or docs reach it;
- markers in comments or docstrings: retired, deprecated, legacy, no longer,
  unused, superseded, kept for, TODO, FIXME, "Option 1/2";
- a parameter accepted and threaded through but never changing behaviour
  (always the default, or read nowhere);
- a commit replaced it (`git log -S`) but the old one stayed;
- written to a JSON/CSV/output file that nothing reads;
- a dependency declared but never imported;
- docs describing a feature the code no longer has, or the reverse.

## Row schema (one detail block per item)

```markdown
### <ID> · `<symbol>` — <path>:<lines>

- **Kind:** function | class | param | setting | config/JSON key | CLI flag | dependency | template block | notebook cell | script | file | module
- **Recommendation:** DELETE | KEEP | DECIDE · **Confidence:** high | medium | low · **Lines:** ~N
- **Why abandoned / replaced by:** <symbol or commit sha + one line>
- **Callers:**
  - code: <file:line …> or none
  - template: <file:line inside which template> or none (say "no templates in this repo" if so)
  - notebook: <notebook, cell> or none
  - scripts/tools/CI: <file:line> (say if legacy) or none
  - tests only: <file:line / test names> or none
  - docs: <file:line> or none
  - commands: `<exact command(s) used>`
- **Config / output keys:** written at <file:line>; read at <file:line> or "never read"
- **Deleting touches:**
  - code: <what to delete; what to edit instead of delete>
  - tests: delete <tests>; edit <tests/fixtures>
  - notebooks: <cells>
  - living docs: <README, docs/ lines>
  - historical records (leave): <file:line>
- **Cross-unit:** <items in other units this frees or depends on>
- **Breaking:** <required param, public name, template import, CLI flag users pass> or no
- **Runtime exposure:** <used by a generated or deployed copy git can't see, a key in data already on disk, external users of a public API> or none
- **Executor notes:** <ordering, same-commit requirements, gotchas>
```

Group tiny related items (e.g. five unit-table keys) into one block. For DECIDE,
the *Why* line states the question the user must answer.

**Write locations so they can be linked.** Always `path:line` or
`path:start-end` with the path relative to `<PATH_BASE>` (a unique basename
is fine). A bare `L123` is linked to the file named *last in the same bullet*,
so when you switch files mid-bullet, name the new file. Notebooks can't be
line-linked: give the notebook path plus the cell index and cell id.

## Auditor prompt (one per unit)

```text
You are auditing ONE unit of a codebase for abandoned threads.
READ-ONLY: do not use Edit, Write or NotebookEdit; use Bash only for read-only
commands (git grep, git log, git show, sed -n, python that only reads). Never
run git checkout/stash/commit/rm. Return your findings as text; do not write
files.

Repo: <ROOT> (git root). Scope: <SCOPE>.
Project: <SUMMARY>
What counts as live: <LIVE_DEFINITION>
Not live on its own: <NOT_LIVE>

Unit <X> — files you own: <list>.
Search the whole search pathspec for callers, but only report items defined
in your files.

<paste "Search rules" and "What counts as an abandoned thread">

Seed items to verify at HEAD and expand (confirm, correct line numbers, map
every connection): <seeds, or "none — first run">
Verified KEEP — do not re-propose unless you find hard evidence they are dead:
<keep list, or "none">

Go symbol by symbol through your files: every public function, class,
module-level constant, parameter, config key and CLI flag; check its callers.
Also read module docstrings and comments for markers.

Write every location as path:line (relative to <PATH_BASE>); when you mention
a line in a different file than the one just named, name that file.

Output, in this order:
1. One detail block per item, using this schema: <paste "Row schema">.
   Provisional IDs <X>-01, <X>-02, … ordered by confidence then size.
2. "Refactor candidates": duplicates/inconsistencies (same computation twice,
   constants defined repeatedly, reversed argument orders) — one line each.
3. "Bugs seen on the way": real defects, not debt — one line each with
   path:line. Don't go looking for these.
4. "Checked and live": things that looked dead but aren't, with the evidence
   (one line each).
No filler; be as long as the evidence needs.
```

## Defender prompt (one per 2–3 units)

```text
READ-ONLY (same rules: no edits, no file writes, read-only Bash only).
Repo: <ROOT>. Scope: <SCOPE>.
What counts as live: <LIVE_DEFINITION>

Below are rows another agent recommends DELETING. Your job is to prove each
one is still LIVE. Try hard:
- template strings rendered into scripts (calls and imports inside them run);
- every notebook in the scope (git grep the JSON);
- **cfg / dict unpacking, getattr, string lookups, importlib by name,
  registries, config files that name it;
- scripts, tools, CI workflows, Makefile and job scripts (non-legacy counts as live);
- entry points, re-exports, __all__, monkeypatching, docs that tell users to
  call it by hand, and public API if this is a published library;
- the same name spelled differently (renamed import `as`, partial names).

<paste "Search rules">

For each row reply exactly one of:
- CONFIRMED DEAD — commands you ran and their (empty) result;
- LIVE — the caller with file:line;
- UNSURE — what you could not rule out.
Then list any connection the row missed (an extra test, doc, notebook cell).

Rows:
<rows>
```

## Register template

```markdown
# Technical-debt register

Audit of abandoned threads in `<SCOPE>` — code, parameters, keys, cells
and files that were planned and then dropped but still exist.

- **Audited:** <date> · branch `<branch>` · commit `<sha>`
- **Produced by:** the `technical-debt` skill, with the repo profile
  `.claude/technical-debt-profile.md`: <N> read-only unit auditors, then <M>
  defender agents that tried to prove every DELETE row still live.
- **Status:** report only — nothing has been deleted.
- **Not touched:** <uncommitted and untracked files from git status>

## How to use this register

Fill in the **Decision** column of the index table: `DELETE`, `KEEP`, `DEFER`,
or a short note. Recommendations are advice, not decisions. A separate session
executes the decided rows using "Notes for the executing session" below. Rows
marked KEEP move to *Verified KEEP* on the next run and are never re-proposed.

**Checking a row.** Every code location is a link that opens the file at that
line (Markdown preview and click, or `Cmd`/`Ctrl`+click in the editor). In the
index, **Code** opens the item's main location and the **ID** jumps to its
detail block. Lines are exact at the audited commit.

## Summary

<counts per recommendation and per unit; total lines removable if every DELETE
is accepted; the biggest items>

## Index

| ID | Item | Rec | Conf | Lines | Decision |
| --- | --- | --- | --- | --- | --- |
| A-01 | `old_helper` + its parameters | DELETE | high | ~N | |

(one table per unit, plus one for bugs and one for refactor candidates;
`link_register.py` adds the **Code** column and turns each ID into a link)

## Details

### Unit A — <name>

<detail blocks>

…

## Refactor candidates

Not abandoned threads — duplicates or inconsistencies whose fix could change
results. Listed for a separate decision.

## Verified KEEP

Looks dead, is live (or is a recorded decision). Do not delete.

## Open questions

## Notes for the executing session

<order, same-commit rules, per-commit gate (which tests to run), runtime
exposure risk>
```
