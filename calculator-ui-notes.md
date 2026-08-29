# Calculator UI Notes

## Excel Export

All calculators offer an `Export to Excel` action after the calculated output. Each workbook includes:

- `Inputs`: the values entered by the user and their units.
- `Results`: the calculated values shown in the result cards, including the selected time horizon.
- `Analysis`: the explanatory text shown beside or below the results.
- `Projection` on SIP Growth: year-by-year invested, nominal, and inflation-adjusted (pre-tax) values — no per-row tax column, see "Tax timing" below.
- `Amortization` on EMI Calculator: year-by-year principal paid, interest paid, and remaining balance.

The export is generated in the browser using SheetJS (pinned to `xlsx@0.18.5` via CDN — do not switch back to an unpinned `@latest`-style URL). It reflects the input values at the time the export button is clicked; users should recalculate first when they have changed inputs. On-screen results and the export both read from the same calculation functions per page (`computeEMI`/`computeAmortizationSchedule`, `computeLoanVsSip`, `computeSIPSeries`/`computeSIPFinal`), so they cannot drift out of sync with each other.

## Calculator Presentation

- Loan vs SIP emphasizes the real-wealth comparison, with property and SIP summaries kept separate.
- Maintenance in Loan vs SIP can be entered as a percentage of property price or as annual rupees.
- LTCG is modeled at **12.5% on equity-SIP gains above the current ₹1,25,000 annual exemption**, applied once at redemption. This applies on **both** Loan vs SIP and SIP Growth now, so the two tools report consistent after-tax numbers for the same investment — previously only Loan vs SIP taxed the SIP leg, which made the two pages disagree. Tax rules and individual outcomes may differ from this simplification.

## Real vs nominal methodology (Loan vs SIP)

Interest and maintenance are nominal cash outflows paid at different points over the loan tenure. They are amortized year by year and each year's outflow is discounted back to today's rupees *before* being netted against the inflation-adjusted (real) future property value. Do not subtract nominal cost totals directly from a real terminal value elsewhere in the app — that mismatches units and understates the true cost of financing.

## Down payment treatment (Loan vs SIP)

The property buyer's down payment is real cash committed on day one. To keep the comparison fair, the SIP scenario invests the same amount as a lump sum on day one, in addition to the monthly SIP equal to the EMI. The "Down payment" metric shown in the Property Summary is not just informational — it feeds directly into the SIP-side future value calculation. Any future change to the down payment logic must update both sides together.

## Input validation

Every calculator validates inputs before calculating or exporting, and shows an inline error message rather than rendering `NaN`/`Infinity`:

- Amounts must be greater than zero.
- Tenure: 1–40 years.
- Interest / return rates: 0–50% (loan interest), 0–30% (SIP return, inflation).
- Property appreciation: -10% to 30%.
- Loan vs SIP: loan amount cannot exceed property price.

## Amount guidance

Indian-rupee inputs show a live amount-in-words line below the field. This helps users confirm values such as `10000000` as **Rupees One Crore Only**. The words are presentation-only; calculations continue to use the numeric input. `numberToIndianWords()` returns the words plus a trailing "Only" (not "rupees only") — the caller prefixes "Rupees " itself. Do not prefix a second "Rupees" or the output duplicates the unit word.

Applied to:

- Loan vs SIP: property price and loan amount
- EMI Calculator: loan amount
- SIP Growth: monthly SIP amount

## Result hierarchy

Each calculator should distinguish three levels:

1. **Final decision result**: the value a user came to understand, shown in a tinted result panel with larger type and a clear accent. This panel switches to a red/negative treatment (`.is-negative`) when the underlying number is negative, instead of staying green regardless of outcome.
2. **Supporting calculations**: inputs, totals, tax, interest, gains, and other intermediate figures shown as compact metric rows.
3. **Explanation**: definitions, assumptions, and interpretation kept in a separate neutral panel.

The Loan vs SIP page gives the strongest emphasis to the real-wealth comparison, then presents Property Summary and SIP Summary as separate sections. EMI emphasizes Monthly EMI, and SIP Growth emphasizes inflation-adjusted, after-tax value while keeping invested amount and gains secondary.

## Color system

