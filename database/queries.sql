-- =====================================================
-- Bluestock Fintech Internship
-- Day 2 - Analytical SQL Queries
-- =====================================================

---------------------------------------------------------
-- 1. Top 5 Fund Houses by AUM
---------------------------------------------------------

SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM aum_by_fund_house
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

---------------------------------------------------------
-- 2. Average NAV per Month
---------------------------------------------------------

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 4) AS average_nav
FROM nav_history
GROUP BY month
ORDER BY month;

---------------------------------------------------------
-- 3. SIP YoY Growth
---------------------------------------------------------

SELECT
    SUBSTR(month, 1, 4) AS year,
    ROUND(SUM(sip_inflow_crore),2) AS total_sip_inflow
FROM monthly_sip_inflows
GROUP BY year
ORDER BY year;

---------------------------------------------------------
-- 4. Transactions by State
---------------------------------------------------------

SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM investor_transactions
GROUP BY state
ORDER BY total_transactions DESC;

---------------------------------------------------------
-- 5. Funds with Expense Ratio less than 1%
---------------------------------------------------------

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

---------------------------------------------------------
-- 6. Top 10 Funds by 5-Year Return
---------------------------------------------------------

SELECT
    scheme_name,
    return_5yr_pct
FROM scheme_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;

---------------------------------------------------------
-- 7. Average Transaction Amount by Payment Mode
---------------------------------------------------------

SELECT
    payment_mode,
    ROUND(AVG(amount_inr),2) AS average_amount
FROM investor_transactions
GROUP BY payment_mode
ORDER BY average_amount DESC;

---------------------------------------------------------
-- 8. Investor Count by KYC Status
---------------------------------------------------------

SELECT
    kyc_status,
    COUNT(*) AS investor_count
FROM investor_transactions
GROUP BY kyc_status;

---------------------------------------------------------
-- 9. Total Net Inflow by Category
---------------------------------------------------------

SELECT
    category,
    ROUND(SUM(net_inflow_crore),2) AS total_inflow
FROM category_inflows
GROUP BY category
ORDER BY total_inflow DESC;

---------------------------------------------------------
-- 10. Highest Rated Funds
---------------------------------------------------------

SELECT
    scheme_name,
    morningstar_rating,
    return_3yr_pct
FROM scheme_performance
WHERE morningstar_rating = 5
ORDER BY return_3yr_pct DESC;