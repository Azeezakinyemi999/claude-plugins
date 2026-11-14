# Repo profile

The profile is the only repo-specific part of this skill. It lives at
`<root>/.claude/technical-debt-profile.md`, is read at the start of every run,
and is the user's way to steer the audit. The skill writes it on the first run
and updates its Units table when files are added; everything else in it
changes only when the user edits it or asks for a change.

## Building it (first run)

Do this yourself for a small repo; for a large one, one Explore agent can do
steps 1–4 and return the facts. Every claim in the profile comes from a file
or a command, not a guess. Anything inferred goes under *Assumptions to
check*.

1. **Size it up.**
   - `git ls-files | wc -l` and `git ls-files | sed 's#/.*##' | sort | uniq -c`
     (top-level folders).
   - Lines per language, e.g.
     `git ls-files -z '*.py' | xargs -0 wc -l | tail -1`; repeat for the
     repo's other extensions (`*.ipynb`, `*.js`, `*.ts`, `*.jl`, `*.f90`, `*.sh` …).
2. **Pick the scope**: the folder or folders holding the project's own code
   and the docs about it. If the root holds several unrelated projects and
   the user didn't name one, put the choice in the profile check.
3. **Read what defines use**: `README*`; `pyproject.toml`, `setup.cfg`,
   `setup.py`, `package.json`, `environment.yml` (entry points, console
   scripts, exported packages, declared dependencies); `.github/workflows/`,
   `Makefile`, `Dockerfile`, job scripts (`*.sh`, `*.slurm`, `*.pbs`); the
   docs index; the package's `__init__` exports and `__all__`; the
   notebooks the README calls entry points.
4. **Write down what counts as live** — what people and machines actually
   run, as a chain from entry points down. Typical entry points:
   - console scripts / CLI commands, and the subcommands and flags they wire up;
   - scripts or notebooks the README tells users to run;
   - code generated from templates (a generator writes a script that later
     runs elsewhere — calls inside the template string are live);
   - scheduled or cluster jobs, CI jobs that run something other than tests;
   - web routes, plugins discovered by entry point or by name;
   - for a published library: the public API (`__init__` exports, `__all__`,
     the API reference in the docs).

   Then what is **not live on its own**: usually `tests/`, `legacy/` or
   archive folders, `if __name__ == "__main__":` demo blocks, docs snippets.
   Code reached only from these is a candidate.
5. **Exclusions**: paths that would pollute caller searches — data and results
   folders, archives, vendored third-party code, and committed copies of the
   package (`build/`, `dist/`, `*.egg-info/`, `site-packages/`). A committed
   build copy makes every function look called; exclude it from searches, but
   report the committed folder itself as an item.
6. **Units**: split the scope into 3–8 units of related files, small enough
   that one agent can read all of it (aim for ≤ ~4k lines of source each).
   Group by layer:
   - foundations imported by everything (config, constants, utils);
   - builders, I/O, parsers;
   - one unit per main feature or pipeline stage;
   - orchestration and entry points;
   - plotting and reporting;
   - last: notebooks, `scripts/`, `tools/`, and stale or duplicate files
     anywhere in the scope outside the main package.

   Name units A, B, C…; don't use R (refactor IDs). A repo under ~3k lines
   can be one or two units.
7. **Shared files**: files several units' items will touch (central config,
   the main notebook, large test files, README, docs with traceability
   tables), so the executing session edits each in one place.
8. **Search rules for this repo**: anything that makes a plain
   `git grep -w` miss real use or report false use — template strings,
   gitignored generated files, loading by name (`importlib`, `getattr`,
   registries, decorators), config files that name classes, tests that `exec`
   code with fake globals, a default interpreter that is broken.
9. **Interpreter**: the Python to use for reading notebooks and running the
   linker. Try `python3 --version`; prefer the env the README names. Record a
   full path only when the default one is broken, and say whose machine it is
   for: other people who clone the repo fall back to `python3`.
10. **Register path**: default `<path base>/audits/technical_debt_register.md`,
    or wherever the repo already keeps audits.

## Template

```markdown
# Technical-debt profile — <repo name>

Read by the `technical-debt` skill at the start of every run. Edit it to steer
the next run. Written <date> at commit `<sha>`. Paths are relative to the git
root, so the profile works in any clone of the repo.

## Project

- **Scope:** `<folder>/`
- **Search pathspec:** `-- <folder> ':!<excluded>' ':!<excluded>'`
- **Paths in the register are relative to:** `<folder>/` (the path base)
- **Register:** `<folder>/audits/technical_debt_register.md`
- **Kind:** research pipeline | published library | app or service | script collection
- **Summary:** <2–4 lines: what the code does, and where it deliberately stops>
- **Python:** `python3` (or a full path, used only where it exists; everyone
  else falls back to `python3`)

## What counts as live

<the chain from entry points down, one or two lines per link>

Not live on their own: <tests/, legacy/, __main__ blocks, docs, …>

## Units

| Unit | Scope | Notes |
| --- | --- | --- |
| A <name> | `<files>` | <who imports it, anything an auditor must know> |

## Shared files

- `<path>` — <why several items touch it>

## Search rules for this repo

- <rule>

## Excluded from search

- `<path>/` — <why>

## Out of scope

- <paths never audited, and how to treat mentions of them (e.g. historical
  audit records: list, never recommend editing)>

## Linker

`<python> <skill>/scripts/link_register.py <register> --exclude <path>/ --prefer <folder>/`
(`<python>` is the Python line above; `<skill>` is wherever the skill is installed)

## Assumptions to check

- <anything inferred rather than confirmed>
```
