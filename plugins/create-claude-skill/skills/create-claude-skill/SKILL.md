---
name: create-claude-skill
description: Create, update or publish a Claude Code skill end to end — pin down what it should do, write a portable SKILL.md with references and scripts, package it as a plugin in the user's GitHub plugin marketplace repo, lint and validate it, test-install it in a throwaway config, link it into ~/.claude/skills for immediate use, and commit and push only after the user says yes. Also adds an existing skill folder to the marketplace, or bumps and republishes one. Use when the user asks to create, make, build, write, scaffold, package, update, version or publish a Claude skill or plugin, or to add a skill to their marketplace.
---

# Create a Claude skill

This skill turns an idea into a skill other people can install, and keeps
every skill in one place: a plugin marketplace repo the user owns (one plugin
per skill, under `plugins/<name>/`). It writes the skill, packages it, checks
it and links it for local use. It publishes only when the user says yes.

Three modes, chosen from the request:

- **New:** a skill that doesn't exist yet.
- **Import:** an existing skill folder (e.g. in `~/.claude/skills/` or a
  repo's `.claude/skills/`) moves into the marketplace.
- **Update:** change a skill already in the marketplace, bump its version,
  republish.

If the user wants a skill only for themselves or one repo and no marketplace,
skip packaging: write it to `~/.claude/skills/<name>/` or
`<repo>/.claude/skills/<name>/`, then follow Phases 2–3 only.

## Hard rules

1. **Commit and push only after the user says yes**, in this run, to the
   exact list of files. Never force-push. Never create a GitHub repo without
   asking its name and visibility.
2. **Never delete or overwrite a user's skill folder.** Replace one only with
   `skillkit.py link --replace`, which moves it to `~/.claude/skill-backups/`.
3. **Skills you write are portable:** no absolute paths, usernames, emails or
   machine-specific interpreters, and every repo-specific fact goes in a
   per-repo profile (see [references/conventions.md](references/conventions.md)).
   `skillkit.py check` flags violations; fix every portability warning
   before publishing.
4. **The marketplace folder is the only copy you edit.** The link in
   `~/.claude/skills/` points at it. Never edit `~/.claude/plugins/cache/`
   (overwritten on update) or a stray copy elsewhere.
5. **Don't install the user's own plugin on the machine where it is linked** —
   they'd get the skill twice (`/name` and `/name:name`).
6. **Ask once, then work.** Gather what you can't infer in a single round of
   questions (Phase 1); don't stop for each detail.

## Files

Everything this skill needs is in the folder this SKILL.md is in (called
`<skill>` below):

- [references/conventions.md](references/conventions.md) — how to write a good,
  portable skill: frontmatter, structure, safety, scripts, testing, versioning.
  **Read it before writing or reviewing any skill.**
- [references/templates.md](references/templates.md) — skeletons for SKILL.md,
  a per-repo profile, and the hand-off message.
- [scripts/skillkit.py](scripts/skillkit.py) — every mechanical step
  (standard library only, Python 3.7+). Run `python3 <skill>/scripts/skillkit.py -h`.
  It never commits, pushes or deletes.

## Workflow

### Phase 0 — Find the marketplace

1. `python3 <skill>/scripts/skillkit.py config`.
2. If it names a folder, run `skillkit.py list` and use it.
3. If nothing is saved, ask the user where their marketplace repo is, or
   whether to create one. A marketplace is a folder (normally a git repo)
   holding `.claude-plugin/marketplace.json`.
   - Existing: `skillkit.py config --set PATH`.
   - New: ask the marketplace name (kebab-case; people install with
     `plugin@<name>`), owner name and folder, then
     `skillkit.py init PATH --name NAME --owner "Owner"`. Ask which license
     (MIT is the usual choice) and write `LICENSE`. Set up git in Phase 5.

### Phase 1 — Pin down the skill

From the request and the conversation, work out what you can; ask the rest
in **one** question round (at most four questions, each with a recommended
option):

- **Purpose:** one sentence on what it does, and the result the user gets.
- **Triggers:** the words people will use to ask for it (these go in the
  description).
- **Inputs and outputs:** what it reads; exactly which files it may write,
  and where.
- **Side effects:** read-only, edits code, runs jobs, network, publishing —
  each outward action needs a "yes" rule in the skill.
- **Repo-specific knowledge:** does it need a per-repo profile?
- **Size:** one pass, or phases with parallel agents?

Pick the **name**: kebab-case, at most 64 characters, specific (not
`helper`). Check it is free with `skillkit.py list`, `ls ~/.claude/skills`,
and the skills available in this session.

For **Update**: read the current skill and ask only what changes. For
**Import**: read the folder and its frontmatter, and run its scripts' `--help`.

### Phase 2 — Write it

1. Register it:
   - New: `skillkit.py new NAME --description "…"`, which writes a skeleton,
     both manifests and a README row.
   - Import: `skillkit.py new NAME --description "…" --from DIR`, which
     copies the folder.
   - Update: edit the files under `plugins/NAME/skills/NAME/` in place.
2. Write the description (≤ 1024 characters): what it does, then
   "Use when …" with the trigger words. It is all Claude sees before
   choosing the skill.
3. Write the body in the order from conventions.md: purpose, hard rules,
   files, workflow, verify, hand-off. Put long material in `references/` and
   exact or repeatable steps in `scripts/` (with `-h` and `--dry-run` where
   they write anything).
4. Go through the checklist at the end of conventions.md.

### Phase 3 — Check

1. `skillkit.py check NAME` — fix every ERROR and every portability WARN;
   decide the rest.
2. Run each script once (`-h`, plus a dry run on a scratch input).
3. `skillkit.py test-install NAME` — installs from the local folder into a
   throwaway config and removes it; the user's own config is untouched.

### Phase 4 — Make it usable here

1. `skillkit.py link NAME --dry-run`, then `skillkit.py link NAME`. The
   symlink makes `~/.claude/skills/NAME` the repo folder, so edits apply
   immediately and there is one copy.
2. If a real folder is already there, `link` says whether it is identical to
   the repo copy. Tell the user, and use `--replace` only on their yes (it
   moves the old folder to `~/.claude/skill-backups/`).
3. Suggest a real task to try it on, in a new session: ask in plain words
   and check Claude picks the skill. If it doesn't, sharpen the description.

### Phase 5 — Publish

1. For an update, `skillkit.py bump NAME patch|minor|major` (rules in
   conventions.md). Installed copies are cached by version: an unchanged
   version means people may not get the change.
2. Show `git -C <marketplace> status --short` and a one-line summary per
   file, and ask: commit and push these?
3. On yes:
   - **No git yet:** `git init -b main`. Before the first commit, check
     `git config user.email`. If it isn't a GitHub no-reply address, offer to
     set this repo's email to `<id>+<user>@users.noreply.github.com`
     (`gh api user --jq .id`), so the commit history doesn't publish the
     real email.
   - Stage by path, never `git add -A`. Commit with a message saying what
     the skill does, and follow any commit-attribution rules the session
     gives.
   - **No remote:** ask the repo name and visibility (public: anyone can
     install it; private: only collaborators can), then
     `gh repo create <user>/<repo> --public|--private --source . --push`.
   - **Otherwise:** `git push`.

## Verify

- `skillkit.py check NAME` ends with 0 errors and no portability warnings.
- `skillkit.py test-install NAME` printed OK.
- `skillkit.py link NAME` reports the link (or the user chose to keep their folder).
- After a push, `git -C <marketplace> status` is clean and `git log -1` is the
  new commit.

## Hand-off

Tell the user, using [references/templates.md](references/templates.md):

- what the skill does and the command: `/NAME` here (via the link), or
  `/NAME:NAME` for anyone who installs the plugin;
- the two install commands to send to other people;
- how to ship a change: edit in the repo, `bump`, check, push;
- anything not done or not verified (e.g. not pushed, not tried on a real task).
