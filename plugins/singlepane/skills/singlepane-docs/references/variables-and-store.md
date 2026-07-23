# Variable definitions & the document store (`sp_docs_store`)

The add-in persists everything as ONE JSON object saved via
`Office.context.document.settings` under the key `sp_docs_store`. When generating a
file offline, you author this object and embed it with
`scripts/graft_sp_store.py` (which handles the double-JSON-encoding and XML wiring —
never hand-edit the XML).

## Top-level shape (schemaVersion 1)

```json
{
  "schemaVersion": 1,
  "viewMode": "tags",
  "variables": [ /* VariableDef, see below */ ],
  "lastRefresh": "2026-07-01T00:00:00.000Z",
  "autoRefresh": true
}
```

- `viewMode`: `"tags"` (show tag text) or `"values"` (show rendered data). Generate
  with `"tags"` — the document you ship shows tags until the user refreshes.
- `autoRefresh: true` makes any variable/global edit re-render automatically.
- `lastRefresh` is optional metadata; set it to generation time or omit.

## Common fields (every variable)

| Field | Notes |
|---|---|
| `id` | UUID v4, stable across renames — generate one per variable |
| `name` | Display name used in tags. Unique case-insensitive; whitespace normalized. Natural names: `Total Revenue`, `Occ` |
| `kind` | `"global"` \| `"query"` \| `"computed"` |
| `description` | Optional free text shown in the pane |
| `defaultModifiers` | Optional array of `{ "name": "...", "args": [...] }` applied when a tag uses the variable with **no** pipe modifiers, e.g. `[{ "name": "percent", "args": [1] }]`. Tag-level modifiers replace (not stack with) the default |

## Global variables

```json
{ "id": "…", "name": "Month", "kind": "global", "valueType": "month", "value": "Jun" }
{ "id": "…", "name": "Year",  "kind": "global", "valueType": "year",  "value": 2026 }
{ "id": "…", "name": "Hotel Code", "kind": "global", "valueType": "text", "value": "ACD" }
```

`valueType`: `"month"` | `"year"` | `"number"` | `"text"` | `"date"`.

- **month**: store the canonical 3-letter form (`"Jun"`). The pane accepts long
  names/numbers from users, but generated stores should be canonical. When rendered
  in document text, a month global displays long ("June") by default; queries always
  receive the short form.
- **year**: 4-digit number (unquoted JSON number).
- **date**: `"YYYY-MM-DD"` string.

## Query variables

Each query parameter field is a **string** that may be a literal (`"Actual"`,
`"Total Revenue - 000"`), a global reference (`"{Year}"`), or a mix
(`"{Month}YTD"`, `"FY{Year}"`). References are resolved by variable name,
case-insensitive. Numbers interpolate as plain digits.

### financials — P&L / budget / forecast values

```json
{ "id": "…", "name": "Total Revenue", "kind": "query", "query": {
    "type": "financials",
    "codes": ["{Hotel Code}"],
    "usali": "Total Revenue - 000",
    "month": "{Month}",
    "year": "{Year}",
    "version": "Actual" } }
```

| Field | Valid values |
|---|---|
| `codes` | Array of property codes (each entry may be a literal or `{ref}`). One code → that property; several → the value is **aggregated (summed)** across them. For aggregated ratio-type lines (Occ %, ADR), aggregate the components in computed variables instead of aggregating the ratio line |
| `usali` | Exact line from the USALI reference, incl. the ` - NNN` suffix — pick from `references/layouts/` |
| `month` | `"Jan"`–`"Dec"` · `"Total Year"` · `"Q1"`–`"Q4"` · `"<Mon>YTD"` · `"<Mon>TTM"` · `"<Mon>BOY"` (month+suffix, no space) |
| `year` | 4-digit year (as string field content, e.g. `"{Year}"` or `"2026"`) |
| `version` | `"Actual"`, `"Budget"`, `"Budget1"`–`"Budget12"`, `"Forecast1"`–`"Forecast12"`, `"Proforma"`, `"LY_Actual"`, `"Var_Budget"`, `"Var_LY_Actual"`, plus company-specific names |

### str — STR / comp-set performance

```json
{ "id": "…", "name": "RGI", "kind": "query", "query": {
    "type": "str",
    "code": "{Hotel Code}",
    "date": "2026-06-30",
    "aggregateType": "month",
    "metric": "RGI",
    "subjectCompMarket": "Subject",
    "segment": "Total" } }
```

| Field | Valid values |
|---|---|
| `date` | `"YYYY-MM-DD"`. **Month-end date** for `month`/`yearToDate`/`running3Month`/`running12Month`; **a Saturday** for `currentWeek`/`running28Days`; the actual day for `day`/`monthToDate` |
| `aggregateType` | Case-sensitive: `day`, `month`, `monthToDate`, `currentWeek`, `running28Days`, `yearToDate`, `running3Month`, `running12Month` |
| `metric` | `Occ`, `ADR`, `RevPAR` · `% Chg` variants (`Occ % Chg`, …) · indexes `MPI`, `ARI`, `RGI` (+ `% Chg`) · ranks (`Occ Rank`, …, `RevPAR % Chg Rank`) |
| `subjectCompMarket` | `Subject`, `CS1`–`CS5`, `Market Scale` |
| `segment` | `Total`, `Group`, `Contract`, `Transient` |

There is no month-name→month-end interpolation — STR dates are literal. For a
monthly-refresh deck, keep the STR date as a `date`-type global the user updates,
or accept editing the variable monthly.

### otb — on-the-books / pace

