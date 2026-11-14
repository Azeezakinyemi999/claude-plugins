#!/usr/bin/env python3
"""Make every code location in a technical-debt register a clickable link.

    python link_register.py <register.md> [--dry-run]
                            [--exclude PATH/ ...] [--prefer PATH/ ...]

--exclude  never link files whose repo path contains this fragment
           (data, archives, committed build copies). Repeatable.
--prefer   when a basename matches several tracked files, pick the one under
           this prefix (usually the profile's path base). Repeatable, in order.

Works in any git repo: the register must sit inside the repo it describes.

What it does (idempotent — safe to re-run):

* ``path:12``, ``path:12-30``, ``path:12, 40, 55`` -> relative links that open
  the file at that line (``../models/x.py#L12``). ``path`` may be a full
  repo path, a partial path (``plots/x.py``) or a unique basename.
* A bare ``L123`` links to the last file named earlier in the same list item;
  it is left as plain text when there is none, or when that file is a notebook
  (notebook links can open the file but cannot jump to a cell).
* Every detail heading (``#### A-01 ·``, ``### BUG-01 ·``) and refactor bullet
  (``- **R-01 ·``) gets an ``<a id="a-01"></a>`` anchor.
* Every index table gets a **Code** column linking the item's main location,
  and its ID cell links to the detail anchor.

Only files tracked by git and still on disk are linked, minus --exclude. The
review log lists every bare-L guess and every index row whose main location
came from the body rather than the heading -- read it.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
from urllib.parse import quote

EXT = (r'(?:py|pyi|pyx|ipynb|md|rst|txt|json|yaml|yml|toml|cfg|ini|in|sh|bash|zsh|'
       r'slurm|pbs|js|mjs|cjs|jsx|ts|tsx|vue|svelte|html|css|scss|sql|c|h|cc|cpp|hpp|'
       r'cu|f|f90|f95|jl|r|R|m|go|rs|java|kt|rb|php|swift|tex|bib|lammps|lmp|vasp|'
       r'xyz|cif|csv|tsv|dat)')
SPECIAL = r'(?:Makefile|Dockerfile|Snakefile|Justfile|\.gitignore|\.env\.example)'
PATH = rf'(?:(?:[A-Za-z0-9_\-]+/)*(?:{SPECIAL}|[A-Za-z0-9_\-.]+\.{EXT}))'
NUM = r'\d+(?:[-–]\d+)?'
LINES = rf'{NUM}(?:(?:,\s?|/):?{NUM})*'
REF_RE = re.compile(rf'(?<![A-Za-z0-9_/.\-])(?P<path>{PATH})(?::(?P<lines>{LINES}))?(?![A-Za-z0-9_])')
BARE_L_RE = re.compile(r'(?<![A-Za-z0-9_])L(?P<a>\d+)(?:[-–]L?(?P<b>\d+))?(?P<more>(?:,\s?\d+(?:[-–]\d+)?)*)(?![A-Za-z0-9_])')
LINK_RE = re.compile(r'\[[^\]]*\]\([^)]*\)')
CODE_RE = re.compile(r'`[^`]*`')
ITEM_START = re.compile(r'^\s*(?:[-*+]|\d+\.)\s')
# unit IDs: one capital letter (A-01 … Q-12); R-NN refactor candidates, BUG-NN bugs
ID_RE = r'(?:[A-Z]-\d{2,3}|BUG-\d{2,3})'
DETAIL_HEAD = re.compile(rf'^(#{{3,4}}) (?P<id>{ID_RE}) ·')
R_BULLET = re.compile(r'^- (?:<a id="[^"]+"></a>)?\*\*(?P<id>R-\d{2,3}) ·')


class Linker:
    def __init__(self, register, exclude=(), prefer=()):
        self.reg = os.path.abspath(register)
        self.reg_dir = os.path.dirname(self.reg)
        self.prefer = tuple(p.rstrip('/') + '/' for p in prefer)
        self.root = subprocess.check_output(
            ['git', '-C', self.reg_dir, 'rev-parse', '--show-toplevel'], text=True).strip()
        files = subprocess.check_output(['git', '-C', self.root, 'ls-files'], text=True).split('\n')
        # tracked AND still on disk -- a tracked file that was moved away would
        # otherwise produce a link that opens nothing
        self.tracked = [f for f in files if f and not any(x in f for x in exclude)
                        and os.path.exists(os.path.join(self.root, f))]
        self.cache: dict[str, str | None] = {}
        self.log: list[str] = []
        self.ambiguous: set[str] = set()

    # -- resolution -----------------------------------------------------------
    def resolve(self, token):
        if token in self.cache:
            return self.cache[token]
        cands = [f for f in self.tracked if f == token or f.endswith('/' + token)]
        if len(cands) > 1:
            def rank(f):
                hit = [i for i, p in enumerate(self.prefer) if f.startswith(p)]
                return (hit[0] if hit else len(self.prefer), f.count('/'), len(f))
            cands.sort(key=rank)
            self.ambiguous.add(f'{token} -> {cands[0]} (also: {", ".join(cands[1:3])})')
        self.cache[token] = cands[0] if cands else None
        return self.cache[token]

    def target(self, repo_path, line=None):
        rel = os.path.relpath(os.path.join(self.root, repo_path), self.reg_dir)
        url = quote(rel.replace(os.sep, '/'), safe='/._-')
        if line and not repo_path.endswith('.ipynb'):
            url += f'#L{line}'
        return url

    @staticmethod
    def text(s):
        return f'`{s}`' if '__' in s else s

    # -- one stretch of plain text (no links, no code spans) -------------------
    # Bare L-refs are linked only in the gaps *between* path refs, so a link this
    # pass just created is never re-scanned, and each L-ref sees the file named
    # most recently before it.
    def link_refs(self, s, ctx, where):
        out, pos = [], 0
        for m in REF_RE.finditer(s):
            f = self.resolve(m['path'])
            out.append(self.link_bare(s[pos:m.start()], ctx, where))
            pos = m.end()
            if f is None:
                out.append(m.group(0))
                continue
            ctx['file'] = f
            if not m['lines']:
                out.append(f'[{self.text(m["path"])}]({self.target(f)})')
                continue
            parts = re.split(r'((?:,\s?|/):?)', m['lines'])
            first = True
            for p in parts:
                if re.fullmatch(r'(?:,\s?|/):?', p):
                    out.append(p)
                    continue
                start = re.match(r'\d+', p).group(0)
                label = f'{m["path"]}:{p}' if first else p
                out.append(f'[{self.text(label)}]({self.target(f, start)})')
                first = False
        out.append(self.link_bare(s[pos:], ctx, where))
        return ''.join(out)

    def link_bare(self, s, ctx, where):
        def sub(m):
            f = ctx.get('file')
            if not f:
                self.log.append(f'  unlinked  {m.group(0):<14} | {where}')
                return m.group(0)
            if f.endswith('.ipynb'):
                return m.group(0)
            first = f'[{m.group(0)[:len(m.group(0)) - len(m["more"])]}]({self.target(f, m["a"])})'
            rest = re.sub(r'(\d+)(?:[-–]\d+)?',
                          lambda n: f'[{n.group(0)}]({self.target(f, n.group(1))})', m['more'])
            self.log.append(f'  {os.path.basename(f):<34} L{m["a"]:<6} | {where}')
            return first + rest
        return BARE_L_RE.sub(sub, s)

    def plain(self, s, ctx, where):
        out, pos = [], 0
        for m in CODE_RE.finditer(s):
            out.append(self.link_refs(s[pos:m.start()], ctx, where))
            inner = m.group(0)[1:-1]
            ref = REF_RE.fullmatch(inner)
            f = self.resolve(ref['path']) if ref else None
            if f:
                ctx['file'] = f
                start = re.match(r'\d+', ref['lines']).group(0) if ref['lines'] else None
                out.append(f'[{m.group(0)}]({self.target(f, start)})')
            else:
                out.append(m.group(0))
            pos = m.end()
        out.append(self.link_refs(s[pos:], ctx, where))
        return ''.join(out)

    def line(self, s, ctx, where):
        out, pos = [], 0
        for m in LINK_RE.finditer(s):      # leave existing links alone
            out.append(self.plain(s[pos:m.start()], ctx, where))
            out.append(m.group(0))
            pos = m.end()
        out.append(self.plain(s[pos:], ctx, where))
        return ''.join(out)

    # -- whole document -------------------------------------------------------
    def run(self, dry):
        lines = open(self.reg, encoding='utf-8').read().split('\n')
        out, ctx, fenced, current_id = [], {}, False, None
        primary: dict[str, tuple[str, str]] = {}   # id -> (link markdown, source)
        index_rows: list[int] = []
        in_index = False
        for i, ln in enumerate(lines):
            if ln.startswith('```'):
                fenced = not fenced
                out.append(ln)
                continue
            if fenced:
                out.append(ln)
                continue
            # an index table is any table whose header row starts "| ID |"
            if ln.startswith('| ID |'):
                in_index = True
            elif not ln.startswith('|'):
                in_index = False
            if in_index:
                index_rows.append(len(out))
                out.append(ln)
                continue
            if not ln.strip() or ln.startswith('#') or ln.startswith('|') or ITEM_START.match(ln):
                ctx = {}
            h = DETAIL_HEAD.match(ln) or R_BULLET.match(ln)
            if h:
                current_id = h['id']
                anchor = f'<a id="{current_id.lower()}"></a>'
                if R_BULLET.match(ln):
                    if anchor not in ln:
                        ln = ln.replace('- **', f'- {anchor}**', 1)
                elif anchor not in out[-3:]:
                    out += [anchor, '']
            new = self.line(ln, ctx, f'{current_id or "header"} L{i + 1}')
            if h:
                first = re.search(r'\[[^\]]*\]\([^)#]*#L\d+\)', new) or re.search(r'\[[^\]]*\]\([^)]*\)', new)
                if first:
                    primary[current_id] = (first.group(0), 'heading')
            elif current_id and current_id not in primary:
                first = re.search(r'\[[^\]]*\]\([^)#]*#L\d+\)', new)
                if first:
                    primary[current_id] = (first.group(0), 'body')
            out.append(new)

        # index tables: ID -> anchor link, add a Code column after the 2nd cell
        # (a table whose header already has Code was linked on an earlier run)
        has_code = False
        for k in index_rows:
            row = out[k]
            cells = row.split('|')
            if cells[1].strip() == 'ID':
                has_code = 'Code' in [c.strip() for c in cells]
            if has_code or len(cells) < 4:
                continue
            if cells[1].strip() == 'ID':
                cells.insert(3, ' Code ')
            elif re.fullmatch(r'\s*-+\s*', cells[1]):
                cells.insert(3, ' --- ')
            else:
                rid = re.sub(r'[\[\]]|\(#.*?\)', '', cells[1]).strip()
                cells[1] = f' [{rid}](#{rid.lower()}) '
                link = primary.get(rid, ('', ''))[0]
                cells.insert(3, f' {link} ')
            out[k] = '|'.join(cells)

        print('== bare-L resolutions (check these) ==')
        print('\n'.join(self.log))
        print('\n== index rows whose Code link came from the body, not the heading ==')
        for rid, (lnk, src) in primary.items():
            if src == 'body':
                print(f'  {rid}: {lnk}')
        missing = [r for r in re.findall(rf'^\| \[?({ID_RE})', '\n'.join(out), re.M)
                   if r not in primary]
        print('\n== index rows with no Code link ==\n  ' + ', '.join(sorted(set(missing))))
        print('\n== ambiguous basenames (resolved to the first) ==\n  ' + '\n  '.join(sorted(self.ambiguous)))
        text = '\n'.join(out)
        if dry:
            print(f'\n(dry run: {text.count("](")} links, nothing written)')
        else:
            open(self.reg, 'w', encoding='utf-8').write(text)
            print(f'\nwrote {self.reg} ({text.count("](")} links)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('register', help='path to the register .md (inside the repo it describes)')
    ap.add_argument('--dry-run', action='store_true', help='print the review log, write nothing')
    ap.add_argument('--exclude', action='append', default=[], metavar='PATH/',
                    help='skip tracked files whose path contains this (repeatable)')
    ap.add_argument('--prefer', action='append', default=[], metavar='PATH/',
                    help='prefix that wins when a basename is ambiguous (repeatable)')
    a = ap.parse_args()
    Linker(a.register, exclude=a.exclude, prefer=a.prefer).run(dry=a.dry_run)
