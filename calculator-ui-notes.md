# Calculator UI Notes

Last updated: 12 October 2026. These notes describe how the tool pages are built and why. Read them before adding or changing a tool.

## Where each tool stands

| Tool | Page | State |
|---|---|---|
| Loan vs SIP | `/tools/loan-vs-sip/` | Reworked. Matches the workbook sheet `Home Loan Analysis` |
| SIP Growth | `/tools/sip-growth/` | Reworked. Matches `SIP Growth` |
| Loan Prepayment | `/tools/loan-prepayment/` | Built to the current pattern. Matches `Loan Prepayment` |
| Step-Up SIP Goal | `/tools/step-up-sip/` | Built to the current pattern. Matches `Step-Up SIP Goal` |
| EMI Calculator | `/tools/emi-calculator/` | Reworked on 12 October 2026. Matches `EMI Calculator`. All five tools now follow the same pattern |

Sections below say which tools they apply to.

## The page pattern (every reworked tool)

1. **Inputs card** with grouped fields and an inline error under each field.
2. **Verdict card first.** One headline answer in plain words, a one-line summary, three to five supporting lines, and a "Worth knowing" box for anything that could mislead (for example a return below inflation, or a loan above the RBI limit). The verdict is the thing the visitor came for.
3. **Collapsed "full breakdown"** (`<details class="breakdown-details">`). It holds every figure, the "what if" tables, and a nested **Advanced Read** with the maths, tax treatment and what is left out. The content is in the page, just folded.
4. **Chart**, with the year-by-year table folded under it where the tool has one.
5. **Export to Excel**, next to the main button.
6. **Real/Nominal choice where it matters.** EMI Calculator and Loan Prepayment have none: they model a loan at a fixed rate in actual rupees and say so on the page. SIP Growth and Step-Up SIP Goal have a "Today's rupees / Future rupees" toggle beside the verdict. Loan vs SIP has the toggle on its chart (the verdict is in real terms by design, as the workbook decides). Loan Prepayment has none, because the workbook model has no inflation input and says so on the page.

Do not put the verdict below the inputs-and-chart or under a fold. Do not repeat the same number in three places.

## Single source of truth

The workbook `WealthCompare Excel Calculator.xlsx` holds the model. The page must give the same numbers as its sheet. Shared assumptions (inflation, return, tax rate and exemption, loan rate, property sale tax, selling cost, LTV bands) live on the **Common Assumptions** sheet. If page and sheet disagree, decide which is right, fix the workbook first, then the page.

Every page exposes its last result for testing (`window.lastResults`, `lastSip`, `lastPlan`, `lastData`) and keeps the pure calculation in plain functions (`simulate`, `computeSIP`, `solvePlan`, `computeLoanVsSip`, and the EMI functions), separate from rendering. On-screen results and the Excel export both read from the same functions, so they cannot drift apart.

## Excel export

Every tool offers `Export to Excel` after the result. The workbook is built in the browser with SheetJS, pinned to `xlsx@0.18.5` (do not use an unpinned `@latest` URL). It reflects the inputs at the moment the button is clicked. Sheets by tool:

- Loan vs SIP: `Inputs`, `Results`
- SIP Growth: `Inputs`, `Results`, `Projection`
- Step-Up SIP Goal: `Inputs`, `Results`, `Projection`
- Loan Prepayment: `Inputs`, `Scenarios`, `Schedule` (for the scenario chosen on the page)
- EMI Calculator: `Inputs`, `Results`, `Analysis`, `Amortization`

Export re-reads and re-validates the inputs. It never exports from stale or invalid values.

## Real vs nominal methodology

These rules apply to every tool. Keep real and nominal consistent on both sides of every comparison, including cost basis.

- A future amount is divided by (1 + inflation)^years.
- Money paid in over time is brought back to today's rupees before it is compared with a final amount. Each year's twelve instalments are divided by (1 + inflation) for that year (the `ceil(month / 12)` convention). Never subtract a plain nominal total from a real terminal value.
- A payment made today (a down payment, a lump sum at the start) is not discounted.
- Closed form for twelve payments a year: the discount factor sum is (1 − (1 + i)^−n) ÷ i, or n when inflation is 0.

### Loan vs SIP

