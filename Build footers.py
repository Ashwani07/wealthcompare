"""
build_footers.py

Syncs footer-template.html into every page listed in PAGES below, filling in
each page's own disclaimer line (or none, for About/Privacy/Terms).

Run this BEFORE every deploy, any time footer-template.html changes, or any
time a new page is added (just add it to PAGES).

Usage:
    python3 build_footers.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE_PATH = ROOT / "footer-template.html"

# path (relative to this script) -> disclaimer text, or None for no disclaimer line
PAGES = {
    "index.html":
        "This site is for educational comparison only. Always verify numbers with your bank, advisor, or official documents.",
    "tools/emi-calculator/index.html":
        "This tool is for educational illustration only. Verify figures with your bank before making a decision.",
    "tools/loan-vs-sip/index.html":
        "This tool is for educational illustration only. It excludes stamp duty, registration, and brokerage — verify figures with your bank or advisor.",
    "tools/sip-growth/index.html":
        "This tool is for educational illustration only. Actual returns will vary based on market conditions, fund choice, and tax rules.",
    "about/index.html": None,
    "privacy-policy/index.html": None,
    "terms/index.html": None,
}

FOOTER_RE = re.compile(r"<footer class=\"footer\">.*?</footer>", re.DOTALL)


def render_footer(template: str, disclaimer: str | None) -> str:
    if disclaimer:
        block = f'\n    <div style="margin-top:6px;">\n        {disclaimer}\n    </div>'
    else:
        block = ""
    return template.replace("{{DISCLAIMER}}", block).strip()


def main():
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    updated, skipped = [], []

    for rel_path, disclaimer in PAGES.items():
        page_path = ROOT / rel_path
        if not page_path.exists():
            skipped.append(rel_path)
            continue

        html = page_path.read_text(encoding="utf-8")
        footer_html = render_footer(template, disclaimer)

        if not FOOTER_RE.search(html):
            print(f"WARNING: no <footer class=\"footer\"> found in {rel_path} — skipped, add one manually first.")
            skipped.append(rel_path)
            continue

        new_html = FOOTER_RE.sub(footer_html, html, count=1)
        if new_html != html:
            page_path.write_text(new_html, encoding="utf-8")
            updated.append(rel_path)

    print(f"Footer synced: {len(updated)} updated, {len(skipped)} skipped.")
    for p in updated:
        print(f"  updated: {p}")
    for p in skipped:
        print(f"  skipped: {p}")


if __name__ == "__main__":
    main()