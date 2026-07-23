# Labor — Singlepane detailed-financials layout

Read [../usali-layouts.md](../usali-layouts.md) first for how to read this table,
exact-string traps, and KPI-row recipes. USALI strings must be copied verbatim into
SP.FINANCIALS.

Property-wide labor view: 000-level totals broken out by department (100, 200, 300, 500–800, 940 House Laundry, 950 Staff Dining).

| Row label | USALI string (exact) | Notes |
|---|---|---|
| **SALARIES, WAGES AND BONUSES** | — | SECTION HEADER |
| Management | `S&W Management - 000` | bold/subtotal |
| Rooms | `S&W Management - 100` |  |
| Consolidated F&B | `S&W Management - 200` |  |
| Other Operated Dpt. | `S&W Management - 300` |  |
| A&G | `S&W Management - 500` |  |
| I&T | `S&W Management - 600` |  |
| S&M | `S&W Management - 700` |  |
| R&M | `S&W Management - 800` |  |
| House Laundry | `S&W Management - 940` |  |
| Staff Dining | `S&W Management - 950` |  |
| Non-Management | `S&W Non-Management - 000` | bold/subtotal |
| Rooms | `S&W Non-Management - 100` |  |
| Consolidated F&B | `S&W Non-Management - 200` |  |
| Other Operated Dpt. | `S&W Non-Management - 300` |  |
| A&G | `S&W Non-Management - 500` |  |
| I&T | `S&W Non-Management - 600` |  |
| S&M | `S&W Non-Management - 700` |  |
| R&M | `S&W Non-Management - 800` |  |
| House Laundry | `S&W Non-Management - 940` |  |
| Staff Dining | `S&W Non-Management - 950` |  |
| Other | `S&W Other - 000` | bold/subtotal |
| Total Salaries And Wages | `Total Salaries & Wages - 000` | bold/subtotal |
| Contract Labor | `Total Contracted Leased & Outsourced Labor - 000` | bold/subtotal |
| Rooms Contract Labor | `Total Contracted Leased & Outsourced Labor - 100` |  |
| Consolidated F&B Contract Labor | `Total Contracted Leased & Outsourced Labor - 200` |  |
| Other Operated Dpt. Contract Labor | `Total Contracted Leased & Outsourced Labor - 300` |  |
| A&G Contract Labor | `Total Contracted Leased & Outsourced Labor - 500` |  |
| I&T Contract Labor | `Total Contracted Leased & Outsourced Labor - 600` |  |
| S&M Contract Labor | `Total Contracted Leased & Outsourced Labor - 700` |  |
| R&M Contract Labor | `Total Contracted Leased & Outsourced Labor - 800` |  |
| House Laundry Contract Labor | `Total Contracted Leased & Outsourced Labor - 940` |  |
| Staff Dining Contract Labor | `Total Contracted Leased & Outsourced Labor - 950` |  |
| Service Charge Distribution | `Total Service Charge Distribution - 000` |  |
| Bonus And Incentive Pay | `Total Bonuses & Incentives - 000` |  |
| Total Salaries, Wages And Bonuses | `Total Salaries Wages & Bonuses - 000` | bold/subtotal |
| **PAYROLL RELATED EXPENSES** | — | SECTION HEADER |
| Personal Days | `Personal Days - 000` |  |
| Sick Pays | `Sick Pay - 000` |  |
| Holiday Pay | `Holiday Pay - 000` |  |
| Vacation/ Paid Time Off | `Vacation/Paid Time Off - 000` |  |
| Severance Pay | `Severance Pay - 000` |  |
| Parental Leave | `Parental Leave - 000` |  |
| Other Pay | `Other Pay - 000` |  |
| Supplemental Pay | `Total Supplemental Pay - 000` | bold/subtotal |
| Automobile Allowance | `Automobile Allowance - 000` |  |
| Child Care | `Child Care - 000` |  |
| Contributory Savings Plan | `Contributory Savings Plan - 000` |  |
| Dental Insurance | `Dental Insurance - 000` |  |
| Disability Insurance | `Disability Insurance - 000` |  |
| Expat Benefits | `Expat Benefits - 000` |  |
| Group Life Insurance | `Group Life Insurance - 000` |  |
| Health Insurance | `Health Insurance - 000` |  |
| Housing And Educational | `Housing and Educational - 000` |  |
| Meals | `Meals - 000` |  |
| Miscellaneous Benefits | `Miscellaneous Benefits - 000` |  |
| Nonunion Insurance | `Nonunion Insurance - 000` |  |
| Nonunion Pension | `Nonunion Pension - 000` |  |
| Profit Sharing | `Profit Sharing - 000` |  |
| Public Subsidized Transportation | `Public Subsidized Transportation - 000` |  |
| Stock Benefits | `Stock Benefits - 000` |  |
| Stock Options | `Stock Options - 000` |  |
| Union Insurance | `Union Insurance - 000` |  |
| Union Other | `Union Other - 000` |  |
| Union Pension | `Union Pension - 000` |  |
| Workers Compensation Insurance | `Workers Compensation Insurance - 000` |  |
| Employee Benefits | `Total Employee Benefits - 000` | bold/subtotal |
| Taxes | `Total Payroll Taxes - 000` |  |
| Total Payroll Related Expenses | `Total Payroll-Related Expenses - 000` | bold/subtotal |
| Total Labor | `Total Labor Costs & Related Expenses - 000` | bold/subtotal |
| **HOURS WORKED - STATS** | — | SECTION HEADER |
| Mgmt Hours Worked | `Mgmt Hours Worked  - 000` | bold/subtotal |
| Rooms | `Mgmt Hours Worked - 100` |  |
| Consolidated F&B | `Mgmt Hours Worked - 200` |  |
| Other Operated Dpt. | `Consolidated Management Hours Worked - 300` |  |
| A&G | `Mgmt Hours Worked - 500` |  |
| I&T | `Mgmt Hours Worked - 600` |  |
| S&M | `Mgmt Hours Worked - 700` |  |
| R&M | `Mgmt Hours Worked - 800` |  |
| House Laundry | `Mgmt Hours Worked - 940` |  |
| Staff Dining | `Mgmt Hours Worked - 950` |  |
| Non-Mgmt Hours Worked | `Non Mgmt Hours Worked  - 000` | bold/subtotal |
| Rooms | `Non-Mgmt Hours Worked - 100` |  |
| Consolidated F&B | `Non-Mgmt Hours Worked - 200` |  |
| Other Operated Dpt. | `Consolidated Non-Management Hours Worked - 300` |  |
| A&G | `Non-Mgmt Hours Worked - 500` |  |
| I&T | `Non-Mgmt Hours Worked - 600` |  |
| S&M | `Non-Mgmt Hours Worked - 700` |  |
| R&M | `Non-Mgmt Hours Worked - 800` |  |
| House Laundry | `Non-Mgmt Hours Worked - 940` |  |
| Staff Dining | `Non-Mgmt Hours Worked - 950` |  |
| Contract Labor Hours Worked | `Outside Labor Hours Worked - 000` | bold/subtotal |
| Rooms Contract Labor | `Outside Labor Hours Worked - 100` |  |
| Consolidated F&B Contract Labor | `Outside Labor Hours Worked - 200` |  |
| Other Operated Dpt. Contract Labor | `Total Contracted Leased & Outsourced Hours Worked - 300` |  |
| A&G Contract Labor | `Outside Labor Hours Worked - 500` |  |
| I&T Contract Labor | `Outside Labor Hours Worked - 600` |  |
| S&M Contract Labor | `Outside Labor Hours Worked - 700` |  |
| R&M Contract Labor | `Outside Labor Hours Worked - 800` |  |
| House Laundry Contract Labor | `Total Contracted Leased & Outsourced Hours Worked - 940` |  |
| Staff Dining Contract Labor | `Outside Labor Hours Worked - 950` |  |
| Total Hours Worked | `Total Hours Worked - 000` | bold/subtotal |