```json
{ "id": "…", "name": "OTB Revenue", "kind": "query", "query": {
    "type": "otb",
    "code": "{Hotel Code}",
    "dailyOrMonthly": "monthly",
    "stayDate": "2026-08-01",
    "targetSet": "subject",
    "periodType": "ty",
    "metric": "revenue",
    "segment": "total",
    "asOfDate": "" } }
```

| Field | Valid values |
|---|---|
| `dailyOrMonthly` | `"daily"` or `"monthly"` |
| `stayDate` | `"YYYY-MM-DD"`; first of the month for `monthly` |
| `targetSet` | `"subject"` or `"cs"` |
| `periodType` | `"ty"` (this year) or `"ly"` (same time last year — pair ty/ly variables to show pace) |
| `metric` | `occ`, `rn`, `adr`, `revenue`, `revpar`, `as_of_date` |
| `segment` | `"total"`, `"group"`, `"transient"` |
| `asOfDate` | Snapshot date (nearest as-of not exceeding it), or `""` for latest |

### interest_rate — benchmark rates

```json
{ "id": "…", "name": "SOFR", "kind": "query", "query": {
    "type": "interest_rate", "benchmarkRate": "SOFR",
    "date": "2026-07-01", "asOfDate": "" } }
```

`benchmarkRate`: `"SOFR"` | `"SONIA"` | `"T10YR"`. Returned as a percent number
(5.33 = 5.33%). `asOfDate` `""` when unused.

## Computed variables

```json
{ "id": "…", "name": "GOP Var Pct", "kind": "computed",
  "expression": "([GOP] - [GOP Budget]) / [GOP Budget]",
  "defaultModifiers": [ { "name": "percent", "args": [1] } ] }
```

- `expression` uses the same grammar as tag expressions (see
  [tag-syntax.md](tag-syntax.md)): `+ - * /`, parentheses, numbers, variable
  references. May reference globals, queries, and other computed variables.
- Wrap multi-word names in `[brackets]` — unambiguous and future-proof.
- No cycles. Division by zero renders as an error — remember missing financials
  data comes back as 0, so a variance % against a zero base will error.
- KPI recipes (from the USALI layouts): Occupancy = `[Rooms Sold] / [Rooms Available]`
  (query vars on `Total Rooms Sold - 100` / `Total Rooms Available - 100`),
  ADR = `[Rooms Revenue] / [Rooms Occupied]`, RevPAR = `[Rooms Revenue] / [Rooms Available]`.

## Worked example — monthly snapshot store

```json
{
  "schemaVersion": 1,
  "viewMode": "tags",
  "autoRefresh": true,
  "variables": [
    { "id": "…", "name": "Hotel Code", "kind": "global", "valueType": "text",  "value": "ACD" },
    { "id": "…", "name": "Month",      "kind": "global", "valueType": "month", "value": "Jun" },
    { "id": "…", "name": "Year",       "kind": "global", "valueType": "year",  "value": 2026 },

    { "id": "…", "name": "Total Revenue", "kind": "query", "query": {
        "type": "financials", "codes": ["{Hotel Code}"], "usali": "Total Revenue - 000",
        "month": "{Month}", "year": "{Year}", "version": "Actual" },
      "defaultModifiers": [ { "name": "abbrev", "args": [1, "$"] } ] },
    { "id": "…", "name": "Revenue Budget", "kind": "query", "query": {
        "type": "financials", "codes": ["{Hotel Code}"], "usali": "Total Revenue - 000",
        "month": "{Month}", "year": "{Year}", "version": "Budget" },
      "defaultModifiers": [ { "name": "abbrev", "args": [1, "$"] } ] },

    { "id": "…", "name": "Rev Var", "kind": "computed",
      "expression": "[Total Revenue] - [Revenue Budget]" }
  ]
}
```

Slide text: `Revenue was <<Total Revenue>>, <<Rev Var | updown>>
<<Rev Var | abs | abbrev:1,$>> vs a budget of <<Revenue Budget>>.`

## Import Variables — handing definitions to a user without a donor

The task pane can ingest variable definitions directly: **Advanced → Import
Variables → paste JSON → Import**. Format notes for authoring import JSON:

- Accepts either a bare array of variable defs (`[{...}, {...}]`) or a full store
  object (`{"variables": [...]}`).
- `id`s are regenerated on import — omit them when authoring for import (they're
  only required when authoring a full store for the graft script).
- Everything else (query fields with `{Global}` references, `defaultModifiers`,
  computed `expression`s) imports as-is; the same validity rules as the rest of
  this document apply.
- Variables whose names already exist in the document are skipped, so re-importing
  an updated JSON only adds the new names — renaming is how you force a
  replacement, or the user deletes the old variable in the pane first.
- The pane's **Export Variables** button produces this same format, so users can
  also move variables between documents with it.

When generating a document without a donor, deliver this JSON alongside the file
and include the paste steps in the handoff — a JSON blob without instructions is
useless to the user.

## How it is persisted in the file (context, not a to-do)

The graft script writes the store as
`<we:property name="sp_docs_store" value="…"/>` inside
`ppt/webextensions/webextension1.xml` (PowerPoint) or
`word/webextensions/webextension1.xml` (Word), where the value is the store JSON
**double-JSON-encoded** (`json.dumps(json.dumps(store))`) then XML-escaped, plus
task-pane wiring (`taskpanes.xml` + rels), content-type overrides, the package-level
relationship, and `Office.AutoShowTaskpaneWithDocument = true`. The add-in reference
(`<we:reference/>`) is copied from the donor file — dev sideloads and the production
store add-in have different references, which is why a donor from the right
installation is required.