All pages pull text, surface, and accent colors from CSS custom properties defined once in `/assets/css/site.css` (`--text-primary`, `--text-secondary`, `--text-muted`, `--surface-muted`, `--border-subtle`, `--bg-grad-*`, `--positive*`, `--negative*`). Don't hardcode a new gray or accent hex value in a page's local `<style>` block — add a token to `site.css` instead, so a future palette change only happens in one place. `--text-muted` targets ≥7:1 contrast against white (WCAG AAA) rather than the old ~4.6–4.8:1 grays that were only just clearing AA.

## Ad placement

Every ad container uses the `.ad-slot` class, which reserves `min-height: 100px` before the ad loads, to avoid layout shift (Cumulative Layout Shift) once real AdSense units are wired in. Don't drop back to a bare `<div style="margin:20px 0;">` wrapper.

`assets/js/ad-slot-collapse.js` (included on every page with ad slots) watches each `<ins class="adsbygoogle">` for AdSense's `data-ad-status` attribute and collapses the wrapping `.ad-slot` to zero height if the slot comes back `"unfilled"`, or never resolves within 4 seconds (script blocked, no AdSense account yet, dev server). This is why ad slots look invisible pre-launch instead of sitting as dead empty rectangles — it's automatic and requires no per-page code. Once AdSense is approved and slots are actually filled, this becomes a no-op and the reserved space behaves exactly as before.

## Tax timing (SIP Growth)

LTCG tax is only triggered by an actual sale — it is **never** shown per-row in the year-by-year table or plotted per-year in the chart, because that would imply annual taxation, which isn't how it works. `computeSIPSeries()` returns pre-tax nominal and pre-tax real (inflation-adjusted) values for every year — inflation genuinely erodes value continuously regardless of whether you've sold, so that part is legitimate to show annually. `computeSIPFinal()` applies tax exactly once, to the final year only, and its output (`tax`, `afterTax`, `realAfterTax`) is used solely in the SIP Summary block. If a future change needs tax visible earlier than the final year (e.g. a "what if you exited in year N" feature), build it as a clearly-labeled separate hypothetical — don't fold it back into the main per-year table.

## Amortization schedule (EMI Calculator)

`computeAmortizationSchedule()` runs a full month-by-month amortization (same pattern as Loan vs SIP's internal interest calculation) and aggregates it to yearly principal/interest/balance rows. This is a free feature, not gated — every competitor's EMI calculator shows this, so withholding it would make the free tier look thinner than the competition, not premium. Verified that yearly principal sums to the loan amount, yearly interest sums to total interest, and balance reaches exactly zero at term.

## Chart sizing

Chart.js's default 2:1 aspect ratio (`maintainAspectRatio: true`, the default) renders too short on mobile. Both charts (Loan vs SIP, SIP Growth) use a `.chart-canvas-wrap` div with an explicit CSS height (300px mobile, 380px at ≥640px) and `maintainAspectRatio: false` in the Chart.js options, so the canvas fills that height instead of deriving it from width. Legend labels are kept short (e.g. "Property Value", not "Property Value (Nominal)") with the full descriptive name moved to the tooltip via a `fullLabel` property on each dataset — long legend labels were wrapping to two lines and eating vertical space that should go to the plot. X-axis ticks are capped (`maxTicksLimit: 6`, `maxRotation: 0`) so labels don't rotate diagonally and consume extra height, especially at longer tenures (30–40 years).

## Link styling

`.site-header a` and `.footer-links a` are forced to `text-decoration: none` in the shared `site.css`, deliberately more specific than any page-level `a{}` rule (bare `a` selectors have lower specificity and lose regardless of source order). This exists because two pages (EMI Calculator, Loan vs SIP) had no page-level underline reset at all, and the legal pages (About/Privacy/Terms) intentionally underline body-text links but were letting that bleed into their footer links too. Any new page must not rely on getting its own `a{}` reset right — the component-scoped rule in `site.css` is the actual guarantee.

## Content rules

- Use Indian number grouping and plain-language labels. Currency values are formatted as whole rupees (`Math.round(x).toLocaleString('en-IN')`) — no paise-level decimals, which previously rendered inconsistently (e.g. ₹1,23,456.7 vs ₹1,23,456.70).
- Keep assumptions beside the result they affect.
- Do not imply that projections are guaranteed.
- Keep future or unavailable features as non-interactive placeholders.