- **Property path.** Sale price after growth, then selling cost, then tax on the gain above the price paid, then the result brought to today's rupees. From that, subtract the down payment, the EMIs and the upkeep, all in today's rupees. Upkeep stays at the first year's rupee amount.
- **SIP path.** The down payment as a lump sum on day one plus a monthly SIP equal to the EMI. Both grow monthly at the yearly return divided by 12. Tax is worked out once at the end.
- **Same cash, both sides.** The down payment feeds the SIP side directly. Any change to the down payment logic must update both sides together.
- The verdict is the difference in real gain. It assumes the visitor already owns a home to live in. It is not a rent-vs-buy comparison for a first home, and the page says so.
- Maintenance can be entered as a percentage of price or as annual rupees.
- The loan field shows the loan-to-value ratio and warns when it is above the RBI limit for that loan size (90% up to ₹30 lakh, 80% up to ₹75 lakh, 75% above). It warns, it does not block.

## Tax rules used in the tools

- **SIP / equity fund gains:** 12.5% on the gain above ₹1,25,000, applied once, at redemption (Section 198 of the Income-tax Act, 2025; Section 112A of the 1961 Act). Used on Loan vs SIP, SIP Growth and Step-Up SIP Goal, so they agree for the same investment. All gains are treated as long-term. Units held 12 months or less would be taxed at 20% (Section 196), so very short plans are understated. The pages say this and show a note when the period is one year.
- **Property sale gain** (Loan vs SIP): an input, default 12.5%, which is the long-term rate without indexation. Reinvestment exemptions, cess, surcharge and the holding period are not modelled.
- Cess, surcharge, exit loads and fund running costs are not included anywhere.
- Never show a tax figure that has not been checked on an official source. See the README for the list of what has been verified.

### Tax timing (SIP Growth and Step-Up)

Tax is triggered by a sale. The main result applies it once, at the end. Year-by-year tables show before-tax values as they grow, and a separate "after tax if sold at the end of that year" column, clearly labelled as a hypothetical. Do not plot tax as if it were charged each year.

## Input validation

Every calculator validates before calculating or exporting. An error appears under the field that is wrong (`.field-error` inside `.input-group`, with `has-error` toggled), never as `NaN` or `Infinity`. Typing in a field clears that field's error. Whole numbers are required where the model needs them.

| Field | Limit |
|---|---|
| Tenure, EMI Calculator, Loan vs SIP, SIP Growth, Loan Prepayment | whole years, 1 to 40 |
| Years to goal, Step-Up SIP Goal | whole years, 1 to 30 |
| Loan interest, EMI Calculator and Loan vs SIP | 0% to 50% |
| Loan interest and new rate, Loan Prepayment | 0% to 30% |
| SIP return, inflation, step-up | 0% to 30% |
| Property growth | -10% to 30% |
| Property sale tax | 0% to 50% |
| Selling cost | 0% to 20% |
| Months, Loan Prepayment | whole months, 1 to 480 (lump-sum months 0 to 480) |
| Lump-sum rows, Loan Prepayment | 1 to 20 rows. Start with three example rows; a + button adds a row and a − button on each row removes it (the last row is cleared, not deleted) |
| Amounts | greater than zero for the main amount, 0 or more for optional ones |
| Loan vs SIP | loan cannot exceed the property price |

## Amount guidance

Rupee inputs show a live amount-in-words line below the field (`bindAmountInWords(inputId, wordsId)` from `assets/js/amount-words.js`). It is presentation only; the calculation always uses the number. Every call is wrapped in `if (typeof bindAmountInWords === "function")`, so if `amount-words.js` fails to load (for example when a page is opened straight from disk, where the root-relative `/assets/...` path does not resolve) the calculator still works and only the words line is missing. `numberToIndianWords()` returns the words plus a trailing "Only"; the caller adds "Rupees " itself, so do not add it twice.

Applied to: Loan vs SIP (property price, loan), EMI (loan), SIP Growth (monthly SIP, lump sum), Step-Up (goal cost, amount already invested), Loan Prepayment (loan, monthly extra, each lump sum).

## Result hierarchy

Distinguish three levels on every tool:

1. **The decision:** the verdict card, and inside the breakdown a tinted result panel (`.final-result`) with a larger figure. It switches to the negative treatment (`.is-negative`) when the number is negative. It must never stay green when the outcome is a loss.
2. **Supporting figures:** compact metric rows (`.metric`).
3. **Explanation:** assumptions and limits, in the Advanced Read and in short notes beside the figure they affect.

## Colour system

