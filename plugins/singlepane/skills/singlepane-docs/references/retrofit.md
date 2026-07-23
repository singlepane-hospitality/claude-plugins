# Retrofitting an existing deck or document onto tags

Goal: take a deck or document the user already produces by hand — numbers typed into
prose, KPI callouts, and tables each month — and make it refreshable by replacing the
hardcoded data with `<<tags>>` backed by a well-designed variable set, while leaving
the layout, styling, and narrative structure intact.

## Step 0 — Work on a copy, always

Never retrofit the original file in place. Copy it first (e.g.
`Board Deck (Singlepane).pptx`) and edit only the copy — the untouched original is the
validation baseline in Step 6.

## Step 1 — Inventory the hardcoded data

Walk every slide / page and list each place data appears:

- **Numbers in prose** ("Total revenue was $1.24M, $63K ahead of budget")
- **KPI callouts** (big-number shapes: Occ, ADR, RevPAR, GOP)
- **Tables** (variance tables, portfolio grids, pace tables)
- **Period labels** — titles and headings like "June 2026 Performance" are data too:
  the month/year words should become `<<Month>> <<Year>>` so the narrative refreshes
  along with the numbers, not just the figures
- **Direction words** tied to numbers ("up", "ahead of", "▲") — candidates for the
  `updown` modifier on a computed variance

Mark what *cannot* be retrofit, and tell the user explicitly rather than silently
skipping it:

- **Charts/graphs** — the add-in only fills text; charts stay static (offer the
  attached-Excel-workbook route from the Excel skill, or a monthly manual update)
- Tags can't live in speaker notes, SmartArt, WordArt, chart elements, or (Word)
  headers/footers/footnotes/floating text boxes — numbers there stay manual
- Numbers Singlepane doesn't hold (cap rates, deal terms, hand-written commentary
  figures) — these remain the user's manual inputs

## Step 2 — Recover each number's inputs

For every inventoried number, work out what query would produce it: property/ies,
period (month/aggregate), year, version (Actual/Budget/Forecast), and account or
metric. Read the evidence around the number — table headers and row labels, slide
titles, footnotes ("as of 6/30"), the column a figure sits in — and ask the user
about anything ambiguous (is "GOP margin" against total revenue? which forecast is
"the reforecast"?). Then map to a query type:

| The number is… | Query type |
|---|---|
| A P&L / budget / forecast value | `financials` (multiple codes aggregate by summing) |
| STR / comp-set performance or index | `str` |
| On-the-books / pace | `otb` |
| A benchmark rate | `interest_rate` |
| A ratio, variance, or per-key figure | `computed` over the query variables above |

Record the mapping (a scratch table of *location → variable name → query params*) —
the retrofit is only as correct as this mapping. USALI strings are exact-match:
pick them from `layouts/` via [usali-layouts.md](usali-layouts.md), and use `- 000`
top-line accounts rather than summing departments.

## Step 3 — Design the variable set: consolidate into globals first

This is the payoff step. Before defining any query variable, look across the whole
mapping for parameters that repeat:

- **Shared by (nearly) everything** → a global: `Hotel Code`, `Month`, `Year`, and
  often `Version` for a reforecast the whole document reads. Query fields reference
  them (`"{Month}"`, `"{Hotel Code}"`) — never repeat the literal. The test: *next
  month, how many things must the user edit before clicking refresh?* The right
  answer is usually one or two globals.
- **Derived periods** stay derived: YTD columns use `"{Month}YTD"`, not a second
  month global that can drift out of sync.
- **STR dates can't interpolate from `Month`** — give them their own `date`-type
  global (e.g. `STR Month End`) so they're still a one-touch monthly edit.
- **Repeated math** → computed variables (`Rev Var`, `GOP Var Pct`), never in-tag
  arithmetic copied across slides.
- Genuinely one-off parameters may stay literal in the query definition — a global
  used once adds noise, not re-pointability. Exception: keep `Hotel Code` a global
  even if used once, since re-pointing the document is the whole point.

Name variables systematically off the existing labels (`Rooms Rev`, `Rooms Rev
Budget`, `Rooms Rev Var`) and set `defaultModifiers` to match how each number is
formatted on the page today (see Step 4).

## Step 4 — Replace the text with tags

- Replace each number **in place** so the tag inherits the original run's font,
  size, and color — don't delete the shape/cell and retype.
- Reproduce the original rendering with modifiers (or `defaultModifiers`): `$1.2M` →
  `abbrev:1,$`; `62.4%` → `percent:1`; "up $63K" → `<<Rev Var | updown>>
  <<Rev Var | abs | abbrev:1,$>>`.
- Replace period words in titles and prose with `<<Month>>` / `<<Year>>` tags
  (`| monthshort` where the page showed "Jun").
- Keep each tag whole within one text frame / table cell.
- Working programmatically (python-pptx / python-docx) is generally safe for
  in-place text edits — but a number split across formatting runs must be rejoined
  carefully so the surrounding styling survives; spot-check a slide before doing all
  of them.

## Step 5 — Define the variables

Two routes, per the main skill's "Two ways to work":

1. **User has the add-in open (or will)**: ship the copy with tags only and give the
   user the variable definitions to enter in the pane — or let the pane's scan
   propose the tag names and fill in the query parameters with them.
2. **Fully offline**: author the `sp_docs_store` JSON
   ([variables-and-store.md](variables-and-store.md)) and run `graft_sp_store.py`.
   Note the donor requirement: an existing deck that has never been saved with the
   add-in loaded **cannot act as its own donor** — if no donor is available, use
   route 1.

## Step 6 — Validate against the original, then hand off

After the user opens the copy, signs in, and refreshes:

1. Compare the refreshed values side-by-side with the original — every number the
   retrofit replaced should match (up to the rounding the modifiers apply).
2. Investigate every discrepancy rather than assuming it's fine: usual causes are a
   wrong USALI mapping, wrong version (Actual vs a reforecast), wrong period
   (month vs YTD), an aggregation mismatch on multi-property numbers — or the
   original deck simply being stale relative to the platform. Stale-original is a
   *finding to report to the user*, not an error to silence.
3. Confirm the monthly workflow with the user end-to-end: which globals they touch
   (typically `Month`, maybe `Year` and an STR date), then refresh — and which
   items remain manual (charts, non-Singlepane numbers) so nothing silently stops
   being updated.
