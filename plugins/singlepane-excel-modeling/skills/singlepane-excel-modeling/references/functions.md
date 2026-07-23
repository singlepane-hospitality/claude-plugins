# Singlepane SP.* function reference

Complete argument-level reference for the supported functions in the add-in (v2.1.x).
All functions are async (Excel shows `#BUSY!` briefly) and require the user to be signed
in. Arguments accept literals (`"ACD"`) — but per the skill's conventions, prefer cell
references to input cells for every argument.

**Supported functions — use ONLY these.** Other `SP.*` functions exist in the add-in
(dashboard/spill data functions like `SP.REV_GOP_EBITDA`, `SP.FLOW_THROUGH`,
`SP.STR_INDEX`, `SP.RISK_UPSIDE`, `SP.GUEST_SATISFACTION`, plus scalar helpers like
`SP.GET_HOTEL_ATTRIBUTE`, `SP.GET_STAR_ID`, `SP.PROPERTY_COUNT`) — they are legacy /
undocumented and must not be used in new models. If you see them in an existing
workbook, leave them alone but don't propagate them. Build everything from:

1. `SP.FINANCIALS` / `SP.FINANCIALS_AGG` — financial data
2. `SP.FILTER` — property-code selection
3. `SP.STR` — STR comp-set data
4. `SP.OTB` — on-the-books / pace
5. `SP.GET_INTEREST_RATE` — benchmark rates
6. `SP.GET_HOTEL_REFERENCE` / `SP.GET_USALI_REFERENCE` — reference spills

---

## 1. SP.FINANCIALS(code, usali, month, year, version)

One P&L / budget / forecast value for one property. Returns a number (0 if no data).

| Arg | Type | Valid values |
|---|---|---|
| code | string | A property code from "My Properties" (e.g. `"ACD"`) |
| usali | string | An exact line from "Usali Reference", e.g. `"Total Revenue - 100"`, including the ` - <number>` suffix. See [usali-layouts.md](usali-layouts.md) for the canonical report layouts and their exact strings |
| month | string | `"Jan"`–`"Dec"` · `"Total Year"` · `"Q1"`/`"Q2"`/`"Q3"`/`"Q4"` · `"<Mon>YTD"` (e.g. `"JulYTD"`) · `"<Mon>TTM"` trailing-12 · `"<Mon>BOY"` balance-of-year — month+suffix has no space |
| year | number | 4-digit year |
| version | string | `"Actual"`, `"Budget"`, `"Budget1"`–`"Budget12"`, `"Forecast1"`–`"Forecast12"`, `"Proforma"`, `"LY_Actual"`, `"Var_Budget"`, `"Var_LY_Actual"`. Case-insensitive. Companies may have additional named versions. |

```excel
=SP.FINANCIALS($B$1,$A6,C$4,$B$2,$B$3)      // all args from input cells — preferred
=SP.FINANCIALS("ACD","Total Revenue - 100","JulYTD",2025,"Actual")   // literal form
```

## 2. SP.FINANCIALS_AGG(codes, usali, month, year, version)

Identical to SP.FINANCIALS but `codes` is a **range or array of property codes** and the
result is aggregated across them. A header cell containing `codes` (as spilled by
SP.FILTER) is ignored automatically, so you can pass a FILTER spill directly.

```excel
=SP.FINANCIALS_AGG(Inputs!$A$2#,$A6,C$4,$B$2,$B$3)   // spill reference from inputs sheet
=SP.FINANCIALS_AGG(SP.FILTER(,"Brand",$B$1),"Total Revenue - 100","Jun",2025,"Actual")
```

Aggregation semantics: values are summed across properties for currency/count accounts.
For ratio-type lines (occupancy %, ADR, margins) compute the ratio from aggregated
components rather than aggregating the ratio line.

## 3. SP.FILTER([codes], [filter1], [value1], … [filter5], [value5]) — spills

Returns a one-column array of property codes (header row `codes`) matching up to five
attribute filters, ANDed together. Each value can be a single string, a comma-separated
list (OR within the filter), or a range of cells.

