#!/usr/bin/env python3
"""sticky_notes.py -- spaced-review sticky notes for the learning-strategy skill.

Notes live in a CSV file, normally learning/<topic>/sticky-notes.csv, with the
columns: id, prompt, answer, source, created, due, interval_days, reviews,
lapses. Dates are YYYY-MM-DD.

Commands:
  add   CSV --prompt P --answer A [--source S]   add a note, due tomorrow
  due   PATH [--next]                            prompts due today (no answers)
  show  CSV ID                                   one note's prompt and answer
  mark  CSV ID --result right|wrong              reschedule after a review
  list  CSV                                      every note and its due date

PATH for `due` is one CSV file or a folder such as learning/, in which case
every <folder>/*/sticky-notes.csv is read. A right answer moves a note along
1 -> 3 -> 7 -> 14 -> 30 -> 60 days; a wrong one sends it back to 1 day.

Writes only the CSV named on the command line, and only with `add` or
`mark`. Both take --dry-run. Standard library only; Python 3.7+.
"""

import argparse
import csv
import datetime as dt
import os
import sys
import tempfile
from pathlib import Path

FIELDS = ['id', 'prompt', 'answer', 'source', 'created', 'due',
          'interval_days', 'reviews', 'lapses']
LADDER = [1, 3, 7, 14, 30, 60]
FILENAME = 'sticky-notes.csv'


def die(msg):
    print('error: ' + msg, file=sys.stderr)
    sys.exit(2)


def parse_day(text):
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        die('{!r} is not a date in YYYY-MM-DD form'.format(text))


def today(args):
    return parse_day(args.today) if args.today else dt.date.today()


