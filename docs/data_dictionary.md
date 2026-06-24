# Mutual Fund Analytics – Data Dictionary

## Dataset 1: fund_master.csv

| Column             | Data Type | Business Definition                |
| ------------------ | --------- | ---------------------------------- |
| amfi_code          | INTEGER   | Unique AMFI scheme code            |
| fund_house         | TEXT      | Mutual fund company                |
| scheme_name        | TEXT      | Name of the mutual fund scheme     |
| category           | TEXT      | Fund category (Equity/Debt/Hybrid) |
| sub_category       | TEXT      | Specific fund type                 |
| plan               | TEXT      | Regular or Direct plan             |
| launch_date        | DATE      | Scheme launch date                 |
| benchmark          | TEXT      | Benchmark index                    |
| expense_ratio_pct  | REAL      | Annual expense ratio (%)           |
| exit_load_pct      | REAL      | Exit load percentage               |
| min_sip_amount     | INTEGER   | Minimum SIP investment             |
| min_lumpsum_amount | INTEGER   | Minimum lump sum investment        |
| fund_manager       | TEXT      | Fund manager name                  |
| risk_category      | TEXT      | Risk level                         |
| sebi_category_code | TEXT      | SEBI category identifier           |

---

## Dataset 2: nav_history.csv

| Column    | Data Type | Business Definition |
| --------- | --------- | ------------------- |
| amfi_code | INTEGER   | Scheme identifier   |
| date      | DATE      | NAV date            |
| nav       | REAL      | Net Asset Value     |

---

## Dataset 3: aum_by_fund_house.csv

| Column         | Data Type | Business Definition |
| -------------- | --------- | ------------------- |
| date           | DATE      | Reporting date      |
| fund_house     | TEXT      | Mutual fund company |
| aum_lakh_crore | REAL      | AUM in lakh crore   |
| aum_crore      | REAL      | AUM in crore        |
| num_schemes    | INTEGER   | Number of schemes   |

---

## Dataset 4: monthly_sip_inflows.csv

| Column                    | Data Type | Business Definition           |
| ------------------------- | --------- | ----------------------------- |
| month                     | TEXT      | Reporting month               |
| sip_inflow_crore          | REAL      | Monthly SIP inflow            |
| active_sip_accounts_crore | REAL      | Active SIP accounts           |
| new_sip_accounts_lakh     | REAL      | Newly registered SIP accounts |
| sip_aum_lakh_crore        | REAL      | SIP assets under management   |
| yoy_growth_pct            | REAL      | Year-over-year growth         |

---

## Dataset 5: category_inflows.csv

| Column           | Data Type | Business Definition         |
| ---------------- | --------- | --------------------------- |
| month            | TEXT      | Reporting month             |
| category         | TEXT      | Mutual fund category        |
| net_inflow_crore | REAL      | Net inflow for the category |

---

## Dataset 6: industry_folio_count.csv

Document each column similarly.

---

## Dataset 7: scheme_performance.csv

Document each column similarly.

---

## Dataset 8: investor_transactions.csv

Document each column similarly.

---

## Dataset 9: portfolio_holdings.csv

Document each column similarly.

---

## Dataset 10: benchmark_indices.csv

| Column      | Data Type | Business Definition |
| ----------- | --------- | ------------------- |
| date        | DATE      | Trading date        |
| index_name  | TEXT      | Benchmark index     |
| close_value | REAL      | Closing index value |

---

## Source

All datasets were provided as part of the Bluestock Fintech Internship Mutual Fund Analytics project and were cleaned and processed before loading into SQLite.
