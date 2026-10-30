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
        "This tool is for educational illustration only. It excludes stamp duty, registration and brokerage. Verify figures with your bank or advisor.",
    "tools/prepay-vs-invest/index.html":
        "This tool is for educational illustration only. Actual returns and interest rates will vary. Verify figures with your bank or advisor.",
    "tools/expense-ratio-impact/index.html":
        "This tool is for educational illustration only. Expense ratios and market returns will vary. Check scheme information documents before investing.",
    "tools/rent-vs-buy/index.html":
        "This tool is for educational illustration only. Real estate and mutual fund returns vary. Verify figures with your advisor before acting.",
    "tools/loan-prepayment/index.html":
        "This tool is for educational illustration only. It excludes prepayment charges, fees and tax benefits. Confirm the revised schedule with your lender.",
    "tools/step-up-sip/index.html":
        "This tool is for educational illustration only. Returns, inflation and tax rules are assumptions and will vary. Check figures with your adviser or official sources.",
    "tools/sip-growth/index.html":
        "This tool is for educational illustration only. Actual returns will vary based on market conditions, fund choice, and tax rules.",
    "insights/emergency-fund-before-investing/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/what-a-sip-return-assumption-means/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/reduce-emi-or-reduce-tenure-after-prepayment/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/how-an-emi-splits-between-interest-and-principal/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/loan-vs-sip-hidden-tradeoffs/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/prepay-loan-vs-invest/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/direct-vs-regular-mutual-fund-expense-ratio/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/rent-vs-buy-india-wealth-comparison/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "tools/emergency-fund/index.html":
        "This tool is for educational illustration only. Actual reserve needs vary based on household risk. Verify with your advisor.",
    "tools/retirement-swp/index.html":
        "This tool is for educational illustration only. Post-retirement returns, inflation and tax rules will vary over time. Verify with your advisor.",
    "tools/term-insurance/index.html":
        "This tool is for educational illustration only. Insurance requirements vary based on personal health and debts. Check policy wording carefully.",
    "insights/sustainable-swp-rate-india-retirement/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/how-much-term-insurance-do-you-need/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "tools/asset-allocation/index.html":
        "This tool is for educational illustration only. Target mix is a rule of thumb, not advisory. Verify with your advisor.",
    "tools/net-worth-tracker/index.html":
        "This tool is for educational illustration only. Balance sheet metrics and ratios are guidelines. Verify with your financial advisor.",
    "tools/goal-planner/index.html":
        "This tool is for educational illustration only. Goal projections and returns are assumptions. Check current numbers before investing.",
    "insights/tax-smart-portfolio-rebalancing/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/financial-health-ratios-cash-flow/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
    "insights/how-to-prioritise-competing-financial-goals/index.html":
        "This article is for educational purposes only. Rates and tax rules change, so verify current figures with your bank, fund house or a qualified advisor.",
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