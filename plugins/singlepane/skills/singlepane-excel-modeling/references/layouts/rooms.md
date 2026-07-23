# Rooms — Singlepane detailed-financials layout

Read [../usali-layouts.md](../usali-layouts.md) first for how to read this table,
exact-string traps, and KPI-row recipes. USALI strings must be copied verbatim into
SP.FINANCIALS.

Department 100. Rooms revenue by market segment (room nights / ADR / revenue triplets), other rooms revenue, then the full rooms expense schedule and labor-hours stats.

| Row label | USALI string (exact) | Notes |
|---|---|---|
| **ROOMS REVENUE** | — | SECTION HEADER |
| Retail - RN | `Retail Rooms Sold - 100` |  |
| Retail - ADR | `Transient Retail - 100` | KPI (segment ADR): `Transient Retail - 100` ÷ `Retail Rooms Sold - 100` |
| Retail - Revenue | `Transient Retail - 100` |  |
| Discount - RN | `Discount Rooms Sold - 100` |  |
| Discount - ADR | `Transient Discount - 100` | KPI (segment ADR): `Transient Discount - 100` ÷ `Discount Rooms Sold - 100` |
| Discount - Revenue | `Transient Discount - 100` |  |
| Negotiated - RN | `Negotiated Rooms Sold - 100` |  |
| Negotiated - ADR | `Transient Negotiated - 100` | KPI (segment ADR): `Transient Negotiated - 100` ÷ `Negotiated Rooms Sold - 100` |
| Negotiated - Revenue | `Transient Negotiated - 100` |  |
| Qualified - RN | `Qualified Rooms Sold - 100` |  |
| Qualified - ADR | `Transient Qualified - 100` | KPI (segment ADR): `Transient Qualified - 100` ÷ `Qualified Rooms Sold - 100` |
| Qualified - Revenue | `Transient Qualified - 100` |  |
| Wholesale - RN | `Wholesale Rooms Sold - 100` |  |
| Wholesale - ADR | `Transient Wholesale - 100` | KPI (segment ADR): `Transient Wholesale - 100` ÷ `Wholesale Rooms Sold - 100` |
| Wholesale - Revenue | `Transient Wholesale - 100` |  |
| Other - RN | `Other Transient Rooms Sold - 100` |  |
| Other - ADR | `Transient Other - 100` | KPI (segment ADR): `Transient Other - 100` ÷ `Other Transient Rooms Sold - 100` |
| Other - Revenue | `Transient Other - 100` |  |
| Rebates | `Transient Rebates and Subsidies - 100` |  |
| Total Transient - RN | `Transient Rooms Sold - 100` | bold/subtotal |
| Total Transient - ADR | `Transient Rooms Revenue - 100` | bold/subtotal; KPI (segment ADR): `Transient Rooms Revenue - 100` ÷ `Transient Rooms Sold - 100` |
| Total Transient - Revenue | `Transient Rooms Revenue - 100` | bold/subtotal |
| Association/Convention - RN | `Association/Convention Rooms Sold - 100` |  |
| Association/Convention - ADR | `Group Association/Convention - 100` | KPI (segment ADR): `Group Association/Convention - 100` ÷ `Association/Convention Rooms Sold - 100` |
| Association/Convention - Revenue | `Group Association/Convention - 100` |  |
| Corporate - RN | `Corporate Rooms Sold - 100` |  |
| Corporate - ADR | `Group Corporate - 100` | KPI (segment ADR): `Group Corporate - 100` ÷ `Corporate Rooms Sold - 100` |
| Corporate - Revenue | `Group Corporate - 100` |  |
| Government - RN | `Government Rooms Sold - 100` |  |
| Government - ADR | `Group Government - 100` | KPI (segment ADR): `Group Government - 100` ÷ `Government Rooms Sold - 100` |
| Government - Revenue | `Group Government - 100` |  |
| Tour & Travel - RN | `Tour/Wholesalers Rooms Sold - 100` |  |
| Tour & Travel - ADR | `Group Tour/Wholesalers - 100` | KPI (segment ADR): `Group Tour/Wholesalers - 100` ÷ `Tour/Wholesalers Rooms Sold - 100` |
| Tour & Travel - Revenue | `Group Tour/Wholesalers - 100` |  |
| SMERF - RN | `SMERF Rooms Sold - 100` |  |
| SMERF - ADR | `Group SMERF - 100` | KPI (segment ADR): `Group SMERF - 100` ÷ `SMERF Rooms Sold - 100` |
| SMERF - Revenue | `Group SMERF - 100` |  |
| Other - RN | `Other Group Rooms Sold - 100` |  |
| Other - ADR | `Group Other - 100` | KPI (segment ADR): `Group Other - 100` ÷ `Other Group Rooms Sold - 100` |
| Other - Revenue | `Group Other - 100` |  |
| Rebates | `Group Rebates and Subsidies - 100` |  |
| Total Group - RN | `Group Rooms Sold - 100` | bold/subtotal |
| Total Group - ADR | `Group Rooms Revenue - 100` | bold/subtotal; KPI (segment ADR): `Group Rooms Revenue - 100` ÷ `Group Rooms Sold - 100` |
| Total Group - Revenue | `Group Rooms Revenue - 100` | bold/subtotal |
| Contract - RN | `Contract Rooms Sold - 100` | bold/subtotal |
| Contract - ADR | `Contract Rooms Revenue - 100` | bold/subtotal; KPI (segment ADR): `Contract Rooms Revenue - 100` ÷ `Contract Rooms Sold - 100` |
| Contract - Revenue | `Contract Rooms Revenue - 100` | bold/subtotal |
| Total Package Revenue | `Total Package Revenue - 100` | bold/subtotal |
| Complimentary RN | `Total Rooms Comp - 100` | bold/subtotal |
| Rooms Only Revenue | `Rooms Only Revenue - 100` |  |
| Day Use | `Day Use Revenue - 100` |  |
| Early Departure | `Early Departure Revenue - 100` |  |
| Late Check-out Fee | `Late Check-Out Fee Revenue - 100` |  |
| No Show | `No Show Revenue - 100` |  |
| Miscelleneous | `Rooms Misc Revenue - 100` |  |
| Surcharge & Service charge | `Rooms Surcharge & Service Charge Revenue - 100` |  |
| Club Lounge | `Club Lounge Revenue - 100` |  |
| Total Other Revenue | `Other Rooms Revenue - 100` | bold/subtotal |
| Summary Level Rooms Revenue | `Summary Rooms Revenue - 100` | bold/subtotal |
| All-Inclusive Package Contra Revenue | `AI Package Contra Revenue - 100` | bold/subtotal |
| Allowance | `Allowances - 100` | bold/subtotal |
| Occupancy (Total) | `Total Rooms Sold - 100` | bold/subtotal; KPI: `Total Rooms Sold - 100` ÷ `Total Rooms Available - 100` |
| Occupancy (Paid) | `Total Rooms Occupied - 100` | bold/subtotal; KPI: `Total Rooms Occupied - 100` ÷ `Total Rooms Available - 100` |
| Total Rooms Sold | `Total Rooms Sold - 100` | bold/subtotal |
| Total Rooms Occupied | `Total Rooms Occupied - 100` | bold/subtotal |
| Total ADR (Paid) | `Total Revenue - 100` | bold/subtotal; KPI: `Total Revenue - 100` ÷ `Total Rooms Occupied - 100` |
| Total Rooms Revenue | `Total Revenue - 100` | bold/subtotal |
| RevPAR | `Total Revenue - 100` | bold/subtotal; KPI: `Total Revenue - 100` ÷ `Total Rooms Available - 100` |
| **ROOMS EXPENSES** | — | SECTION HEADER |
| **SALARIES, WAGES AND BONUSES** | — | SECTION HEADER |
| Management | `S&W Management - 100` | bold/subtotal |
| Housekeeping REG | `Housekeeping Management Reg S&W - 100` |  |
| Housekeeping OT | `Housekeeping Management OT S&W - 100` |  |
| Front Desk REG | `Front Desk Management Reg S&W - 100` |  |
| Front Desk OT | `Front Desk Management OT S&W - 100` |  |
| Unassigned REG | `Unassigned Management Reg S&W - 100` |  |
| Unassigned OT | `Unassigned Management OT S&W - 100` |  |
| Non-Management | `S&W Non-Management - 100` | bold/subtotal |
| Housekeeping REG | `Housekeeping Reg S&W - 100` |  |
| Housekeeping OT | `Housekeeping OT S&W - 100` |  |
| Front Desk REG | `Front Desk Reg S&W - 100` |  |
| Front Desk OT | `Front Desk OT S&W - 100` |  |
| Reservations REG | `Reservations Reg S&W - 100` |  |
| Reservations OT | `Reservations OT S&W - 100` |  |
| Comp F&B REG | `Comp F&B Reg S&W - 100` |  |
| Comp F&B OT | `Comp F&B OT S&W - 100` |  |
| Unassigned REG | `Rooms Unassigned Reg S&W - 100` |  |
| Unassigned OT | `Rooms Unassigned OT S&W - 100` |  |
| Other | `S&W Other - 100` |  |
| Total Salaries and Wages | `Total Salaries & Wages - 100` | bold/subtotal |
| Contract Labor | `Total Contracted Leased & Outsourced Labor - 100` |  |
| Service Charge Distribution | `Total Service Charge Distribution - 100` |  |
| Bonus and Incentive Pay | `Total Bonuses & Incentives - 100` |  |
| Total Salaries, Wages and Bonuses | `Total Salaries Wages & Bonuses - 100` | bold/subtotal |
| **PAYROLL RELATED EXPENSES** | — | SECTION HEADER |
| Personal Days | `Personal Days - 100` |  |
| Sick Pays | `Sick Pay - 100` |  |
| Holiday Pay | `Holiday Pay - 100` |  |
| Vacation/ Paid Time Off | `Vacation/Paid Time Off - 100` |  |
| Severance Pay | `Severance Pay - 100` |  |
| Parental Leave | `Parental Leave - 100` |  |
| Other Pay | `Other Pay - 100` |  |
| Supplemental Pay | `Total Supplemental Pay - 100` | bold/subtotal |
| Automobile Allowance | `Automobile Allowance - 100` |  |
| Child Care | `Child Care - 100` |  |
| Contributory Savings Plan | `Contributory Savings Plan - 100` |  |
| Dental Insurance | `Dental Insurance - 100` |  |
| Disability Insurance | `Disability Insurance - 100` |  |
| Expat Benefits | `Expat Benefits - 100` |  |
| Group Life Insurance | `Group Life Insurance - 100` |  |
| Health Insurance | `Health Insurance - 100` |  |
| Housing and Educational | `Housing and Educational - 100` |  |
| Meals | `Meals - 100` |  |
| Miscellaneous Benefits | `Miscellaneous Benefits - 100` |  |
| Nonunion Insurance | `Nonunion Insurance - 100` |  |
| Nonunion Pension | `Nonunion Pension - 100` |  |
| Profit Sharing | `Profit Sharing - 100` |  |
| Public Subsidized Transportation | `Public Subsidized Transportation - 100` |  |
| Stock Benefits | `Stock Benefits - 100` |  |
| Stock Options | `Stock Options - 100` |  |
| Union Insurance | `Union Insurance - 100` |  |
| Union Other | `Union Other - 100` |  |
| Union Pension | `Union Pension - 100` |  |
| Workers’ Compensation Insurance | `Workers Compensation Insurance - 100` |  |
| Employee Benefits | `Total Employee Benefits - 100` | bold/subtotal |
| Taxes | `Total Payroll Taxes - 100` | bold/subtotal |
| Total Payroll Related Expenses | `Total Payroll-Related Expenses - 100` | bold/subtotal |
| Total Labor | `Total Labor Costs & Related Expenses - 100` | bold/subtotal |
| **OTHER EXPENSES** | — | SECTION HEADER |
| Cleaning Supplies | `Cleaning Supplies - 100` |  |
| Cluster Services | `Cluster Services - 100` |  |
| Commissions | `Commissions - 100` |  |
| Commissions & Fees - Group | `Commissions & Fees - Group - 100` |  |
| Complimentary Food & Beverage | `Complimentary Food & Beverage - 100` |  |
| Complimentary In-Room/Media Entertainment | `Complimentary In-Room/Media Entertainment - 100` |  |
| Complimentary Services & Gifts | `Complimentary Services & Gifts - 100` |  |
| Contract Services | `Contract Services - 100` |  |
| Corporate Office Reimbursables | `Corporate Office Reimbursables - 100` |  |
| Decorations | `Decorations - 100` |  |
| Dues & Subscriptions | `Dues & Subscriptions - 100` |  |
| Entertainment- In-House | `Entertainment- In-House - 100` |  |
| Equipment Rental | `Equipment Rental - 100` |  |
| Guest Relocation | `Guest Relocation - 100` |  |
| Guest Supplies | `Guest Supplies - 100` |  |
| Guest Transportation | `Guest Transportation - 100` |  |
| Laundry & Dry Cleaning | `Laundry & Dry Cleaning - 100` |  |
| Licenses & Permits | `Licenses & Permits - 100` |  |
| Linen | `Linen - 100` |  |
| Miscellaneous | `Miscellaneous - 100` |  |
| Operating Supplies | `Operating Supplies - 100` |  |
| Postage & Overnight Delivery Charges | `Postage & Overnight Delivery Charges - 100` |  |
| Printing & Stationary | `Printing & Stationary - 100` |  |
| Reservations | `Reservations - 100` |  |
| Loyalty Program Member Benefits | `Loyalty Program Member Benefits - 100` |  |
| Royalty Fees | `Royalty Fees - 100` |  |
| Training | `Training - 100` |  |
| Travel - Meals & Entertainment | `Travel - Meals & Entertainment - 100` |  |
| Travel - Other | `Travel - Other - 100` |  |
| Uniform Costs | `Uniform Costs - 100` |  |
| Uniform Laundry | `Uniform Laundry - 100` |  |
| Club Lounge Cost | `Club Lounge Cost - 100` |  |
| Total Other Expenses | `Total Other Expenses - 100` | bold/subtotal |
| Total Rooms Expenses | `Total Departmental Expenses - 100` | bold/subtotal |
| Departmental Profit | `Dept Profit - 100` | bold/subtotal |
| **HOURS WORKED - STATS** | — | SECTION HEADER |
| Mgmt Hours Worked | `Mgmt Hours Worked - 100` | bold/subtotal |
| Housekeeping Management REG | `Housekeeping Management Reg Hours Worked - 100` |  |
| Housekeeping Management OT | `Housekeeping Management OT Hours Worked - 100` |  |
| Front Desk Management REG | `Front Desk Management Reg Hours Worked - 100` |  |
| Front Desk Management OT | `Front Desk Management OT Hours Worked - 100` |  |
| Unassigned Management REG | `Unassigned Management Reg Hours Worked - 100` |  |
| Unassigned Management OT | `Unassigned Management OT Hours Worked - 100` |  |
| Non-Mgmt Hours Worked | `Non-Mgmt Hours Worked - 100` | bold/subtotal |
| Housekeeping REG | `Housekeeping Reg Hours Worked - 100` |  |
| Housekeeping OT | `Housekeeping OT Hours Worked - 100` |  |
| Front Desk REG | `Front Desk Reg Hours Worked - 100` |  |
| Front Desk OT | `Front Desk OT Hours Worked - 100` |  |
| Reservations REG | `Reservations Reg Hours Worked - 100` |  |
| Reservations OT | `Reservations OT Hours Worked - 100` |  |
| Comp F&B REG | `Comp F&B Reg Hours Worked - 100` |  |
| Comp F&B OT | `Comp F&B OT Hours Worked - 100` |  |
| Unassigned REG | `Rooms Unassigned Reg Hours Worked - 100` |  |
| Unassigned OT | `Rooms Unassigned OT Hours Worked - 100` |  |
| Contract Labor | `Outside Labor Hours Worked - 100` | bold/subtotal |
| Total Hours Worked | `Total Hours Worked - 100` | bold/subtotal |

