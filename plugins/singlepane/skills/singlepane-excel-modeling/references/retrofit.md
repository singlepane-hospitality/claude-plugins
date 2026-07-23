# Retrofitting an existing workbook onto SP.* formulas

Goal: take a model or report the user already has — fed by pasted data tabs, hardcoded
numbers, or links to other workbooks — and make it live on Singlepane by replacing the
*data entry points* with SP.* formulas, while leaving the model's own logic and layout
intact.

## Step 0 — Work on a copy, always

Never retrofit the original file in place. Save a copy first (e.g.
`Q3 Model (Singlepane).xlsx`) and do all editing in the copy:

- In Excel: **Save As** before touching anything.
- Programmatically: copy the file (`shutil.copy`) and open only the copy.

The original is the validation baseline in Step 6 — you need it untouched.

## Step 1 — Survey where data enters the workbook

Inventory every way numbers get *into* the model:

| Source pattern | How to spot it |
|---|---|
| Hardcoded actuals | Grids of numeric literals shaped like months × accounts or properties × metrics |
| Lookups against pasted data tabs | `VLOOKUP` / `XLOOKUP` / `INDEX`+`MATCH` / `SUMIF(S)` / `GETPIVOTDATA` pointing at tabs that hold exported/pasted data |
| External workbook links | Formulas containing `[OtherBook.xlsx]` |
| Pivot tables | Built on pasted export ranges |

Distinguish **source cells** (data enters the workbook) from **derived cells** (Excel
math over other cells — subtotals, variances, ratios, per-key math). Only source cells
get replaced; derived cells are the model's logic and must be preserved.

Also distinguish **data** from **assumptions**: period P&L / STR / pace values are data
and get replaced; user-owned inputs (growth rates, cap rates, staffing assumptions,
underwriting toggles) stay manual. When a tab's role is unclear, ask the user which
tabs are data dumps and which hold their assumptions — don't guess.

## Step 2 — Map each source to its replacement

| The number is… | Replace with |
|---|---|
| A P&L value for one property/period/version | `SP.FINANCIALS` |
| A P&L value summed across properties | `SP.FINANCIALS_AGG` (over a `SP.FILTER` spill if the set is rule-based) |
| STR / comp-set performance or index | `SP.STR` |
| On-the-books / pace | `SP.OTB` |
| A benchmark rate (SOFR, SONIA, T10YR) | `SP.GET_INTEREST_RATE` |
| A hotel attribute (room count, brand, market…) | `XLOOKUP` against the "My Properties" sheet |

Anything that doesn't map to one of these (e.g. company data Singlepane doesn't hold)
stays as-is — tell the user which cells remain manual and why.

## Step 3 — Map the model's row labels to USALI lines

Existing row labels rarely match USALI strings exactly — the model may say "Rooms
Revenue" where the exact-match string is `"Rooms Revenue - ..."`, or "Total Revenue"
where the user's chart of accounts splits things differently. Use the "Usali Reference"
sheet and the layout files under `layouts/` to build the mapping, and confirm ambiguous
lines with the user (does their "Other Income" include misc income? is "GOP" before or
after fees?). The retrofit is only as correct as this mapping — write it down (a hidden
mapping column next to the row labels works well, and doubles as the USALI input cells
the formulas reference).

## Step 4 — Hoist parameters into input cells

A retrofit is the moment to fix hardcoded parameters. Per the main skill's layout rule:
property codes, year, month, version, and as-of dates move into labeled input cells the
new formulas reference — not literals repeated inside formulas. If the old model had
"2025" baked into 300 cells, the retrofit should leave it in exactly one.

## Step 5 — Replace the source cells

- Prefer one grid formula referencing row/column driver cells
  (`=SP.FINANCIALS($B$1,$A6,C$4,$B$2,$B$3)`) over hundreds of bespoke formulas.
- Preserve number formats, layout, and every derived row untouched.
- **Leave the old data tabs and pasted values in place for now** — they're needed for
  validation.

## Step 6 — Validate against the original, then clean up

After the user opens the copy, signs in, and recalculates:

1. Compare the retrofit's values against the original workbook's values — a temporary
   check sheet of differences, or side-by-side spot checks on totals and a sample of
   line items.
2. Investigate every discrepancy rather than assuming it's fine: usual causes are a
   wrong USALI mapping, an aggregation mismatch (e.g. the old model summed different
   properties), a version mismatch (Actual vs a reforecast), or the original simply
   being stale relative to the platform. Stale-original is a *finding to report*, not
   an error to silence.
3. Only after the user accepts the comparison: delete or hide the now-unused data
   tabs, and break any external workbook links.

## Programmatic (openpyxl) cautions

- Everything in the main skill's "Building workbooks programmatically" section applies —
  above all, run `scripts/fix_sp_formulas.py` on the saved copy or every replaced cell
  shows `#NAME?`.
- **openpyxl silently drops charts, pivot tables, slicers, and images when re-saving a
  workbook it opened.** Before editing an existing file programmatically, check for
  these; if present, either do the retrofit inside Excel instead (with the user, or via
  Claude for Excel) or warn the user exactly what will be lost. `.xlsm` files need
  `keep_vba=True` or macros are stripped.
- Do a read-only pass (`load_workbook(path, read_only=True)`) to survey (Steps 1–3)
  before opening for editing.
