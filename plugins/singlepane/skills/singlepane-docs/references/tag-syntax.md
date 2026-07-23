# Tag syntax & format modifiers

A tag is `<<` expression ( `|` modifier )* `>>` placed as literal text in a slide
shape / table cell (PowerPoint) or body paragraph / table cell (Word).

```
<<Total Revenue>>
<<Total Revenue | abbrev:1,$>>
<<([GOP] - [GOP Budget]) / [GOP Budget] | percent:1>>
<<Month | monthlong>> <<Year>>
```

## Expression grammar

```
tag            := expr ("|" modifier)*
expr           := additive
additive       := multiplicative (("+" | "-") multiplicative)*
multiplicative := unary (("*" | "/") unary)*
unary          := "-"? primary
primary        := number | varref | "(" expr ")"
varref         := bare multi-word name | [Bracketed Name]
modifier       := name (":" arg ("," arg)*)?
```

- **Variable references**: bare names are matched greedily (longest run of words)
  against the defined variables, case-insensitive, whitespace-normalized. In
  expressions with multiple variables, always use `[Bracketed Names]` — greedy
  matching of bare names next to each other is ambiguous.
- **Unknown names are not errors**: a tag referencing an undefined name shows in
  the pane as a *proposed* variable for the user to define. Useful in live-document
  mode; in offline generation define everything in the store instead.
- Numbers are plain literals (`1000`, `0.5`). No strings, no function calls.
- A `|` inside `[...]` is part of the name, not a modifier separator.

## Format modifiers

Chained left-to-right with `|`; each receives the previous output. Names are
lowercase. Args are comma-separated after `:`. With no modifiers, numbers render
full-precision and ungrouped — so every numeric tag should carry modifiers or the
variable should have `defaultModifiers`.

| Modifier | Args | Example | Result |
|---|---|---|---|
| `currency` | code=USD, decimals=0 | `1234.5 \| currency:USD,2` | `$1,234.50` |
| `percent` | decimals=1 — **input is a ratio** | `0.125 \| percent:1` | `12.5%` |
| `number` | decimals=0 | `1234567 \| number` | `1,234,567` |
| `abbrev` | decimals=1, prefix="" | `1234567 \| abbrev:1,$` | `$1.2M` (K/M/B/T) |
| `abs` | — | `-500 \| abs \| abbrev:0,$` | `$500` |
| `updown` | upWord=up, downWord=down, flatWord=flat — uses the sign of the **original** value | `-500 \| updown:higher,lower` | `lower` |
| `sign` | — prefix `+` on positives | `500 \| number \| sign` | `+500` |
| `paren` | — negatives in parentheses | `-1234 \| number \| paren` | `(1,234)` |
| `words` | mode (`approx`), sigDigits=2 | `1200000 \| words:approx` | `one point two million` |
| `date` | moment.js format, default `YYYY-MM-DD` | `2026-06-30 \| date:MMM D, YYYY` | `Jun 30, 2026` |
| `monthlong` | — | `Jun \| monthlong` | `June` |
| `monthshort` | — | `June \| monthshort` | `Jun` |
| `upper` / `lower` / `capitalize` | — | `June \| upper` | `JUNE` |

Recipes:

- Money on a KPI tile: `<<GOP | abbrev:1,$>>`; in a table: `<<GOP | currency:USD,0>>`
  or `<<GOP | number | paren>>` for accounting style.
- Occupancy (stored as a ratio): `<<Occ | percent:1>>`.
- Variance prose: `<<Var | updown>> <<Var | abs | abbrev:1,$>>` → "down $1.3M".
- Variance in a table: `<<Var | number | sign>>` or `<<Var | number | paren>>`.
- Signed percent: `<<Var Pct | percent:1 | sign>>` → "+4.2%".

## Authoring rules

- The tag must be complete within one text frame / table cell; don't split across
  runs is fine (the add-in scans plain text), but don't split across shapes/cells.
- Tags take on the character formatting of the text they replace — format the tag
  text itself as the number should appear.
- An unmatched `<<` (half-deleted tag) triggers a document warning in the pane;
  don't leave stray delimiters in generated files.
- `percent` multiplies by 100 — feed it ratios (0.72), not percents (72). The
  validated pairing: a query on `Total Occ % - 100` rendered correctly with
  `| percent:1` (the account returns a ratio). If a % account looks 100× off,
  switch between `percent:1` and `number:1` with a literal `%` in the slide text.
