---
name: technical-debt
description: Multi-agent, read-only audit of any git repo for abandoned threads — functions, parameters, settings, config/JSON keys, template blocks, notebook cells and files that were planned or once used, then dropped, but still exist. Works in any repo — on the first run it maps the repo into a profile (.claude/technical-debt-profile.md — what counts as live, work units, exclusions). It then writes a register with a DELETE / KEEP / DECIDE recommendation and a "what it touches" map per item, plus a blank Decision column for the user. Never edits code, tests, notebooks or docs — a separate session executes the user's decisions. Use when the user asks to find or report technical debt, dead code, abandoned threads, or to refresh the register.
---

# Technical-debt register

This skill does ONE thing: find threads a project planned to use and then
abandoned, and write a register the user can decide from. It does not delete,
refactor, or fix anything. Execution happens later, in a separate session,
from the Decision column the user fills in.

An example of an abandoned thread: a simulation pipeline used to go past
permeability Φ = D·S to a hydrogen flux J (`fick_flux`, `richardson_flux`,
operating pressures, membrane thickness). It now stops at Φ, but the flux
code, its parameters, tests and docs all survived.

## Hard rules

1. **Never modify code, tests, notebooks, docs or config.** In the target repo
   this skill writes exactly two files: the profile
   (`.claude/technical-debt-profile.md`) and the register (path set in the
   profile).
2. **Agents are read-only and return rows as text.** Only the lead writes
   files. Tell every agent explicitly: no Edit/Write/NotebookEdit, and Bash
   only for read-only commands (`git grep`, `git log`, `git show`, `sed -n`,
   `python -c` that only reads). No `git checkout`, `stash`, `commit`, `rm`.
3. **Every DELETE needs proof.** Each caller claim carries the exact command
   that produced it. A claim without a command is a DECIDE.
4. **Uncertain means DECIDE**, with the reason. Never round up to DELETE.
5. **Report, don't ask.** Open questions become DECIDE rows; don't stop to ask
   the user one item at a time. The one exception is the profile check on a
   repo's first run (Phase 0).
6. **Keep the scope to abandoned threads.** Duplicates and inconsistencies
   that a fix could change results for (two helpers computing the same thing,
   a constant defined seven times) go in the separate *Refactor candidates*
   section.
7. **A library's public API is live by default.** If the repo is a package
   other people install, anything exported or documented for users is at most
   DECIDE (Breaking: yes), never DELETE just because nothing in the repo calls
   it.

## Files

Everything the skill needs is in the folder this SKILL.md is in (called
`<skill>` below). The folder is self-contained: it works from
`~/.claude/skills/` (every repo on this machine) or copied into one repo's
`.claude/skills/`.

- How to build and read a repo profile, plus its template:
  [references/profile.md](references/profile.md)
- Search rules, row schema, agent prompts, register template:
  [references/prompts.md](references/prompts.md)
- Linker that makes every location clickable (stdlib only, Python 3.7+):
  [scripts/link_register.py](scripts/link_register.py)

In the target repo:

- `<root>`: the git root of the repo the user named, else of the working
  directory (`git rev-parse --show-toplevel`). Run every command from there.
  The root always comes from git, never from the profile, so a profile
  committed to a shared repo works in anyone's clone. If there is no git
  repo, say so and stop: the method depends on `git grep` and `git log`.
- Profile: `<root>/.claude/technical-debt-profile.md`.
- Register: the path the profile names.

## Workflow

### Phase 0 — Prepare

1. Record `git branch --show-current`, `git rev-parse --short HEAD` and
   `git status --short` (the header lists uncommitted and untracked files as
   "not touched").
