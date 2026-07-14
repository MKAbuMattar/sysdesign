#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown", "weasyprint", "python-docx", "htmldocx"]
# ///
"""Export the system-design reference files into a single numbered bundle (md + PDF + docx).

Independent and self-contained: resolves every path relative to this script, reads no config,
makes no network calls, and works in any checkout. PDF/docx are best-effort — if an optional
dependency can't load, the Markdown bundle is still produced and the run still succeeds.
"""
from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
REF_DIR = REPO / "skills" / "system-design" / "references"
DIAGRAM_DIR = REPO / "artifacts" / "diagrams"

# Reading order for the bundle (generic system-design curriculum). Files not present are skipped.
ORDER = [
    "architecture-patterns.md", "api-web.md", "networking.md", "data-storage.md",
    "caching-performance.md", "distributed-systems.md", "os-concurrency.md",
    "security-auth.md", "payments.md", "ai-ml-systems.md", "devops-k8s.md",
    "dev-tools.md", "case-studies.md", "interview.md",
]

HEADING = re.compile(r"^(#{1,6})(\s)")
TITLE = re.compile(r"^#\s+(.*)$")

CSS = """
@page { margin: 2cm; }
body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; line-height: 1.5; font-size: 11pt; }
h1 { border-bottom: 2px solid #333; padding-bottom: 4px; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
code, pre { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 9.5pt; }
pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ccc; padding: 4px 8px; text-align: left; }
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-o", "--out", type=Path, default=REPO / "dist", help="Output directory (default: ./dist)")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    return p.parse_args()


def read_reference(path: Path) -> tuple[str, str]:
    """Return (title, body-without-the-H1) for a reference file."""
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()
    title = path.stem
    body_start = 0
    for i, line in enumerate(lines):
        m = TITLE.match(line)
        if m:
            title = m.group(1).strip()
            body_start = i + 1
            break
    return title, "\n".join(lines[body_start:]).strip()


def shift_headings(md: str) -> str:
    """Demote every heading one level so file sections nest under the bundle's H1."""
    out = []
    for line in md.splitlines():
        m = HEADING.match(line)
        out.append(("#" + line) if m and len(m.group(1)) < 6 else line)
    return "\n".join(out)


def diagrams_section() -> str:
    if not DIAGRAM_DIR.is_dir():
        return ""
    parts = ["# Diagrams\n"]
    for mmd in sorted(DIAGRAM_DIR.glob("*.mmd")):
        name = mmd.stem.replace("-", " ").title()
        parts.append(f"## {name}\n\n```mermaid\n{mmd.read_text(encoding='utf-8').strip()}\n```\n")
    return "\n".join(parts)


def build_bundle(out: Path) -> str:
    """Assemble the combined Markdown and write per-topic numbered files. Returns combined md."""
    standard_dir = out / "standard"
    standard_dir.mkdir(parents=True, exist_ok=True)
    sections = ["# System Design — Reference Standard\n",
                "A self-contained, tradeoff-first reference. Generic; not tied to any stack or vendor.\n",
                "## Contents\n"]
    bodies, n = [], 0
    for fname in ORDER:
        path = REF_DIR / fname
        if not path.exists():
            logger.warning("skipping missing reference: %s", fname)
            continue
        n += 1
        title, body = read_reference(path)
        sections.append(f"{n}. {title}")
        bodies.append(f"# {n}. {title}\n\n{shift_headings(body)}\n")
        (standard_dir / f"{n:02d}-{path.stem}.md").write_text(
            f"# {n}. {title}\n\n{body}\n", encoding="utf-8")
    combined = "\n".join(sections) + "\n\n" + "\n\n".join(bodies) + "\n\n" + diagrams_section()
    logger.info("bundled %d reference files → %s", n, standard_dir)
    return combined


def render_svgs(out: Path) -> None:
    """Render diagrams to SVG if the mermaid CLI (mmdc) is available; otherwise skip quietly."""
    mmdc = shutil.which("mmdc")
    if not mmdc or not DIAGRAM_DIR.is_dir():
        logger.info("mmdc not found — diagrams stay as ```mermaid source (renders on GitHub)")
        return
    svg_dir = out / "diagrams"
    svg_dir.mkdir(parents=True, exist_ok=True)
    for mmd in sorted(DIAGRAM_DIR.glob("*.mmd")):
        try:
            subprocess.run([mmdc, "-i", str(mmd), "-o", str(svg_dir / f"{mmd.stem}.svg")],
                           check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.warning("mmdc failed for %s: %s", mmd.name, e)
    logger.info("rendered SVGs → %s", svg_dir)


def main() -> int:
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    try:
        out: Path = args.out
        out.mkdir(parents=True, exist_ok=True)
        combined = build_bundle(out)

        md_path = out / "system-design-standard.md"
        md_path.write_text(combined, encoding="utf-8")
        logger.info("wrote %s", md_path)

        try:
            import markdown  # noqa: PLC0415
            html = "<style>%s</style>\n%s" % (
                CSS, markdown.markdown(combined, extensions=["tables", "fenced_code", "sane_lists"]))
        except ImportError:
            logger.warning("`markdown` unavailable — skipping PDF and docx (Markdown bundle is ready)")
            return 0

        try:
            from weasyprint import HTML  # noqa: PLC0415
            HTML(string=html).write_pdf(str(out / "system-design-standard.pdf"))
            logger.info("wrote %s", out / "system-design-standard.pdf")
        except Exception as e:  # weasyprint pulls system libs; degrade, don't fail
            logger.warning("PDF skipped (%s): %s", type(e).__name__, e)

        try:
            from docx import Document  # noqa: PLC0415
            from htmldocx import HtmlToDocx  # noqa: PLC0415
            doc = Document()
            HtmlToDocx().add_html_to_document(html, doc)
            doc.save(str(out / "system-design-standard.docx"))
            logger.info("wrote %s", out / "system-design-standard.docx")
        except Exception as e:
            logger.warning("docx skipped (%s): %s", type(e).__name__, e)

        render_svgs(out)
        logger.info("done → %s", out)
        return 0
    except FileNotFoundError as e:
        logger.error("path not found: %s", e)
        return 2
    except Exception:
        logger.exception("unexpected error")
        return 2


if __name__ == "__main__":
    sys.exit(main())
