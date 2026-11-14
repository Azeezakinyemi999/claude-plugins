# Conventions for skills

Read this before writing or reviewing a skill. The checklist at the end is
the definition of done.

## Anatomy

```text
<name>/
├── SKILL.md          required: frontmatter + instructions
├── references/       optional: long material Claude reads when a step needs it
├── scripts/          optional: code Claude runs (not reads) for exact, repeatable steps
└── assets/           optional: templates or files copied into outputs
```

Only the frontmatter is always in Claude's context. The body loads when the
skill is chosen; `references/` files load only when the body sends Claude to
them. So keep the body focused and link to detail from the step that needs it.

## Frontmatter

```yaml
---
name: kebab-case-name
description: What it does, in one or two sentences. Use when the user asks to <the words they will actually say>.
---
```

- `name`: lowercase letters, digits and hyphens, at most 64 characters, and
  the same as the folder name.
- `description`: at most 1024 characters, in the third person. Say **what it
  does** and **when to use it** ("Use when …"), with the phrases and synonyms
  users actually type. If the skill has a key boundary (read-only, never
  pushes), say so: it helps Claude choose correctly. The description is the
  only thing Claude sees when deciding whether to load the skill, so a vague
  one means the skill never runs.
- Claude Code accepts a few optional fields (for example `allowed-tools`).
  Add one only with a concrete reason, and check the current docs first.

## Body, in this order

1. **Purpose:** one paragraph on what it does and what it never does.
2. **Hard rules:** numbered, short and checkable. These are the rules that
   must hold on every run: which files it may write, what needs the user's
   yes, and what counts as proof.
3. **Files:** what is in the skill folder, and what the skill reads and
   writes in the user's project.
4. **Workflow:** phases or steps, each with the exact commands.
5. **Verify:** how the skill checks its own output before handing off.
6. **Hand-off:** what to tell the user at the end, including anything not
   done or not verified.

## Writing style

- Imperative and specific. Spell out commands exactly as they should run.
- Give the reason for any rule that isn't obvious: Claude applies a rule
  better when it knows why, and can handle cases the rule didn't foresee.
- One concrete example beats a paragraph of description.
- Prefer checklists and tables to long prose.
- Keep `SKILL.md` under ~500 lines (aim for 150–300). Move long material
  into `references/`.

## Portability (required)

The skill must work for someone else, on another machine, in another repo.

- **No** absolute paths, usernames, emails, hostnames or machine-specific
  interpreter paths in any skill file.
- Refer to bundled files relative to the skill: "`<skill>/scripts/x.py`,
  where `<skill>` is the folder this SKILL.md is in". The skill can then run
  from `~/.claude/skills/`, from a repo's `.claude/skills/`, or from an
  installed plugin.
- Find the project root at run time (`git rev-parse --show-toplevel`). Never
  store it.
- **Repo-specific knowledge goes in a per-repo profile**,
  `<repo>/.claude/<skill-name>-profile.md`:
  - the skill builds it on its first run in a repo, and asks the user once to
    confirm it;
  - later runs read it, and the user edits it to steer the skill;
  - machine-specific values in it (such as a Python path) are used only where
    they exist, with `python3` as the fallback.

  [templates.md](templates.md) has the profile skeleton.
- Scripts: use the standard library where possible, with Python 3.7+ or
  POSIX `sh`. Take repo specifics as flags, provide `-h`, and add `--dry-run`
  for anything that writes.

## Safety

- **Read-only by default.** List the exact files the skill may write.
- **Ask before outward or irreversible actions:** pushing, publishing,
  sending messages, submitting jobs, deleting, overwriting user files,
  installing software, and network calls that carry user data.
- **Multi-agent skills:** sub-agents are read-only and return text, and only
  the lead writes files. Launch independent agents in one message so they
  run in parallel.
- **Uncertain means report, don't guess.** Flag it for the user instead of
  silently picking an answer.
- **No secrets** in skill files, examples or test data.

## Scripts or instructions?

Use a **script** when the step must come out exactly the same every time:
editing JSON, linking files, parsing output, counting, or checking a format.
Use **instructions** when the step needs judgment. Scripts are run, not read,
so they don't take up context. Say in `SKILL.md` exactly how to call them.

## Testing a skill

1. **Trigger:** in a new session, ask for the task in plain words. Claude
   should choose the skill. If it doesn't, improve the description.
2. **Task:** run it on a real project, and check the output against the hard
   rules.
3. **Package:** run `skillkit.py check NAME` (0 errors, no portability
   warnings), then `skillkit.py test-install NAME`.

## Versioning

Use `MAJOR.MINOR.PATCH`, kept the same in `plugin.json` and
`marketplace.json` (`skillkit.py bump` updates both):

- **patch:** wording, a bug fix, or a clearer instruction;
- **minor:** a new capability that keeps existing behaviour and outputs;
- **major:** changes which files it writes, their format, or how users call it.

Installed copies are cached by version, so a change shipped without a bump
may never reach users.

## Naming

- One skill per plugin, with the same name for both, so the command reads
  `/name:name`.
- **Exception:** skills that form one workflow and share a record (for
  example, evaluate an idea and then plan it) go in **one plugin**, named for
  the workflow. Each skill keeps its own folder, and any shared reference is
  copied into each skill and kept identical. Users install once and call
  `/plugin:skill`.
- Use a verb-noun or a noun phrase that says what it does
  (`technical-debt`, `create-claude-skill`). Avoid generic names that collide
  (`helper`, `tools`).

## Checklist (definition of done)

- [ ] `name` matches the folder; the description says what + "Use when …" with real trigger words.
- [ ] Hard rules list every file it writes and every action that needs a yes.
- [ ] No absolute paths, usernames, emails or machine paths; repo facts live in a profile.
- [ ] Bundled files are referenced relative to the skill folder.
- [ ] Scripts have `-h`; writers have `--dry-run`; standard library only where possible.
- [ ] A Verify section and a Hand-off section exist.
- [ ] `SKILL.md` ≤ ~500 lines; detail is in `references/`.
- [ ] `skillkit.py check` passes; `test-install` passes; it triggers from plain words.
- [ ] Version bumped (updates only); README row says what it does.
