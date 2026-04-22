#!/usr/bin/env python3
"""Convert existing markdown frontmatter to press format."""

import os
import re
from datetime import datetime, timezone

SITE_DIR = "site"


def parse_frontmatter(content):
    """Extract frontmatter dict and body from markdown content."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    fm = {}
    # Simple YAML key: value and key:\n  - item parsing
    lines = fm_block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "" or val is None:
                # Check for list items on next lines
                items = []
                i += 1
                while i < len(lines) and lines[i].startswith("  - "):
                    items.append(lines[i][4:].strip())
                    i += 1
                fm[key] = items
                continue
            else:
                # Strip surrounding quotes
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                fm[key] = val
        i += 1

    return fm, body


def date_to_rfc3339(date_str):
    """Convert a date string like '2014-02-01' to RFC 3339."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return "2020-01-01T00:00:00Z"


def slug_from_filename(filename):
    """Derive a slug from the filename (strip date prefix if present)."""
    base = os.path.splitext(filename)[0]
    # Strip date prefix YYYY-MM-DD-
    m = re.match(r'^\d{4}-\d{2}-\d{2}-(.*)', base)
    if m:
        return m.group(1)
    return base


def build_press_frontmatter(old_fm, filename):
    title = old_fm.get("title", slug_from_filename(filename).replace("-", " ").title())

    alias = old_fm.get("slug", old_fm.get("alias", slug_from_filename(filename)))

    raw_tags = old_fm.get("categories", old_fm.get("tags", []))
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    tags = raw_tags

    weight = int(old_fm.get("weight", 0))

    # created_at: prefer 'date' then 'created_at', else derive from filename
    date_val = old_fm.get("date") or old_fm.get("created_at")
    if date_val:
        created_at = date_to_rfc3339(str(date_val))
    else:
        # Try to extract from filename
        m = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
        created_at = date_to_rfc3339(m.group(1)) if m else "2020-01-01T00:00:00Z"

    updated_at = old_fm.get("updated_at", created_at)

    lines = ['---']
    lines.append(f'title: "{title}"')
    lines.append(f'alias: "{alias}"')
    if tags:
        lines.append('tags:')
        for t in tags:
            lines.append(f'  - "{t}"')
    else:
        lines.append('tags: []')
    lines.append(f'weight: {weight}')
    lines.append(f'created_at: "{created_at}"')
    lines.append(f'updated_at: "{updated_at}"')
    lines.append('---')

    return "\n".join(lines)


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    old_fm, body = parse_frontmatter(content)
    filename = os.path.basename(filepath)
    new_fm = build_press_frontmatter(old_fm, filename)

    new_content = new_fm + "\n\n" + body
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  updated: {filepath}")


def main():
    processed = 0
    for root, dirs, files in os.walk(SITE_DIR):
        # Skip assets directories
        dirs[:] = [d for d in dirs if d != "assets"]
        for fname in files:
            if fname.endswith(".md"):
                process_file(os.path.join(root, fname))
                processed += 1

    print(f"\nDone. Processed {processed} files.")


if __name__ == "__main__":
    main()
