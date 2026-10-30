# WealthCompare

Free personal-finance calculators and short articles for Indian households, at [wealthcompare.in](https://wealthcompare.in).

The aim is simple. Show what a money decision does in **today's rupees** as well as future rupees, state every assumption in plain words, and keep the tools educational. Nothing here recommends a fund, stock, lender or broker.

Last updated: 30 October 2026.

---

## 1. Mission & Core Philosophy

Most Indian financial portals (banks, brokers, aggregators) design calculators as lead-generation funnels. Their projections show massive, multi-crore nominal sums while hiding inflation, commissions, and exit taxes.

WealthCompare operates on three principles:
1. **Purchasing Power Reality:** ₹1 crore 20 years from now will not buy what ₹1 crore buys today. Every tool and worked example calculates the real purchasing power in today's rupees using stated inflation assumptions.
2. **Radical Transparency:** Every variable (inflation, expected return, tax rate, tax exemption, selling cost, maintenance) is an editable input. What a tool leaves out is stated prominently in an "Advanced Read" section.
3. **No Commercial Conflicts:** Strictly educational. No demat account affiliate links, no sponsored loan recommendations, and no dark patterns.

---

## 2. Architecture & Technical Stack

- **Static Frontend:** Plain, semantic HTML5, CSS3, and vanilla JavaScript. No framework overhead (no React, Next.js, or build pipeline).
- **Fast Global Hosting:** Cloudflare Pages with automatic HTTPS and edge distribution.
- **Client-Side Autonomy:** All calculations, compound interest models, and amortization schedules run 100% inside the browser. No server-side calculation calls.
- **Zero Blocking Heavy Libraries:**
  - `Chart.js` (4.4.4 pinned) loaded via jsDelivr for responsive interactive canvas rendering.
  - `SheetJS` (`xlsx.full.min.js`) is **lazy-loaded on demand** only when a user clicks "Export to Excel" (saving ~500KB of blocking render time).
  - Resource hints (`<link rel="preconnect">`) enabled for Google Fonts and jsDelivr.
- **Viral Scenario Sharing:** Built-in `share-scenario.js` syncs form inputs with URL parameters in real time and provides a one-click clipboard copy (`?param=value`) so visitors can share exact calculations.
- **Offline Reference Workbook:** `WealthCompare Excel Calculator.xlsx` is strictly an offline mathematical baseline and developer reference. It is never deployed, linked, or served on the site, and is disallowed from search indexing via `robots.txt`.

---

## 3. Directory Layout

```
/
├── index.html                                 Homepage (hero, 8 calculators grid, 8 insights grid)
├── 404.html                                   Custom 404 page
├── ads.txt                                    Google AdSense publisher verification
├── robots.txt                                 Crawler instructions (disallows *.xlsx)
├── sitemap.xml                                Full sitemap with 25 validated URLs
├── site.webmanifest                           PWA web manifest
├── favicon.ico
├── build_footers.py                           Syncs standardized footer template across all pages
├── footer-template.html                       Footer base template with {{DISCLAIMER}} tag
├── WealthCompare Excel Calculator.xlsx        Offline mathematical model (not served publicly)
├── README.md                                  This comprehensive documentation
├── calculator-ui-notes.md                     Page patterns, tax rules, validation limits, UX notes
├── paid-features.txt                          Monetization status and roadmap notes
├── folder-tree.txt                            Directory tree backup
├── about/                                     About & Contact page
├── privacy-policy/                            DPDP Act 2023 & cookie compliance policy
├── terms/                                     Terms of Use & legal limitations
├── assets/
│   ├── logo.svg  og-image.png                 Branding and social share images
│   ├── css/site.css                           Shared CSS design tokens, .learn, .formula, .share-button
│   ├── icons/                                 Touch and favicon icons
│   └── js/                                    Shared JS:
│       ├── amount-words.js                    Indian numbering (lakh/crore) text under inputs
│       ├── export-excel.js                    On-demand lazy-loading client-side Excel exporter
│       ├── share-scenario.js                  URL query parameter sync and clipboard sharing
│       └── ad-slot-collapse.js                AdSense unfilled ad container collapse (prevents CLS)
├── insights/                                  10 Long-form Educational Articles:
│   ├── emergency-fund-before-investing/
│   ├── loan-vs-sip-hidden-tradeoffs/
│   ├── what-a-sip-return-assumption-means/
│   ├── reduce-emi-or-reduce-tenure-after-prepayment/
│   ├── how-an-emi-splits-between-interest-and-principal/
│   ├── prepay-loan-vs-invest/
│   ├── direct-vs-regular-mutual-fund-expense-ratio/
│   ├── rent-vs-buy-india-wealth-comparison/
│   ├── sustainable-swp-rate-india-retirement/
│   └── how-much-term-insurance-do-you-need/
└── tools/                                     11 Interactive Financial Calculators:
    ├── emi-calculator/
    ├── loan-prepayment/
    ├── sip-growth/
    ├── step-up-sip/
    ├── expense-ratio-impact/
    ├── prepay-vs-invest/
    ├── rent-vs-buy/
    ├── loan-vs-sip/
    ├── emergency-fund/
    ├── retirement-swp/
    └── term-insurance/
```

---

## 4. Current Suite: 11 Tools & 10 Articles

### A. The 11 Calculators

| Tool | Path | What It Answers | Status |
|---|---|---|---|
| **EMI Calculator** | `/tools/emi-calculator/` | Monthly EMI, total interest, and year-by-year principal vs. interest breakdown. | Live |
| **Loan Prepayment** | `/tools/loan-prepayment/` | How lump sums, monthly top-ups, or rate hikes affect tenure and interest saved. | Live |
| **SIP Growth** | `/tools/sip-growth/` | Long-term mutual fund SIP compounding, LTCG tax deduction, and real wealth in today's rupees. | Live |
| **Step-Up SIP Goal** | `/tools/step-up-sip/` | Solves for the starting SIP needed for a goal when increasing investment annually with salary hikes. | Live |
| **Expense Ratio Impact** | `/tools/expense-ratio-impact/` | Direct vs. Regular mutual fund compounding cost (shows how a 1% fee eats ₹20L+). | Live |
| **Prepay vs Invest** | `/tools/prepay-vs-invest/` | Prepaying home loan vs. investing surplus in mutual funds (hurdle rate, early debt-free date). | Live |
| **Rent vs Buy** | `/tools/rent-vs-buy/` | 20-year wealth: buying a flat vs. renting and investing down payment + surplus in equity SIP. | Live |
| **Loan vs SIP Matchup** | `/tools/loan-vs-sip/` | Buying a second property with a loan vs. investing the down payment and EMI in an equity SIP. | Live |

*All 8 tools feature: inline numeric validation, amount-in-words under currency fields, URL scenario sharing, client-side Excel export, interactive charts, and rich static educational (`.learn`) sections.*

### B. The 8 In-Depth Insight Articles

| Article | Path | Core Focus |
|---|---|---|
| **Emergency Fund Before Investing** | `/insights/emergency-fund-before-investing/` | How much cash to keep aside before starting a SIP; post-tax yields of savings, FDs, and liquid funds. |
| **Loan vs SIP: Hidden Trade-offs** | `/insights/loan-vs-sip-hidden-tradeoffs/` | 5 factors calculators miss: liquidity, divisibility, maintenance, tax rules, and emotional debt friction. |
| **What a SIP Return Assumption Means** | `/insights/what-a-sip-return-assumption-means/` | Expected return vs. guaranteed return, 1% sensitivity, and why sequence of returns matters. |
| **Reduce EMI or Reduce Tenure?** | `/insights/reduce-emi-or-reduce-tenure-after-prepayment/` | Why reducing tenure saves significantly more interest than reducing EMI, with worked examples. |
| **How an EMI Splits Over Time** | `/insights/how-an-emi-splits-between-interest-and-principal/` | Month-by-month analysis showing why early EMIs are 80%+ interest, and when the turning point occurs. |
| **Prepay Loan vs Invest: The Math** | `/insights/prepay-loan-vs-invest/` | Hurdle rate formula (`[Loan / (1-Tax)] + TER`), early debt freedom, and sequence risk. |
| **Direct vs Regular Mutual Funds** | `/insights/direct-vs-regular-mutual-fund-expense-ratio/` | Why a 1% fee costs ₹22L+ over 20 years, how fees are deducted from NAV, and tax-efficient switching. |
| **Rent vs Buy in India** | `/insights/rent-vs-buy-india-wealth-comparison/` | Why the 30x rule fails in Indian metros (~3% rental yields vs. 8.5% loans) and 20-year sensitivity. |

---

## 5. Mathematical & Regulatory Standards

Every calculation and published article follows strict verified benchmarks:

1. **Taxation on Equity Funds (Section 198, Income-tax Act, 2025):**
   - Long-Term Capital Gains (LTCG) on equity mutual fund units held >12 months: **12.5%** on gains exceeding **₹1,25,000** per financial year.
   - Short-Term Capital Gains (STCG) on units held ≤12 months: **20%** under Section 196.
2. **Property Capital Gains (Finance Act 2024 / Income-tax Act, 2025):**
   - 12.5% without indexation benefit for properties acquired after 23 July 2024.
3. **RBI Loan-to-Value (LTV) Limits:**
   - 90% for loans up to ₹30 lakh.
   - 80% for loans between ₹30 lakh and ₹75 lakh.
   - 75% for loans above ₹75 lakh.
4. **RBI Pre-payment Directions:**
   - Zero pre-payment penalties on floating-rate term loans to individual borrowers for non-business purposes.
5. **Real vs. Nominal Formula:**
   - `Value in Today's Rupees = Future Nominal Amount ÷ (1 + Inflation)^Years`
   - Ongoing monthly contributions brought to today's purchasing power using `ceil(month / 12)`.

---

## 6. Future Monetization Strategy

The owner decision is to keep the entire site free with **no mandatory user login, no credit card storage, and no intrusive popups**. The monetization plan follows a 3-stage roadmap:

### Stage 1: Display Advertising (Immediate Focus)
- **Primary Channel:** Google AdSense Auto Ads (configured with anchor and responsive in-page units).
- **Status:** Previous rejection for "Low value content" is now completely addressed by expanding to 8 in-depth, original articles (each 1,500–2,500 words with official citations) and adding static educational sections to all 8 calculators.
- **Action:** Request AdSense re-review in the Google AdSense dashboard.

### Stage 2: Micro-Transaction Utility (When Traffic Hits 5,000+ Monthly Visitors)
- **One-Click Comprehensive PDF Reports (₹99 - ₹149 via UPI / Razorpay):**
  - Instant client-side PDF generation (e.g. using `pdfmake` or `html2pdf`).
  - Generates a branded, multi-page personalized financial memo: amortization tables, visual charts, scenario comparisons, and tax breakdown.
  - No user accounts required; delivered via instant browser download upon UPI payment confirmation.

### Stage 3: Professional & B2B Licensing (Future)
- **Embeddable Financial Widgets for Independent Financial Advisors (IFAs) & CAs:**
  - Whitelabel iframe widgets or custom reports for fee-only financial planners and Chartered Accountants.
- **Dedicated Sponsor / Banner Placements:**
  - Direct fixed-fee monthly sponsorships from SEBI-registered fee-only investment advisors (RIA) or ethical fintech platforms (strictly screened for alignment with our educational mission).

---

## 7. Marketing & Traffic Acquisition Strategy

To build awareness and traffic without a paid ad budget, execute this playbook:

### 1. Organic Search & Programmatic SEO
- **Target High-Intent Indian Financial Queries:**
  - Search queries like *"loan prepayment vs sip calculator"*, *"rent vs buy calculator bangalore"*, *"direct vs regular mutual fund calculator"*, and *"how much interest saved by reducing tenure"*.
- **Submit to Google Search Console (GSC):**
  - Verify ownership via Cloudflare DNS or HTML tag.
  - Submit `https://wealthcompare.in/sitemap.xml` for immediate crawling.
- **Rich Snippets & Structured Data:**
  - Maintain `WebApplication` JSON-LD on all 8 tools and `Article` schema on all 8 articles to capture featured snippets.

### 2. High-Intent Community Seeding
- **Reddit (`r/IndiaInvestments`, `r/FIRE_India`, `r/developersIndia`):**
  - Write thoughtful, data-driven answers to user questions (e.g., *"I have a 10 lakh bonus, should I prepay my 8.5% home loan or put it in Nifty 50?"*).
  - Use our **Share Calculation** links (`?loan=...&rate=...`) to illustrate the math directly. Never spam; provide complete value in the comment and link to the tool as the source calculator.
- **X (Twitter) & LinkedIn:**
  - Post bite-sized visual charts showing counter-intuitive financial realities:
    - *"Why paying rent of ₹25k feels bad, but paying ₹45k in bank interest in Year 1 of a loan feels like an investment."*
    - *"How a 1% mutual fund commission quietly costs ₹22,00,000 over 20 years."*
  - Include the direct calculator link in the thread.

### 3. WhatsApp & Word-of-Mouth Virality
- The newly added **"Share calculation"** button enables users running real scenarios (e.g., buying a flat in Pune or comparing prepayments) to copy a clean link with all numbers prefilled and send it directly to their spouse, family, or financial planner.

---

## 8. Development & Maintenance Guidelines

### Deploying Changes
The site is hosted on Cloudflare Pages connected to this Git repository. Pushing to `main` triggers an automatic global build.

### Everyday Maintenance Commands
1. **Sync Footers:**
   Run after modifying `footer-template.html` or adding a new page:
   ```bash
   python build_footers.py
   ```
2. **Update Sitemap:**
   Ensure every new page is added to `sitemap.xml` with today's date in `YYYY-MM-DD` format.
3. **Verify Integrity:**
   Ensure all internal links use relative or canonical HTTPS URLs, and that no public page references `WealthCompare Excel Calculator.xlsx`.

---

## Disclaimer

WealthCompare is an educational resource. It is not a SEBI-registered investment adviser, research analyst, or distributor, and nothing on the site is personalised advice. Tax and regulatory rules change, so check current figures with the Income Tax Department, RBI, SEBI, your lender, or a qualified professional before acting.
