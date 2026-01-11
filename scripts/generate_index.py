#!/usr/bin/env python3
"""
generate_index.py

Scan a year-drafts/<YEAR>/ directory for markdown files and generate an index.json
listing each file with metadata (file, title, date, summary).

Usage:
  python3 scripts/generate_index.py 2026

If no year is provided, defaults to 2026.
The script extracts YAML-like front-matter if present (--- ... ---) and looks for
`title`, `date`, and `summary` keys. If missing, it derives a title from the filename.

This script has no external dependencies and writes year-drafts/<YEAR>/index.json.
"""

import sys
from pathlib import Path
import json
import re

FRONT_MATTER_RE = re.compile(r"^---\s*\n([\s\S]*?)\n---\s*\n", re.MULTILINE)
KV_RE = re.compile(r"^(title|date|summary)\s*:\s*(.*)$", re.IGNORECASE)


def parse_front_matter(text):
    m = FRONT_MATTER_RE.search(text)
    if not m:
        return {}
    fm = m.group(1)
    data = {}
    for line in fm.splitlines():
        k = KV_RE.match(line.strip())
        if k:
            key = k.group(1).lower()
            val = k.group(2).strip().strip('"').strip("'")
            data[key] = val
    return data


def slug_title_from_filename(name):
    name = Path(name).stem
    # remove leading year- prefix if present
    name = re.sub(r'^\d{4}[-_]?','', name)
    name = name.replace('-', ' ').replace('_',' ')
    return name.title()


def gen_index(year='2026'):
    base = Path.cwd()
    drafts_dir = base / 'year-drafts' / str(year)
    if not drafts_dir.exists() or not drafts_dir.is_dir():
        print(f"Error: directory not found: {drafts_dir}")
        return 2

    entries = []
    for p in sorted(drafts_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() not in ('.md', '.markdown'):
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: failed to read {p}: {e}")
            continue
        fm = parse_front_matter(text)
        title = fm.get('title') or slug_title_from_filename(p.name)
        date = fm.get('date') or ''
        summary = fm.get('summary') or ''
        entries.append({'file': p.name, 'title': title, 'date': date, 'summary': summary})

    # sort: prefer files with date (desc), then README first, then filename
    def sort_key(e):
        if e['file'].lower() == 'readme.md':
            return (2, '')  # put README near top (we'll reverse later)
        return (1, e.get('date',''))

    # Put README first, then by date descending
    entries_sorted = sorted(entries, key=lambda e: (0 if e['file'].lower()=='readme.md' else 1, e.get('date','')), reverse=True)

    out_path = drafts_dir / 'index.json'
    out_path.write_text(json.dumps(entries_sorted, indent=2), encoding='utf-8')
    print(f"Wrote {out_path} ({len(entries_sorted)} entries)")
    return 0


if __name__ == '__main__':
    year = sys.argv[1] if len(sys.argv) > 1 else '2026'
    sys.exit(gen_index(year))