| Arg | Notes |
|---|---|
| codes (optional) | Range of codes to restrict the search to; omit to search all authorized hotels (leave the slot empty: `SP.FILTER(,"Brand",$B$1)`) |
| filterN | Attribute name — see list below |
| valueN | Matching value(s) for filterN — prefer an input cell |

Valid filter attribute names: `Ownership`, `ManagementCompany`, `HotelCompany`,
`Brand`, `ManagedOrFranchised`, `Market`, `STRMarketClass`, `RoomRange`, `Union`,
`Rooms`, `AssetManager`, `Fund`, `Lender`, `ServiceLevel`, `ProductType`,
`InvestmentStage`, `MeetingSpaceSqft`, `UDF1`–`UDF20`.

Values are exact strings from the user's data (check the "My Properties" sheet — e.g.
"Marriott" may live in `HotelCompany` while `Brand` holds the flag like "Courtyard").

```excel
=SP.FILTER(,"ProductType","Resort,Urban")                       // OR within one filter
=SP.FILTER(,"Brand",$B$1,"Market",$B$2)                         // AND across filters
```

Returns `No data` if nothing matches. Primarily designed to feed SP.FINANCIALS_AGG.

## 4. SP.STR(code, date, aggregateType, metric, [subject_comp_market], [segment])

STR (Smith Travel Research) performance for the subject hotel and its comp sets.
Returns a scalar.

| Arg | Valid values |
|---|---|
| code | Property code |
| date | `"YYYY-MM-DD"` or Excel date. Report date — e.g. month-end for monthly data |
| aggregateType | **Case-sensitive:** `day`, `month`, `monthToDate`, `currentWeek`, `running28Days`, `yearToDate`, `running3Month`, `running12Month` |
| metric | `Occ`, `ADR`, `RevPAR` · `% Chg` variants: `Occ % Chg`, `ADR % Chg`, `RevPAR % Chg` · indexes: `MPI`, `ARI`, `RGI` (+ `% Chg` variants) · ranks: `Occ Rank`, `ADR Rank`, `RevPAR Rank`, `Occ % Chg Rank`, `ADR % Chg Rank`, `RevPAR % Chg Rank` (case-insensitive) |
| subject_comp_market (optional, default `Subject`) | `Subject`, `CS1`–`CS5` (comp sets), `Market Scale` |
| segment (optional, default `Total`) | `Total`, `Group`, `Contract`, `Transient` |

```excel
=SP.STR($B$1,$A6,"month",C$5,C$4,"Total")                 // grid form off input cells
=SP.STR("ACD","2025-06-30","month","RGI","CS2","Total")   // June RGI vs comp set 2
```

**Which date to pass for each aggregate type** — getting this wrong returns no/wrong
data:

| Aggregate type | Date to pass | Excel helper |
|---|---|---|
| `month`, `yearToDate`, `running3Month`, `running12Month` | **Month-end date** (28th/30th/31st) of the period's last month | `=EOMONTH(date,0)` |
| `currentWeek`, `running28Days` | **A Saturday** — STR weeks end Saturday | most recent Saturday on/before d: `=d-WEEKDAY(d,16)+1` |
| `day`, `monthToDate` | The actual day you want (for `monthToDate`, the as-of day) | — |

When building a monthly STR grid, generate the date column with
`=EOMONTH(DATE($B$2,ROW()-5,1),0)`-style formulas so every row is guaranteed to be a
month-end; for weekly grids, step `=A6+7` from a known Saturday.

Note on indexes: MPI/ARI/RGI are already subject-vs-compset ratios, so requesting an
index for `CS1`–`CS5` returns the index computed against that comp set. Occ/ADR/RevPAR
with `CS1`–`CS5` return the comp set's own performance.

## 5. SP.OTB(code, dailyOrMonthly, stayDate, targetSet, periodType, metric, segment, [asOfDate])

Reservation / pace data for stay dates as of a booking snapshot date.