2. **Profile.**
   - If it exists, read it. Re-derive the file list with
     `git ls-files <scope>` and check every source file is in a unit. Put new
     files in the closest unit, update the profile's Units table, and say so
     in the register header. If the profile's Python is a full path that
     doesn't exist on this machine (the profile was written on someone else's
     computer), use `python3` instead and say so in the register header.
   - If it is missing, build it as [references/profile.md](references/profile.md)
     describes and write it. Then show the user, in one message, the summary,
     what counts as live, the units and the exclusions, and ask once whether
     to proceed: a wrong "live" definition wastes every agent run after it. If
     the user already said to run end to end without stopping, or nobody can
     answer (headless run), carry on and copy the profile's *Assumptions to
     check* into the register's Open questions.
3. If the register already exists, read it first:
   - keep every ID and the user's Decision text exactly;
   - items whose code is now gone → status DONE (re-check with `git grep -n -w`);
   - items the user marked KEEP → move to *Verified KEEP*, never re-propose;
   - pass the existing rows for each unit to that unit's auditor as seeds.

### Phase 1 — Audit (parallel)

Launch one general-purpose agent per unit **in a single message** so they run
concurrently. Use the auditor prompt in [references/prompts.md](references/prompts.md),
filled in from the profile: root, scope, summary, what counts as live, the
unit's files, the repo's search rules, the unit's seed items, and the full
Verified KEEP list. Each agent owns its unit's files but searches the whole
search pathspec for callers.

### Phase 2 — Defend (parallel)

When the auditors return, collect every DELETE row. Launch defender agents in
one message, one per 2–3 units (at least one), using the defender prompt.
Their job is to prove each row is still live. Apply the results: refuted rows
become KEEP (add to Verified KEEP with the evidence); rows the defender
couldn't rule out become DECIDE with the reason.

### Phase 3 — Consolidate and write

1. Dedupe items reported by more than one unit; keep the owning unit's row and
   note the other unit under cross-unit dependencies.
2. Add cross-unit chains: deleting a caller in one unit can make a provider in
   another unit dead. Record both directions.
3. Assign stable IDs `<unit>-NN` (A-01, D-07, …), ordered by size and
   confidence within each unit; `BUG-NN` for bugs found on the way, `R-NN` for
   refactor candidates. Reuse existing IDs on reruns.
4. Write the register from the template in [references/prompts.md](references/prompts.md):
   header, index table with a blank Decision column, detail blocks, Refactor
   candidates, Verified KEEP, Open questions, Notes for the executing session.
   Write every location as `path:line`, with paths relative to the profile's
   path base.
5. Make every location clickable, so the user can check each row in their
   editor before deciding. Use the interpreter and flags from the profile's
   *Linker* line:

   ```bash
   <python> <skill>/scripts/link_register.py <register> --dry-run \
     --exclude <path>/ --prefer <path base>/
   ```

   It links every `path:line`, links a bare `L123` to the file named last in
   the same list item, anchors every row, and adds a **Code** column to the
   index. Read its review log: wherever a bare `L123` landed on the wrong
   file (a different file was mentioned in between) or stayed unlinked, name
   the file in the row text. Repeat, then run without `--dry-run`. It is
   idempotent, so re-running after edits is safe.

### Phase 4 — Verify

- `git status` shows the profile and the register as the only changes made by
  this run.
- Re-run the evidence command for ~5 random DELETE rows; the output must
  match what the row claims.
- Every DELETE row has a `-w` caller search, states template and notebook
  coverage (or "none in this repo"), lists tests (delete vs edit) and living
  docs.
- Index-table IDs and detail-block IDs match 1:1.
- Every link opens something: each relative target exists on disk, each `#L`
  is within the file, each in-page `#id` has an anchor, and every index row
  has a **Code** link. (Only tracked files still on disk get linked — check
  `git status` for tracked files that moved, and say so in the header.)

## Handing off

Tell the user where the register is, how many items per recommendation, the
biggest wins by lines, and the open questions. On a first run, also point to
the profile and say that editing it (live entry points, units, exclusions)
steers the next run. Remind them the Decision column is the only thing they
need to fill in, and that executing it is a separate step — don't offer to
start deleting.
