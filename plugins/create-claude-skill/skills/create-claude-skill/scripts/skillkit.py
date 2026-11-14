#!/usr/bin/env python3
"""skillkit -- the helper script of the create-claude-skill skill.

Manages a Claude Code plugin marketplace folder: add plugins, bump versions,
lint them, test-install them in a throwaway config, and link their skills into
~/.claude/skills for use on this machine. Standard library only (Python 3.7+).
It never commits, pushes or deletes: replaced folders are moved to
~/.claude/skill-backups/.

    python3 skillkit.py [--marketplace PATH] COMMAND [options]

Commands
  config [--set PATH]               show, or save, the marketplace folder
  init PATH --name N --owner O      create a new, empty marketplace folder
  list                              plugins, versions and their skills
  new NAME --description D          add plugins/NAME (skeleton, or --from DIR;
                                    --skill S names the skill folder)
  add-skill NAME --from DIR         add another skill folder to plugin NAME
  bump NAME [patch|minor|major]     raise the version in both manifests
  check [NAME ...]                  lint plugins, then `claude plugin validate`
  test-install NAME                 install into a throwaway CLAUDE_CONFIG_DIR
  link NAME [--replace] [--dry-run] point ~/.claude/skills/<skill> at the repo

The marketplace folder comes from --marketplace, else from
~/.claude/create-claude-skill.json (written by `config --set` or `init`).
"""
from __future__ import annotations

import argparse
import datetime
import filecmp
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CONFIG = Path.home() / '.claude' / 'create-claude-skill.json'
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SEMVER_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')
IGNORE = shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store', '.git')
TEXT_EXT = {'.md', '.py', '.sh', '.json', '.txt', '.yaml', '.yml', '.toml',
            '.cfg', '.ini', '.js', '.ts', '.html', '.css', '.r', '.jl'}
HOME_RE = re.compile(r'(?:/Users/|/home/|C:\\Users\\)([A-Za-z0-9._-]+)')
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
EMAIL_OK = ('noreply', 'no-reply', 'example.com', 'example.org', 'users.noreply.github.com')

SKELETON = """---
name: {name}
description: {description}
---

# {title}

TODO: one paragraph -- what this skill does, and what it never does.

## Hard rules

1. TODO: the few rules that must hold on every run (e.g. which files it may
   write, what needs the user's yes).

## Files

Everything the skill needs is in the folder this SKILL.md is in (called
`<skill>` below).

- TODO: references/... (read when a step needs them), scripts/... (run them)

## Workflow

### Step 1 -- TODO

### Step 2 -- TODO

## Verify

TODO: how the skill checks its own output before handing off.

## Hand-off

TODO: what to tell the user at the end.
"""


# -- small helpers --------------------------------------------------------------

def die(msg: str, code: int = 1):
    print(f'error: {msg}', file=sys.stderr)
    sys.exit(code)


def read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except FileNotFoundError:
        die(f'{p} not found')
    except json.JSONDecodeError as e:
        die(f'{p} is not valid JSON: {e}')