Text, surface and accent colours come from the CSS custom properties defined once in `/assets/css/site.css` (`--text-primary`, `--text-secondary`, `--text-muted`, `--surface-muted`, `--border-subtle`, `--bg-grad-*`, `--positive*`, `--negative*`, brand tokens). Do not hardcode a new grey or accent in a page's `<style>`. Add a token to `site.css`, so a palette change happens in one place. `--text-muted` targets at least 7:1 contrast on white. Bump the `?v=` on the stylesheet link in every page when `site.css` changes.

## Ads

- The AdSense **Auto Ads** script is in the head of every page. All five tool pages and the articles contain **no manual ad units**.
- Only the homepage still has manual units with placeholder slot IDs (`300000001` to `300000003`). Replace them with real IDs or remove them. Do not invent slot IDs.
- `.ad-slot` reserves `min-height: 100px` to avoid layout shift, and `assets/js/ad-slot-collapse.js` collapses a slot that comes back unfilled or never resolves within 4 seconds. Use that class for any manual unit you add later. Never fall back to a bare `<div style="margin:20px 0;">`.
- `ads.txt` must contain exactly: `google.com, pub-4357149194740826, DIRECT, f08c47fec0942fa0`.
- Do not show "coming soon" or "planned" tiles or article cards for things that do not exist. They make a site look unfinished to AdSense reviewers and to visitors. Add a tile when the page is live.

## EMI Calculator

`computeEMI()` gives the EMI (P / n at 0%), `computeMonthly()` runs the month-by-month schedule, and `computeYearly()` groups it into yearly principal, interest and balance rows. The verdict also reports the month when principal first exceeds interest and the month when half the loan is repaid. A chart of stacked yearly bars shows interest against principal, and two small tables show the EMI and total interest for a tenure of five years more or less and a rate of one point more or less. The schedule is a free feature, not gated. Verified: yearly principal sums to the loan amount, yearly interest sums to total interest, and the balance reaches zero at term. The page also holds a short block of static explanation (the formula, a worked example, fixed versus floating rates, what is left out, common questions). Its worked-example numbers are written into the HTML, so if the default inputs change, recompute them.

## Loan Prepayment engine

Lump sums are added by month, so two rows with the same month simply add up. The page accepts up to 20 lump-sum rows; the workbook sheet has five slots (see the README), and the maths is the same.

`simulate(kind, inputs)` runs one month-by-month schedule per scenario (normal, lump sums, monthly extra, rate change, combination) for up to 480 months. It follows the workbook's `Prepayment Engine` formula for formula. Prepayments are capped at the balance. "Reduce EMI" recalculates the EMI for the months left on the original schedule after any month with a prepayment. In the rate-change month under "Keep EMI, change tenure", a prepayment from the month before still reduces the EMI first, at the old rate. If a rate rise leaves the EMI below the monthly interest, the page says the loan is not repaid within 40 years.

## Chart sizing

Charts use a `.chart-canvas-wrap` with an explicit height (300px on mobile, 380px from 640px wide) and `maintainAspectRatio: false`. Keep legend labels short and put the full name in the tooltip. Cap the x-axis ticks (`maxTicksLimit: 6`, `maxRotation: 0`) so labels do not rotate on long tenures.

## Link styling

`.site-header a` and `.footer-links a` are forced to `text-decoration: none` in `site.css`, with higher specificity than any page-level `a {}` rule. Do not rely on a page getting its own reset right. The legal pages underline body links on purpose; the component rule keeps that out of the header and footer.

## Footer

The footer comes from `footer-template.html` and is copied into every page by `python3 build_footers.py`. Each page's own disclaimer sits in the script's `PAGES` list. Add every new page to that list and run the script before deploying.

## Content rules

- Indian number grouping and plain labels. Currency as whole rupees (`Math.round(x).toLocaleString('en-IN')`), no paise.
- Headlines may use "lakh" and "crore" with two decimals (`₹1.79 crore`) so they read easily. Detailed figures use full grouping.
- Keep assumptions beside the result they affect. Label every rate and return as an assumption, not a forecast.
- Never imply a projection is guaranteed. Never recommend a fund, stock, lender or product.
- Write in simple language and short sentences. No em dashes. Put complexity in the Advanced Read.
- Every page needs one H1, a unique title and meta description, Open Graph and Twitter tags, and a `WebApplication` JSON-LD block (articles use `Article`).