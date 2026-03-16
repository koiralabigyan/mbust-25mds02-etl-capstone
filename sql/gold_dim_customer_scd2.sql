MERGE INTO GOLD.dim_customer tgt
USING (
    SELECT DISTINCT
        CUSTOMER_NO AS customer_id,
        COUNTRY
    FROM SILVER.sales_clean_dedup
) src
ON tgt.customer_id = src.customer_id
AND tgt.is_current = TRUE

WHEN MATCHED
AND tgt.country <> src.country
THEN
UPDATE SET
    tgt.end_date = CURRENT_DATE(),
    tgt.is_current = FALSE

WHEN NOT MATCHED
THEN
INSERT (
    customer_id,
    country,
    start_date,
    end_date,
    is_current
)
VALUES (
    src.customer_id,
    src.country,
    CURRENT_DATE(),
    NULL,
    TRUE
);