def write_json(p: Path, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def frontmatter(skill_md: Path):
    """Parse the simple YAML block at the top of SKILL.md -> dict, or None."""
    lines = skill_md.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    out, key = {}, None
    for ln in lines[1:]:
        if ln.strip() == '---':
            return out
        m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', ln)
        if m and not ln[:1].isspace():
            key, val = m.group(1), m.group(2).strip()
            if val in ('>', '|', '>-', '|-'):
                val = ''
            if len(val) >= 2 and val[0] == val[-1] and val[0] in '"\'':
                val = val[1:-1]
            out[key] = val
        elif key and ln[:1].isspace():
            out[key] = (out[key] + ' ' + ln.strip()).strip()
    return None


def git_remote_https(folder: Path):
    try:
        url = subprocess.run(['git', '-C', str(folder), 'config', '--get', 'remote.origin.url'],
                             capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        return None
    m = re.match(r'^(?:git@|https://)([^:/]+)[:/](.+?)(?:\.git)?$', url)
    return f'https://{m.group(1)}/{m.group(2)}' if m else None


class Market:
    def __init__(self, root: Path):
        self.root = root.expanduser().resolve()
        self.manifest = self.root / '.claude-plugin' / 'marketplace.json'
        if not self.manifest.exists():
            die(f'{self.root} is not a marketplace (no .claude-plugin/marketplace.json). '
                f'Create one with: skillkit.py init PATH --name NAME --owner "Your Name"')
        self.data = read_json(self.manifest)

    @property
    def name(self):
        return self.data.get('name')

    def entry(self, name):
        for p in self.data.get('plugins', []):
            if p.get('name') == name:
                return p
        return None

    def plugin_dir(self, name):
        e = self.entry(name)
        src = (e or {}).get('source', f'./plugins/{name}')
        if not isinstance(src, str):
            die(f'plugin {name!r} has a non-local source; this tool only manages local plugins')
        return (self.root / src).resolve()

    def skills(self, name):
        d = self.plugin_dir(name) / 'skills'
        return sorted(p for p in d.iterdir() if p.is_dir()) if d.is_dir() else []

    def save(self):
        write_json(self.manifest, self.data)


def market(args) -> Market:
    if args.marketplace:
        return Market(Path(args.marketplace))
    if CONFIG.exists():
        cfg = read_json(CONFIG)
        if cfg.get('marketplace'):
            return Market(Path(cfg['marketplace']))
    die('no marketplace folder set. Run `skillkit.py config --set PATH` for an existing one, '
        'or `skillkit.py init PATH --name NAME --owner "Your Name"` for a new one.')


def save_config(path: Path):
    cfg = read_json(CONFIG) if CONFIG.exists() else {}
    cfg['marketplace'] = str(path.expanduser().resolve())
    write_json(CONFIG, cfg)
    print(f'saved marketplace = {cfg["marketplace"]}  ({CONFIG})')


# -- commands -------------------------------------------------------------------

def cmd_config(args):
    if args.set:
        Market(Path(args.set))          # validates it is a marketplace
        save_config(Path(args.set))
        return
    if not CONFIG.exists():
        print(f'no config yet ({CONFIG})')
        return
    print(json.dumps(read_json(CONFIG), indent=2))


def cmd_init(args):
    root = Path(args.path).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        die(f'{root} exists and is not empty')
    if not NAME_RE.match(args.name):
        die(f'marketplace name {args.name!r} must be kebab-case (a-z, 0-9, hyphens)')
    write_json(root / '.claude-plugin' / 'marketplace.json', {
        'name': args.name,
        'owner': {'name': args.owner},
        'metadata': {'description': args.description or 'Claude Code plugins.', 'version': '1.0.0'},
        'plugins': [],
    })
    (root / 'plugins').mkdir(parents=True, exist_ok=True)
    (root / '.gitignore').write_text('__pycache__/\n*.pyc\n.DS_Store\n', encoding='utf-8')
    (root / 'README.md').write_text(
        f'# {args.name}\n\n{args.description or "Claude Code plugins."}\n\n'
        '| Plugin | What it does |\n| --- | --- |\n\n'
        '## Install\n\n```bash\nclaude plugin marketplace add <github-user>/<repo>\n```\n\n'
        f'```bash\nclaude plugin install <plugin>@{args.name}\n```\n', encoding='utf-8')
    print(f'created marketplace {args.name!r} at {root}')
    if not CONFIG.exists():
        save_config(root)
    else:
        print(f'(config already points elsewhere; switch with: skillkit.py config --set {root})')
    print('next: add a LICENSE, then `git init -b main` when you are ready to publish.')


def cmd_list(args):
    m = market(args)
    print(f'marketplace {m.name!r} at {m.root}')
    for e in m.data.get('plugins', []):
        skills = ', '.join(s.name for s in m.skills(e['name'])) or '(no skills/)'
        print(f'  {e["name"]:<28} {e.get("version", "?"):<9} skills: {skills}')


def _readme_add_row(m: Market, name: str, desc: str, link: str = None):
    readme = m.root / 'README.md'
    if not readme.exists():
        print('  README.md: none, skipped')
        return
    lines = readme.read_text(encoding='utf-8').split('\n')
    head = next((i for i, l in enumerate(lines) if re.match(r'^\|\s*Plugin\s*\|', l)), None)
    if head is None:
        print('  README.md: no "| Plugin |" table found; add a row by hand')
        return
    if any(f'[{name}]' in l for l in lines):
        print('  README.md: row already present')
        return
    end = head + 1
    while end < len(lines) and lines[end].startswith('|'):
        end += 1
    first = re.split(r'(?<=[.!?])\s', desc.strip(), maxsplit=1)[0]
    link = link or f'plugins/{name}/skills/{name}/SKILL.md'
    lines.insert(end, f'| [{name}]({link}) | {first} |')
    readme.write_text('\n'.join(lines), encoding='utf-8')
    print('  README.md: added a row to the plugin table')


def cmd_new(args):
    m = market(args)
    name = args.name
    if not NAME_RE.match(name) or len(name) > 64:
        die(f'{name!r} must be kebab-case (a-z, 0-9, hyphens), at most 64 characters')
    if m.entry(name):
        die(f'{name!r} is already in {m.manifest}')
    pdir = m.root / 'plugins' / name
    if pdir.exists():
        die(f'{pdir} already exists')
    skill = args.skill or name
    if not NAME_RE.match(skill) or len(skill) > 64:
        die(f'skill name {skill!r} must be kebab-case, at most 64 characters')
    sdir = pdir / 'skills' / skill
    if args.source:
        _copy_skill(args.source, sdir)
    else:
        sdir.mkdir(parents=True)
        (sdir / 'SKILL.md').write_text(SKELETON.format(
            name=skill, description=args.description,
            title=skill.replace('-', ' ').capitalize()), encoding='utf-8')
        print(f'  wrote skeleton {sdir / "SKILL.md"}')
    owner = (m.data.get('owner') or {}).get('name')
    author = {'name': args.author or owner} if (args.author or owner) else None
    license_ = next((read_json(m.plugin_dir(e['name']) / '.claude-plugin' / 'plugin.json').get('license')
                     for e in m.data.get('plugins', [])
                     if (m.plugin_dir(e['name']) / '.claude-plugin' / 'plugin.json').exists()), None)
    url = git_remote_https(m.root)
    manifest = {'name': name, 'version': args.version, 'description': args.description}
    if author:
        manifest['author'] = author
    if url:
        manifest['homepage'] = manifest['repository'] = url
    if license_:
        manifest['license'] = license_
    if args.keywords:
        manifest['keywords'] = args.keywords
    write_json(pdir / '.claude-plugin' / 'plugin.json', manifest)
    entry = {'name': name, 'source': f'./plugins/{name}', 'description': args.description,
             'version': args.version}
    if author:
        entry['author'] = author
    if args.keywords:
        entry['keywords'] = args.keywords
    m.data.setdefault('plugins', []).append(entry)
    m.save()
    print(f'  registered {name} {args.version} in {m.manifest.relative_to(m.root)}')
    _readme_add_row(m, name, args.description,
                    None if skill == name else f'plugins/{name}/')
    print(f'next: write the skill in {sdir}, then `skillkit.py check {name}`')


def _copy_skill(source, sdir: Path):
    src = Path(source).expanduser().resolve()
    if not (src / 'SKILL.md').exists():
        die(f'{src} has no SKILL.md')
    if sdir.exists():
        die(f'{sdir} already exists')
    fm = frontmatter(src / 'SKILL.md') or {}
    if fm.get('name') != sdir.name:
        print(f'  warning: SKILL.md frontmatter name is {fm.get("name")!r}, not {sdir.name!r}; fix it')
    shutil.copytree(src, sdir, ignore=IGNORE)
    print(f'  copied {src} -> {sdir}')


def cmd_add_skill(args):
    """Add a second (third, ...) skill to an existing plugin, for skills that form one workflow."""
    m = market(args)
    if not m.entry(args.name):
        die(f'{args.name!r} is not in the marketplace; create it with `new` first')
    src = Path(args.source).expanduser().resolve()
    skill = args.skill or src.name
    if not NAME_RE.match(skill) or len(skill) > 64:
        die(f'skill name {skill!r} must be kebab-case, at most 64 characters')
    _copy_skill(src, m.plugin_dir(args.name) / 'skills' / skill)
    print(f'next: `skillkit.py check {args.name}`; if {args.name} is already published, '
          f'`skillkit.py bump {args.name} minor`')


def _bump(v, part):
    mm = SEMVER_RE.match(v or '')
    if not mm:
        die(f'version {v!r} is not MAJOR.MINOR.PATCH')
    a, b, c = map(int, mm.groups())
    return {'major': f'{a + 1}.0.0', 'minor': f'{a}.{b + 1}.0', 'patch': f'{a}.{b}.{c + 1}'}[part]


def cmd_bump(args):
    m = market(args)
    e = m.entry(args.name) or die(f'{args.name!r} is not in the marketplace')
    pj_path = m.plugin_dir(args.name) / '.claude-plugin' / 'plugin.json'
    pj = read_json(pj_path)
    old_m, old_p = e.get('version'), pj.get('version')
    if old_m != old_p:
        print(f'  warning: versions disagree (marketplace {old_m}, plugin.json {old_p}); bumping the higher')
    key = lambda v: tuple(map(int, SEMVER_RE.match(v).groups())) if v and SEMVER_RE.match(v) else (-1,)
    old = max([v for v in (old_m, old_p) if v], key=key)
    new = _bump(old, args.part)
    e['version'] = pj['version'] = new
    m.save()
    write_json(pj_path, pj)
    print(f'{args.name}: {old} -> {new} (plugin.json and marketplace.json)')


def _scan_personal(path: Path):
    user = getpass.getuser()
    hits = []
    for f in sorted(path.rglob('*')):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXT or '__pycache__' in f.parts:
            continue
        for i, line in enumerate(f.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            why = []
            if HOME_RE.search(line):
                why.append('absolute home path')
            for em in EMAIL_RE.findall(line):
                if not any(ok in em.lower() for ok in EMAIL_OK):
                    why.append(f'email {em}')
            if user and len(user) > 2 and user in line:
                why.append(f'your username "{user}"')
            if why:
                hits.append(f'{f.relative_to(path)}:{i}: {", ".join(why)}')
    return hits


def cmd_check(args):
    m = market(args)
    names = args.names or [e['name'] for e in m.data.get('plugins', [])]
    errors, warnings = [], []
    readme = (m.root / 'README.md').read_text(encoding='utf-8') if (m.root / 'README.md').exists() else ''
    for name in names:
        e = m.entry(name)
        if not e:
            errors.append(f'{name}: not in marketplace.json')
            continue
        pdir = m.plugin_dir(name)
        if not pdir.is_dir():
            errors.append(f'{name}: source folder {pdir} missing')
            continue
        pj_path = pdir / '.claude-plugin' / 'plugin.json'
        if not pj_path.exists():
            errors.append(f'{name}: no .claude-plugin/plugin.json')
            continue
        pj = read_json(pj_path)
        if pj.get('name') != name:
            errors.append(f'{name}: plugin.json name is {pj.get("name")!r}')
        for where, v in (('plugin.json', pj.get('version')), ('marketplace.json', e.get('version'))):
            if not (v and SEMVER_RE.match(v)):
                errors.append(f'{name}: {where} version {v!r} is not MAJOR.MINOR.PATCH')
        if pj.get('version') != e.get('version'):
            errors.append(f'{name}: version {pj.get("version")} in plugin.json but '
                          f'{e.get("version")} in marketplace.json (run `bump`)')
        skills = m.skills(name)
        if not skills:
            errors.append(f'{name}: no skills/<skill>/ folder')
        for s in skills:
            sm = s / 'SKILL.md'
            if not sm.exists():
                errors.append(f'{name}/{s.name}: no SKILL.md')
                continue
            fm = frontmatter(sm)
            if fm is None:
                errors.append(f'{name}/{s.name}: SKILL.md has no --- frontmatter block')
                continue
            sname, desc = fm.get('name', ''), fm.get('description', '')
            if sname != s.name:
                errors.append(f'{name}/{s.name}: frontmatter name {sname!r} != folder name')
            if not NAME_RE.match(sname) or len(sname) > 64:
                errors.append(f'{name}/{s.name}: name must be kebab-case, at most 64 characters')
            if not desc:
                errors.append(f'{name}/{s.name}: empty description')
            elif len(desc) > 1024:
                errors.append(f'{name}/{s.name}: description is {len(desc)} characters (max 1024)')
            elif not re.search(r'\buse (it )?when\b', desc, re.I):
                warnings.append(f'{name}/{s.name}: description has no "Use when ..." trigger sentence')
            raw = next((l for l in sm.read_text(encoding='utf-8').splitlines()
                        if l.startswith('description:')), '')
            plain = raw[len('description:'):].strip()
            if plain and plain[0] not in '"\'>|' and (': ' in plain or ' #' in plain):
                warnings.append(f'{name}/{s.name}: unquoted description contains ": " or " #", '
                                'which YAML misreads; wrap it in double quotes')
            if 'TODO' in sm.read_text(encoding='utf-8'):
                warnings.append(f'{name}/{s.name}: SKILL.md still contains TODO')
            n = len(sm.read_text(encoding='utf-8').splitlines())
            if n > 500:
                warnings.append(f'{name}/{s.name}: SKILL.md is {n} lines; move detail to references/')
        for hit in _scan_personal(pdir / 'skills'):
            warnings.append(f'{name}: portability: {hit}')
        if readme and f'[{name}]' not in readme and f'`{name}`' not in readme:
            warnings.append(f'{name}: not mentioned in README.md')
    for w in warnings:
        print(f'WARN  {w}')
    for x in errors:
        print(f'ERROR {x}')
    claude = shutil.which('claude')
    if claude:
        for target in [m.root] + [m.plugin_dir(n) for n in names if m.entry(n)]:
            r = subprocess.run([claude, 'plugin', 'validate', str(target)], capture_output=True, text=True)
            ok = r.returncode == 0 and 'passed' in (r.stdout + r.stderr).lower()
            print(f'{"OK   " if ok else "ERROR"} claude plugin validate {target.relative_to(m.root) if target != m.root else "."}')
            if not ok:
                errors.append(f'claude plugin validate failed for {target}')
                print((r.stdout + r.stderr).strip())
    else:
        print('SKIP  claude CLI not found; `claude plugin validate` not run')
    print(f'\n{len(errors)} error(s), {len(warnings)} warning(s)')
    sys.exit(1 if errors else 0)


def cmd_test_install(args):
    m = market(args)
    if not m.entry(args.name):
        die(f'{args.name!r} is not in the marketplace')
    claude = shutil.which('claude') or die('claude CLI not found on PATH')
    tmp = tempfile.mkdtemp(prefix='skillkit-cc-')
    env = dict(os.environ, CLAUDE_CONFIG_DIR=tmp)
    try:
        steps = [[claude, 'plugin', 'marketplace', 'add', str(m.root)],
                 [claude, 'plugin', 'install', f'{args.name}@{m.name}'],
                 [claude, 'plugin', 'list']]
        out = ''
        for cmd in steps:
            r = subprocess.run(cmd, capture_output=True, text=True, env=env)
            out = (r.stdout + r.stderr).strip()
            print(f'$ {" ".join(cmd[1:])}\n{out}\n')
            if r.returncode != 0:
                die('test install failed at the step above')
        cached = list(Path(tmp, 'plugins').rglob('SKILL.md'))
        if f'{args.name}@{m.name}' not in out or not cached:
            die('plugin not listed after install, or no SKILL.md in the install cache')
        print(f'OK  {args.name}@{m.name} installs cleanly ({len(cached)} skill(s)); '
              f'throwaway config removed, your own config untouched')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _same_tree(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(str(a), str(b), ignore=['__pycache__', '.DS_Store'])
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errs = filecmp.cmpfiles(str(a), str(b), cmp.common_files, shallow=False)
    if mismatch or errs:
        return False
    return all(_same_tree(a / d, b / d) for d in cmp.common_dirs)


def cmd_link(args):
    m = market(args)
    if not m.entry(args.name):
        die(f'{args.name!r} is not in the marketplace')
    home_skills = Path.home() / '.claude' / 'skills'
    backups = Path.home() / '.claude' / 'skill-backups'
    for src in m.skills(args.name):
        dst = home_skills / src.name
        say = (lambda s: print(f'[dry run] {s}')) if args.dry_run else print
        if dst.is_symlink():
            if dst.resolve() == src.resolve():
                print(f'{dst} -> already linked to {src}')
                continue
            if not args.replace:
                print(f'{dst} is a link to {os.readlink(dst)}; rerun with --replace to repoint it')
                continue
            say(f'repoint {dst} -> {src}')
            if not args.dry_run:
                dst.unlink()
                dst.symlink_to(src, target_is_directory=True)
            continue
        if dst.exists():
            same = dst.is_dir() and _same_tree(dst, src)
            state = 'identical to the repo copy' if same else 'DIFFERENT from the repo copy'
            if not args.replace:
                print(f'{dst} is a real folder, {state}. Rerun with --replace to move it to '
                      f'{backups}/ and link the repo copy instead.')
                continue
            stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            bak = backups / f'{src.name}-{stamp}'
            say(f'move {dst} -> {bak} ({state})')
            say(f'link {dst} -> {src}')
            if not args.dry_run:
                backups.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dst), str(bak))
                dst.symlink_to(src, target_is_directory=True)
            continue
        say(f'link {dst} -> {src}')
        if not args.dry_run:
            home_skills.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src, target_is_directory=True)


def main(argv=None):
    ap = argparse.ArgumentParser(prog='skillkit.py', description=__doc__.split('\n\n')[0],
                                 epilog='Run `skillkit.py COMMAND -h` for a command\'s options.')
    ap.add_argument('--marketplace', metavar='PATH', help='marketplace folder (overrides the saved config)')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('config', help='show or save the marketplace folder')
    p.add_argument('--set', metavar='PATH')
    p.set_defaults(fn=cmd_config)

    p = sub.add_parser('init', help='create a new, empty marketplace folder')
    p.add_argument('path')
    p.add_argument('--name', required=True, help='marketplace name, kebab-case (users type plugin@NAME)')
    p.add_argument('--owner', required=True, help='owner name shown in marketplace.json')
    p.add_argument('--description')
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser('list', help='plugins, versions and skills')
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser('new', help='add a plugin holding one skill')
    p.add_argument('name')
    p.add_argument('--description', required=True, help='what it does + "Use when ..." (max 1024 chars)')
    p.add_argument('--from', dest='source', metavar='DIR', help='copy an existing skill folder instead of a skeleton')
    p.add_argument('--skill', metavar='S', help='skill folder name, if different from the plugin name')
    p.add_argument('--author', help='defaults to the marketplace owner')
    p.add_argument('--version', default='1.0.0')
    p.add_argument('--keywords', nargs='*')
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser('add-skill', help='add another skill folder to an existing plugin')
    p.add_argument('name', help='the plugin')
    p.add_argument('--from', dest='source', metavar='DIR', required=True, help='the skill folder to copy')
    p.add_argument('--skill', metavar='S', help='skill folder name (default: the source folder name)')
    p.set_defaults(fn=cmd_add_skill)

    p = sub.add_parser('bump', help='raise a plugin version in plugin.json and marketplace.json')
    p.add_argument('name')
    p.add_argument('part', nargs='?', default='patch', choices=['patch', 'minor', 'major'])
    p.set_defaults(fn=cmd_bump)

    p = sub.add_parser('check', help='lint plugins and run `claude plugin validate`')
    p.add_argument('names', nargs='*')
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser('test-install', help='install a plugin into a throwaway Claude config')
    p.add_argument('name')
    p.set_defaults(fn=cmd_test_install)

    p = sub.add_parser('link', help='link a plugin\'s skills into ~/.claude/skills')
    p.add_argument('name')
    p.add_argument('--replace', action='store_true', help='move an existing folder to ~/.claude/skill-backups/ first')
    p.add_argument('--dry-run', action='store_true')
    p.set_defaults(fn=cmd_link)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == '__main__':
    main()
