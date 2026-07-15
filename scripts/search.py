#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Section-level ranked search over the reference knowledge base.

`grep` returns matching lines; this returns the whole `##` sub-section that matches, ranked
across all references by relevance (term frequency, with a heading-match bonus). Use it to find
*which* reference and section answers a question, not just where a word appears.

Usage:
  python3 scripts/search.py consistent hashing
  python3 scripts/search.py idempotency --top 5 --full
  uv run scripts/search.py cache stampede
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

REF_DIR = Path(__file__).resolve().parent.parent / "skills" / "system-design" / "references"


def sections(path: Path):
    """Yield (heading, body) blocks split on `##` headings; text before the first is the intro."""
    heading, buf = f"({path.stem})", []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if buf:
                yield heading, "\n".join(buf).strip()
            heading, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if buf:
        yield heading, "\n".join(buf).strip()


def score(text: str, heading: str, terms: list[str]) -> int:
    hay, head = text.lower(), heading.lower()
    total, matched = 0, 0
    for t in terms:
        n = hay.count(t)
        if n or t in head:
            matched += 1
        total += n + (3 if t in head else 0)
    if len(terms) > 1:  # reward the exact phrase so it beats scattered single-word hits
        phrase = " ".join(terms)
        if phrase in head:
            total += 15
            matched += 1
        elif phrase in hay:
            total += 10
            matched += 1
    return total if matched else 0  # require at least one term present


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query", nargs="+", help="search terms")
    p.add_argument("--top", type=int, default=3, help="max results (default 3)")
    p.add_argument("--full", action="store_true", help="print the whole section, not a snippet")
    p.add_argument("--dir", type=Path, default=REF_DIR, help="references dir")
    args = p.parse_args()

    terms = [t.lower() for t in args.query]
    hits = []
    for f in sorted(args.dir.glob("*.md")):
        for heading, body in sections(f):
            s = score(heading + "\n" + body, heading, terms)
            if s:
                hits.append((s, f.stem, heading, body))
    hits.sort(key=lambda h: h[0], reverse=True)

    if not hits:
        log.info("no matches for: %s", " ".join(args.query))
        return 1

    q = " ".join(args.query)
    log.info("%d section(s) for '%s':\n", len(hits), q)
    for s, stem, heading, body in hits[: args.top]:
        log.info("── %s › %s  (score %d)", stem, heading, s)
        snippet = body if args.full else "\n".join(body.splitlines()[:6])
        log.info("%s\n", snippet)
    if len(hits) > args.top:
        log.info("(+%d more; raise --top)", len(hits) - args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
