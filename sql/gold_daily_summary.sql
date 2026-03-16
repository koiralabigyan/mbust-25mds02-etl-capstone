SELECT
    CURRENT_DATE() AS report_date,
    COUNT(*) AS total_transactions,
    SUM(total_sales) AS total_sales_amount,
    COUNT(DISTINCT customer_sk) AS unique_customers,
    COUNT(DISTINCT product_sk) AS unique_products
FROM GOLD.fact_sales
WHERE date_sk = CURRENT_DATE();