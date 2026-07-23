# Summary — Singlepane detailed-financials layout

Read [../usali-layouts.md](../usali-layouts.md) first for how to read this table,
exact-string traps, and KPI-row recipes. USALI strings must be copied verbatim into
SP.FINANCIALS.

The owner/executive P&L. KPI block first, then the full USALI summary flow: revenue → departmental expenses → departmental profit → undistributed → GOP → fees → non-operating → EBITDA → NOI → net income. This is the default layout for a "summary P&L" request.

| Row label | USALI string (exact) | Notes |
|---|---|---|
| Rooms available | `Total Rooms Available - 100` |  |
| Rooms sold | `Total Rooms Sold - 100` |  |
| Rooms Occupied | `Total Rooms Occupied - 100` |  |
| Occupancy (Total) | `Total Rooms Occupied - 100` | KPI: `Total Rooms Occupied - 100` ÷ `Total Rooms Available - 100` |
| Occupancy | `Total Rooms Sold - 100` | KPI: `Total Rooms Sold - 100` ÷ `Total Rooms Available - 100` |
| ADR | `Total Revenue - 100` | KPI: `Total Revenue - 100` ÷ `Total Rooms Occupied - 100` |
| RevPAR | `Total Revenue - 100` | KPI: `Total Revenue - 100` ÷ `Total Rooms Available - 100` |
| Package ADR | `Total Package Revenue - 100` | KPI: `Total Package Revenue - 100` ÷ `Total Rooms Occupied - 100` |
| Package RevPAR | `Total Package Revenue - 100` | KPI: `Total Package Revenue - 100` ÷ `Total Rooms Available - 100` |
| TRevPAR | `Total Revenue - 000` | KPI: `Total Revenue - 000` ÷ `Total Rooms Available - 100` |
| GOPPAR | `Total Hotel GOP - 000` | KPI: `Total Hotel GOP - 000` ÷ `Total Rooms Available - 100` |
| LPAR | `Total Labor Costs & Related Expenses - 000` | KPI: `Total Labor Costs & Related Expenses - 000` ÷ `Total Rooms Available - 100` |
| **OPERATING REVENUE** | — | SECTION HEADER |
| Rooms | `Total Revenue - 100` |  |
| Food & Beverage | `Total Revenue - 200` |  |
| Other Operated Departments | `Total Revenue - 300` |  |
| Miscellaneous Income | `Total Revenue - 400` |  |
| Total Operating revenue | `Total Revenue - 000` | bold/subtotal |
| **DEPARTMENTAL EXPENSES** | — | SECTION HEADER |
| Rooms | `Total Departmental Expenses - 100` |  |
| Food & Beverage | `Total Departmental Expenses - 200` |  |
| Other Operated Departments | `Total Departmental Expenses - 300` |  |
| Total Departmental Expenses | `Total Departmental Expenses - 000` | bold/subtotal |
| **DEPARTMENTAL PROFIT** | — | SECTION HEADER |
| Rooms | `Dept Profit - 100` |  |
| Food & Beverage | `Dept Profit - 200` |  |
| Other Operated Departments | `Dept Profit - 300` |  |
| Miscellaneous Income | `Total Revenue - 400` |  |
| Total Departmental Profit | `Total Departmental Income (Loss) - 000` | bold/subtotal |
| **UNDISTRIBUTED EXPENSES** | — | SECTION HEADER |
| Administrative & General | `Total Departmental Expenses - 500` |  |
| Sales & Marketing | `Total Departmental Expenses (ex FF) - 700` |  |
| Franchise Fees | `Franchise Fees - 700` |  |
| Information & Telecom Systems | `Total Departmental Expenses - 600` |  |
| Repair & Maintenance | `Total Departmental Expenses - 800` |  |
| Utilities | `Total Utilities Expense - 810` |  |
| Total Undistributed Expenses | `Total Undistributed Expenses - 000` | bold/subtotal |
| Gross Operating Profit | `Total Hotel GOP - 000` | bold/subtotal |
| **MANAGEMENT FEES** | — | SECTION HEADER |
| Base Fee | `Base Fee - 920` |  |
| Incentive Fee | `Incentive Fee - 920` |  |
| Other Fees | `Other Fee - 920` |  |
| Total Management Fees | `Total Management Fees - 920` | bold/subtotal |
| **NON-OPERATING INCOME AND EXPENSES** | — | SECTION HEADER |
| Non-operating Income | `Total Non-Operating Income - 900` |  |
| Rental & Leases | `Total Rent - 900` |  |
| Property and other taxes | `Total Taxes - 900` |  |
| Insurance | `Total Insurance - 900` |  |
| Foreign Exchange Gains or Losses | `FX Gain Loss - 900` |  |
| Other | `Total Other Expenses - 900` |  |
| Total Non-operating Income & Expenses | `Total Non-Op - 000` | bold/subtotal |
| EBITDA | `Total EBITDA - 000` | bold/subtotal |
| Replacement reserve | `FF&E - 930` |  |
| EBITDA less Reserves | `Total EBITDA Less Reserves - 000` | bold/subtotal |
| Interest | `Total Interest - 910` |  |
| Depreciation | `Total Depreciation - 910` |  |
| Other Capital Expenses | `Total Other Capital Expenses - 910` |  |
| Amortization | `Amortization Expense - 910` |  |
| Total Interest, Depreciation & Amortization | `Total Interest Depreciation & Amortization - 910` | bold/subtotal |
| Hotel Net Income | `Hotel Net Operating Income - 000` | bold/subtotal |
| Corporate Adjustments | `Adjustments - 000` | bold/subtotal |
| Net Income | `Total Net Operating Income - 000` | bold/subtotal |

