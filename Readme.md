# WealthCompare

Free personal-finance calculators and short articles for Indian households, at [wealthcompare.in](https://wealthcompare.in).

The aim is simple. Show what a money decision does in **today's rupees** as well as future rupees, state every assumption in plain words, and keep the tools educational. Nothing here recommends a fund, stock, lender or broker.

Last updated: 12 October 2026.

---

## How the site is built

- Static HTML, CSS and plain JavaScript. No framework and no build step beyond one small Python script.
- Hosted on Cloudflare Pages.
- Every page lives at `/<section>/<slug>/index.html`.
- Shared styling is in `assets/css/site.css` (loaded as `?v=6`). Bump the version number in every page when you change it.
- Shared scripts are in `assets/js/`: `amount-words.js` (amount in words under inputs), `export-excel.js` (Export to Excel button) and `ad-slot-collapse.js`.
- Charts use Chart.js 4.4.4 and spreadsheet export uses SheetJS 0.18.5, both pinned and loaded from jsDelivr.
- Ads: the AdSense Auto Ads script is in the head of each page. See "Ads" below.

## Folder layout

```
/
├── index.html                  Homepage
├── 404.html
├── ads.txt                     AdSense publisher line
├── robots.txt
├── sitemap.xml                 Keep lastmod dates current
├── site.webmanifest
├── favicon.ico
├── build_footers.py            Syncs the footer into every page (see below)
├── footer-template.html        The footer, with a {{DISCLAIMER}} placeholder
├── WealthCompare Excel Calculator.xlsx   Offline development reference only; not served on the website.
├── README.md                   This file
├── calculator-ui-notes.md      How the tool pages are built: page pattern, tax rules, validation, ads, chart sizing
├── paid-features.txt           Monetization status, options and the feature backlog (nothing here is decided)
├── folder-tree.txt             Folder listing
├── about/ privacy-policy/ terms/
├── Articles/                   Markdown sources for the articles
├── assets/
│   ├── logo.svg  og-image.png
│   ├── css/site.css
│   ├── icons/
│   └── js/                     amount-words.js, export-excel.js, ad-slot-collapse.js
├── insights/                   Articles
│   ├── emergency-fund-before-investing/
│   ├── loan-vs-sip-hidden-tradeoffs/
│   ├── what-a-sip-return-assumption-means/
│   └── reduce-emi-or-reduce-tenure-after-prepayment/
└── tools/                      Calculators
    ├── emi-calculator/
    ├── loan-vs-sip/
    ├── sip-growth/
    ├── loan-prepayment/
    └── step-up-sip/
```

---

## Tools

| Tool | Path | What it answers | State |
|---|---|---|---|
| EMI Calculator | `/tools/emi-calculator/` | EMI, total interest, total repayment, yearly split between interest and principal | Live. Reworked, matches the workbook |
| Loan vs SIP | `/tools/loan-vs-sip/` | If you already own a home: buy a second property with a loan, or invest the same down payment and EMI in a SIP | Live. Reworked, matches the workbook |
| SIP Growth | `/tools/sip-growth/` | What a SIP grows to, before and after tax, in today's rupees | Live. Reworked, matches the workbook |
| Loan Prepayment | `/tools/loan-prepayment/` | Lump sums, monthly extra, rate change: effect on tenure and interest | Live. Matches the workbook |
| Step-Up SIP Goal | `/tools/step-up-sip/` | Starting SIP for a goal when you raise it each year | Live. Matches the workbook |
| Prepay vs Invest | `/tools/prepay-vs-invest/` | Prepay loan vs invest surplus in equity SIP: hurdle rate, early debt-free month, terminal wealth | Live. Matches the workbook |
| Expense Ratio Impact | `/tools/expense-ratio-impact/` | Direct vs Regular mutual funds: compounding cost of distributor commissions | Live. Matches the workbook |
| Rent vs Buy | `/tools/rent-vs-buy/` | Buy with home loan vs rent and invest down payment + monthly difference in mutual funds | Live. Matches the workbook |

Workbook sheets not yet converted to web pages: Prepay vs Invest, Retirement SWP, Emergency Fund, Net Worth & Cash Flow, Term Insurance, Asset Allocation, Goal Dashboard, Expense Ratio Impact, Rent vs Buy (plus its Sensitivity sheet). Rent vs Buy and Expense Ratio Impact had a lighter review than the others. Re-verify them before converting.

All tools follow one layout: verdict first, a collapsed full breakdown, an "Advanced Read", a chart, inline field errors, and Export to Excel.

## Articles

| Article | Path |
|---|---|
| Emergency Fund Before Investing | `/insights/emergency-fund-before-investing/` |
| Loan vs SIP: The Hidden Trade-offs | `/insights/loan-vs-sip-hidden-tradeoffs/` |
| What a SIP Return Assumption Really Means | `/insights/what-a-sip-return-assumption-means/` |
| Reduce EMI or Reduce Tenure After a Prepayment? | `/insights/reduce-emi-or-reduce-tenure-after-prepayment/` |
| How Your EMI Splits Between Interest and Principal | /insights/how-an-emi-splits-between-interest-and-principal/ |
| Prepay Loan vs Invest: The Mathematics of Surplus Cash | /insights/prepay-loan-vs-invest/ |
| Direct vs Regular Mutual Funds: How a 1% Fee Costs ₹23 Lakh | /insights/direct-vs-regular-mutual-fund-expense-ratio/ |

| Rent vs Buy in India: Why the 30x Rule of Thumb is Broken | /insights/rent-vs-buy-india-wealth-comparison/ |
Planned: real vs nominal wealth.

---

## The workbook is the source of truth

WealthCompare Excel Calculator.xlsx is strictly an offline mathematical reference and source of truth for development; it is never linked or served directly to users. Each web tool runs client-side JavaScript that independently matches its sheet.

- Defaults and shared assumptions (inflation, return, tax rate, exemption, loan rate, property tax, selling cost, LTV bands) sit on the **Common Assumptions** sheet.
- Read `calculator-ui-notes.md` before building a tool. It records the page pattern and the reasons behind each convention.
- If a page and its sheet disagree, find out which is right, fix the workbook first, then fix the page. Never patch only the page.
- A sheet's hidden engine sheets (Prepayment Engine, PVI Engine) carry the month-by-month calculation. Do not delete them.

### Conventions every tool follows

1. **Real and nominal stay consistent on both sides.** A future amount is divided by (1 + inflation)^years. Money paid in over time is brought back to today's rupees year by year, using the year each instalment falls in (`ceil(month / 12)`), not left as a plain total. The down payment is paid today and is not discounted.
2. **Tax is applied once, at redemption.** SIP gains: 12.5% on the gain above ₹1,25,000. Tools treat all gains as long-term and say so. Cess, surcharge, exit loads and fund costs are not included.
3. **Monthly compounding** at the yearly rate divided by 12. SIP instalments go in at the end of the month.
4. **No hard return figures in evergreen content.** Any rate shown is a labelled assumption.
5. **Educational only.** No tool or article recommends a fund, stock, lender or product.

---

## Standards for any new content

- **Verify every tax or regulatory figure on an official source before writing it.** Allowed sources: incometaxindia.gov.in, sebi.gov.in, rbi.org.in, dicgc.org.in, nism.ac.in. If there is no official source, say so and soften the claim.
- The Income-tax Act, 2025 replaced the 1961 Act on 1 April 2026. Use the new section number and put the old one in brackets, for example "Section 198 (Section 112A of the 1961 Act)".
- "Checked on" and "published" dates use the real date, never one copied from elsewhere.
- Simple language, short sentences, specific numbers. Put complexity in a collapsible "Advanced Read". Avoid stock phrases and em dashes.
- Do not recommend specific funds or stocks.

### What has been verified

| Fact | Source |
|---|---|
| Long-term gains on equity-oriented fund units: 12.5% above ₹1,25,000; 65% equity test | Income-tax Act, 2025, Section 198 on incometaxindia.gov.in (the same provisions appear under Section 112A of the 1961 Act) |
| Short-term gains on equity-oriented fund units: 20% | Income-tax Act, 2025, Section 196 on incometaxindia.gov.in |
| Property long-term gains: 12.5% without indexation; resident individuals who bought land or buildings before 23 July 2024 can choose 20% with indexation | Income Tax Department, capital gains page |
| Loan-to-value limits for individual housing loans: 90% up to ₹30 lakh, 80% up to ₹75 lakh, 75% above | RBI Master Circular, Housing Finance (18 February 2022) on rbi.org.in. A later version exists, so link the latest |
| No pre-payment charges on floating-rate loans to individuals for non-business purposes, for loans sanctioned or renewed from 1 January 2026 | RBI (Pre-payment Charges on Loans) Directions, 2025, RBI/2025-26/64 |
| When floating rates reset, lenders must offer a higher EMI or more EMIs, a switch to a fixed rate where offered, and prepayment at any time | RBI FAQs on reset of floating interest rate on EMI based loans |

### Not verified yet

- The 12-month holding period for equity-oriented units under the 2025 Act (taken from a 1961-Act page).
- The Income-tax Act, 2025 section for property gains.
- The Section 156 rebate and the ₹12 lakh limit.
- The SEBI mutual fund advertisement code wording on a SEBI page. The AMFI guideline (a 2% to 13% return range for fund companies' calculators) was used as a sanity check only.

---

## Everyday tasks

### Sync the footer into every page

Run this before every deploy, and any time the footer changes or a page is added:

```
python3 build_footers.py
```

It copies `footer-template.html` into each page listed in `PAGES` inside the script, filling in that page's own disclaimer. To add a page, add one entry to `PAGES` with its disclaimer text. A page whose footer is already correct is left unchanged, so running it twice does no harm.

### Add a new tool

1. Build or finish the sheet in the workbook. Put shared inputs on Common Assumptions.
2. Copy an existing tool page as the template (Loan Prepayment or Step-Up SIP are the cleanest). Keep the same classes and layout.
3. Port the formulas from the sheet. Do not invent new maths.
4. Check the page against the workbook for at least eight cases: the defaults, zero rate, zero tenure or the shortest allowed, the longest allowed, a result that goes negative, and one extreme value for each input.
5. Add the footer disclaimer to `build_footers.py` and run it.
6. Add the page to `sitemap.xml` with today's date and to the homepage tools grid.
7. Add a link from a related article, and a link to the tool from the article.

### Add a new article

1. Copy `insights/what-a-sip-return-assumption-means/` as the template.
2. Every number must come from a calculator or a script. State the assumptions. Label rates as examples.
3. Verify any tax or regulatory fact (see the standards above) and list it under "Sources and Verification" with the date checked.
4. Add it to `sitemap.xml`, the homepage Insights grid, `build_footers.py`, and the "Keep reading" links of related articles.

### Update the sitemap

Change `lastmod` on a page whenever its content changes. The date is the real date. Do not leave stale dates.

### Test a page

There is no test folder in the repository yet. The approach used so far:

1. Load the page in jsdom with the chart, export and amount-words scripts replaced by stubs.
2. Set the inputs, call the page's calculate function, and read the result object.
3. Recalculate the same inputs in the workbook (for example with LibreOffice in headless mode) and compare every summary number and every row of the schedule.
4. Check validation, the Real/Nominal toggle, the empty and error cases, and that no `NaN`, `undefined` or `Infinity` appears anywhere on the page.

Adding these scripts to a `tests/` folder would make the checks repeatable. Dynamic-array functions such as `XMATCH` do not recalculate in LibreOffice, so compare payoff months from the engine's balance columns instead.

---

## Ads

- AdSense Auto Ads are loaded from the head of each page (publisher `ca-pub-4357149194740826`).
- `ads.txt` must contain exactly: `google.com, pub-4357149194740826, DIRECT, f08c47fec0942fa0`
- The homepage still has three manual ad units with slot IDs that look like placeholders (`300000001` to `300000003`). Replace them with real slot IDs from AdSense or remove the manual units.
- All five tool pages and the articles contain no manual ad units.
- AdSense status last seen: "Needs attention, Low value content" (8 September 2026). More original articles are being added before a review is requested. Monetization beyond ads is undecided. Decision as of 12 October 2026: no accounts, email capture or payment collection for now; see `paid-features.txt`.

---

## Known open items

- Homepage ad slot IDs (above).
- `build_footers.py` does not yet list the Loan vs SIP article, because its page was not available to check.
- `EMI Calculator` sheet: the yearly schedule has 20 rows while tenure can go to 40, the schedule errors at a 0% rate (CUMPRINC and CUMIPMT need a rate above zero), and the sheet has no input validation. The web page handles all three.
- `Home Loan Analysis`, cells `C41` and `C42`, hold text instead of values and break the text in row 48 (fix prompt given separately).
- Rent vs Buy and Expense Ratio Impact need a full re-derivation before conversion.
- Lower-priority workbook items: the Loan Prepayment sheet's yearly schedule is 30 rows while tenure goes to 40, and it has five lump-sum slots while the page accepts up to 20 (the page was checked against an independent simulator for more than five).
- Check the Section 196 link used in the emergency-fund article.

---

## Pages that are not tools or articles

- `about/` was rewritten on 12 October 2026. It describes the site as built by one independent person in India and does not publish the creator's name, experience or certifications. Keep it that way unless that is changed on purpose.
- `privacy-policy/` and `terms/` were updated on 12 October 2026 so that they describe what the site really does (third-party fonts and scripts, AdSense, the current list of tools, no regulated-adviser status). They are not legal advice. Have them reviewed by a qualified person before adding accounts, email capture, payments or referral links, and before relying on them for visitors outside India.

## Disclaimer

WealthCompare is an educational resource. It is not a SEBI-registered investment adviser, research analyst or distributor, and nothing on the site is personalised advice. Tax and regulatory rules change, so check current figures with the Income Tax Department, RBI, SEBI, your lender or a qualified professional before acting.