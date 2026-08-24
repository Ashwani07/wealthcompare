# Calculator UI Notes

## Excel Export

All calculators offer an `Export to Excel` action after the calculated output. Each workbook includes:

- `Inputs`: the values entered by the user and their units.
- `Results`: the calculated values shown in the result cards, including the selected time horizon.
- `Analysis`: the explanatory text shown beside or below the results.
- `Projection` on SIP Growth: the year-by-year invested, nominal, and inflation-adjusted values.

The export is generated in the browser using SheetJS. It reflects the input values at the time the export button is clicked; users should recalculate first when they have changed inputs.

## Calculator Presentation

- Loan vs SIP emphasizes the real-wealth comparison, with property and SIP summaries kept separate.
- Maintenance in Loan vs SIP can be entered as a percentage of property price or as annual rupees.
- LTCG in Loan vs SIP is shown as a 12.5% educational assumption on equity-SIP gains above the current ₹1,00,000 exemption. Tax rules and individual outcomes may differ.

## Amount guidance

Indian-rupee inputs show a live amount-in-words line below the field. This helps users confirm values such as `10000000` as **Rupees Ten Crore only**. The words are presentation-only; calculations continue to use the numeric input.

Applied to:

- Loan vs SIP: property price and loan amount
- EMI Calculator: loan amount
- SIP Growth: monthly SIP amount

## Result hierarchy

Each calculator should distinguish three levels:

1. **Final decision result**: the value a user came to understand, shown in a tinted result panel with larger type and a clear accent.
2. **Supporting calculations**: inputs, totals, tax, interest, gains, and other intermediate figures shown as compact metric rows.
3. **Explanation**: definitions, assumptions, and interpretation kept in a separate neutral panel.

The Loan vs SIP page gives the strongest emphasis to the real-wealth comparison, then presents Property Summary and SIP Summary as separate sections. EMI emphasizes Monthly EMI, and SIP Growth emphasizes inflation-adjusted value while keeping invested amount and gains secondary.

## Content rules

- Use Indian number grouping and plain-language labels.
- Keep assumptions beside the result they affect.
- Do not imply that projections are guaranteed.
- Keep future or unavailable features as non-interactive placeholders.