def read_notes(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        missing = [c for c in FIELDS if c not in (reader.fieldnames or [])]
        if missing:
            die('{} is missing columns: {}'.format(path, ', '.join(missing)))
        rows = list(reader)
    for row in rows:
        for key in ('id', 'interval_days', 'reviews', 'lapses'):
            try:
                row[key] = int(row[key])
            except (TypeError, ValueError):
                die('{}: note {!r} has a bad {} value {!r}'.format(
                    path, row.get('id'), key, row.get(key)))
        parse_day(row['due'])
    return rows


def write_notes(path, rows):
    """Write atomically: a temp file in the same folder, then replace."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(prefix='.sticky-', suffix='.csv', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row[k] for k in FIELDS})
        os.replace(tmp, str(path))
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def find(rows, note_id, path):
    for row in rows:
        if row['id'] == note_id:
            return row
    die('{} has no note with id {}'.format(path, note_id))


def csv_files(path):
    """One CSV, or every <folder>/*/sticky-notes.csv (plus <folder>/sticky-notes.csv)."""
    p = Path(path)
    if p.is_file():
        return [p]
    if p.is_dir():
        found = sorted(p.glob('*/' + FILENAME))
        if (p / FILENAME).is_file():
            found.insert(0, p / FILENAME)
        return found
    die('{} does not exist'.format(p))


def topic_of(path):
    return Path(path).resolve().parent.name


# ---- commands ---------------------------------------------------------------

def cmd_add(args):
    path = Path(args.csv)
    if not path.parent.is_dir():
        die('folder {} does not exist; create the study folder first'.format(path.parent))
    prompt, answer = args.prompt.strip(), args.answer.strip()
    if not prompt or not answer:
        die('--prompt and --answer must not be empty')
    rows = read_notes(path)
    for row in rows:
        if row['prompt'].strip().lower() == prompt.lower():
            die('note {} already has this prompt; review or edit it instead'.format(row['id']))
    day = today(args)
    row = {
        'id': max([r['id'] for r in rows] or [0]) + 1,
        'prompt': prompt,
        'answer': answer,
        'source': (args.source or '').strip(),
        'created': day.isoformat(),
        'due': (day + dt.timedelta(days=LADDER[0])).isoformat(),
        'interval_days': LADDER[0],
        'reviews': 0,
        'lapses': 0,
    }
    if args.dry_run:
        print('dry run: would add note {} to {}, due {}'.format(row['id'], path, row['due']))
        return
    write_notes(path, rows + [row])
    print('added note {} to {}, due {}'.format(row['id'], path, row['due']))


def cmd_due(args):
    day = today(args)
    files = csv_files(args.path)
    due, upcoming = [], []
    for f in files:
        for row in read_notes(f):
            entry = (parse_day(row['due']), topic_of(f), f, row)
            (due if entry[0] <= day else upcoming).append(entry)
    if args.next:
        if due:
            print('{} note(s) due now ({})'.format(len(due), day.isoformat()))
        elif upcoming:
            first = min(e[0] for e in upcoming)
            n = sum(1 for e in upcoming if e[0] == first)
            print('next review: {} ({} note(s))'.format(first.isoformat(), n))
        else:
            print('no sticky notes found')
        return
    if not due:
        msg = 'nothing due on {}'.format(day.isoformat())
        if upcoming:
            msg += '; next review {}'.format(min(e[0] for e in upcoming).isoformat())
        print(msg)
        return
    due.sort(key=lambda e: (e[0], e[1], e[3]['id']))
    print('{} note(s) due on {} (answers hidden; use `show`):'.format(len(due), day.isoformat()))
    for when, topic, f, row in due:
        late = (day - when).days
        tag = ' [{} day(s) late]'.format(late) if late > 0 else ''
        print('  {} #{}: {}{}   ({})'.format(topic, row['id'], row['prompt'], tag, f))


def cmd_show(args):
    rows = read_notes(args.csv)
    row = find(rows, args.id, args.csv)
    print('#{} prompt: {}'.format(row['id'], row['prompt']))
    print('#{} answer: {}'.format(row['id'], row['answer']))
    if row['source']:
        print('#{} source: {}'.format(row['id'], row['source']))


def cmd_mark(args):
    path = Path(args.csv)
    rows = read_notes(path)
    row = find(rows, args.id, path)
    day = today(args)
    if args.result == 'right':
        bigger = [n for n in LADDER if n > row['interval_days']]
        interval = bigger[0] if bigger else LADDER[-1]
    else:
        interval = LADDER[0]
        row['lapses'] += 1
    row['interval_days'] = interval
    row['reviews'] += 1
    row['due'] = (day + dt.timedelta(days=interval)).isoformat()
    verb = 'dry run: would mark' if args.dry_run else 'marked'
    print('{} note {} {}; next review {} (in {} day(s))'.format(
        verb, row['id'], args.result, row['due'], interval))
    if not args.dry_run:
        write_notes(path, rows)


def cmd_list(args):
    rows = read_notes(args.csv)
    if not rows:
        print('no notes in {}'.format(args.csv))
        return
    for row in sorted(rows, key=lambda r: (r['due'], r['id'])):
        print('#{:<3} due {}  every {:>2}d  reviews {}  misses {}  {}'.format(
            row['id'], row['due'], row['interval_days'], row['reviews'],
            row['lapses'], row['prompt']))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__.split('\n\n')[0],
        epilog='Run `sticky_notes.py COMMAND -h` for a command\'s options.')
    sub = ap.add_subparsers(dest='cmd')
    sub.required = True

    def common(p, writes=False):
        p.add_argument('--today', metavar='YYYY-MM-DD',
                       help='treat this date as today (for testing)')
        if writes:
            p.add_argument('--dry-run', action='store_true',
                           help='print what would change; write nothing')

    p = sub.add_parser('add', help='add a note, due tomorrow')
    p.add_argument('csv', help='the CSV file, e.g. learning/<topic>/sticky-notes.csv')
    p.add_argument('--prompt', required=True, help='the question shown first')
    p.add_argument('--answer', required=True, help='the hidden answer')
    p.add_argument('--source', help='where it came from, e.g. "step 9 quiz"')
    common(p, writes=True)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser('due', help='prompts due today, answers hidden')
    p.add_argument('path', help='a CSV file, or a folder such as learning/')
    p.add_argument('--next', action='store_true', help='print only the next review date')
    common(p)
    p.set_defaults(func=cmd_due)

    p = sub.add_parser('show', help="one note's prompt and answer")
    p.add_argument('csv')
    p.add_argument('id', type=int)
    p.set_defaults(func=cmd_show)

    p = sub.add_parser('mark', help='reschedule a note after a review')
    p.add_argument('csv')
    p.add_argument('id', type=int)
    p.add_argument('--result', required=True, choices=['right', 'wrong'])
    common(p, writes=True)
    p.set_defaults(func=cmd_mark)

    p = sub.add_parser('list', help='every note and its due date')
    p.add_argument('csv')
    p.set_defaults(func=cmd_list)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