| Arg | Valid values |
|---|---|
| code | Property code |
| dailyOrMonthly | `"daily"` or `"monthly"` |
| stayDate | `"YYYY-MM-DD"` or Excel date. For `monthly`, use the first of the month |
| targetSet | `"subject"` (the hotel) or `"cs"` (comp set) |
| periodType | `"ty"` (this year) or `"ly"` (same time last year, offset dates) |
| metric | `occ`, `rn` (room nights), `adr`, `revenue`, `revpar`, `as_of_date` (returns the snapshot date actually used) |
| segment | `"total"`, `"group"`, `"transient"` |
| asOfDate (optional) | Snapshot date — uses the nearest as-of date **not exceeding** this. Omit for the latest available. Put it in an input cell so the whole report reprices from one cell |

```excel
=SP.OTB($B$1,"monthly",$A6,"subject","ty","revenue","total",$B$2)
=SP.OTB($B$1,"monthly",$A6,"subject","ly","revenue","total",$B$2)   // STLY pair for pace
```

Pace = ty vs ly at the same as-of offset: build both columns and difference them.
Metric availability can vary with the property's data subscriptions.

## 6. SP.GET_INTEREST_RATE(benchmark_rate, date, [as_of_date])

Percent rate for a benchmark on a date (forward-curve values for future dates).

| Arg | Valid values |
|---|---|
| benchmark_rate | `"SOFR"`, `"SONIA"`, `"T10YR"` (case-insensitive) |
| date | Date the rate applies to |
| as_of_date (optional) | Which model-update date's curve to use — pin it in an input cell so the model doesn't shift when curves update |

```excel
=SP.GET_INTEREST_RATE($B$1,$A6,$B$2)
```

Returned as a percent (e.g. `5.33` = 5.33%) — divide by 100 before using in interest
calculations, and verify scale against a known value on first use.

## 7. Reference spills

### SP.GET_HOTEL_REFERENCE() — spills
Every authorized hotel × every attribute. This is what populates the auto-created
"My Properties" sheet. Columns, in order:
`Code, StarId, HotelName, Ownership, ManagementCompany, HotelCompany, Brand,
ManagedOrFranchised, Market, STRMarketClass, RoomRange, Union, Rooms, AssetManager,
OpenDate, AcquisitionDate, SaleDate, Fund, Lender, ServiceLevel, ProductType,
InvestmentStage, MeetingSpaceSqft, UDF1…UDF20, Address, City, State, Country, SuiteMix,
TwoBeddedMix, InteriorMeetingSpaceSqft, OutdoorMeetingSpaceSqft,
LargestMeetingSpaceSqft, NumberOfMeetingSpaces, STRSubClass, LatestRenovationYear,
ResortFee, ResortFeeAmount, HasSpa, SpaManagement, SpaNumberTreatmentRooms,
FitnessCenterSqft, NumberIndoorPools, NumberOutdoorPools, IsMixedUse, HasSki,
HasWaterpark, HasCasino, HasGolf, IsResort, AllInclusive, MaterialFBRevenue,
NumberInHouseFBOutlets, NumberManagedFBOutlets, OffersParking, UnionContractStart,
UnionContractEnd, UnionHousekeeping, UnionFrontDesk, UnionFB, UnionEngineering,
LaundryType, PropertyType`

To use a single attribute in a model (room count, brand, market), `XLOOKUP` the code
against the "My Properties" sheet rather than calling any per-attribute function:
```excel
=XLOOKUP($B$1,'My Properties'!A:A,'My Properties'!M:M)    // Rooms for the input code
```

### SP.GET_USALI_REFERENCE() — spills
All USALI/GL account lines. Columns: `usali, category, dept, sub_dept, default_metric`.
The `usali` column is the exact string SP.FINANCIALS expects. Populates the
auto-created "Usali Reference" sheet. Handy as the source range for a data-validation
dropdown on a USALI input cell.

---

## Caching & batching

- FINANCIALS, FINANCIALS_AGG, STR, OTB, and FILTER batch all concurrent cell calls into
  one backend request (100 ms window) and cache results for up to 12 hours — large
  models recalc fast; a grid of thousands of SP.FINANCIALS cells is a normal, supported
  design.
- Reference spills cache for the whole session; GET_INTEREST_RATE is never cached.
- The task pane's **Clear Cached Data** + **Recalculate All Functions** force a full
  refresh.
