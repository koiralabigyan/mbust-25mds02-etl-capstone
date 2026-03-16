from datetime import datetime
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Default DAG arguments
default_args = {"owner": "airflow", "start_date": datetime(2026, 3, 15), "retries": 1}

with DAG(
    "sales_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for Sales data into Snowflake",
    schedule_interval="@daily",  # Change as needed
    catchup=False,
) as dag:

    # 1️⃣ Silver Layer: Clean Data
    load_sales_clean = SnowflakeOperator(
        task_id="load_sales_clean",
        snowflake_conn_id="snowflake_default",
        sql="sql/silver_sales_clean.sql",  # Your SQL file path
    )

    # 2️⃣ Silver Dedup
    dedup_sales = SnowflakeOperator(
        task_id="dedup_sales",
        snowflake_conn_id="snowflake_default",
        sql="sql/silver_sales_clean_dedup.sql",
    )

    # 3️⃣ Dim Product
    dim_product = SnowflakeOperator(
        task_id="dim_product",
        snowflake_conn_id="snowflake_default",
        sql="sql/gold_dim_product.sql",
    )

    dim_customer = SnowflakeOperator(
        task_id="dim_customer",
        snowflake_conn_id="snowflake_default",
        sql="sql/gold_dim_customer_scd2.sql",
    )

    # 5️⃣ Dim Date
    dim_date = SnowflakeOperator(
        task_id="dim_date",
        snowflake_conn_id="snowflake_default",
        sql="sql/gold_dim_date.sql",
    )

    # 6️⃣ Fact Sales
    fact_sales = SnowflakeOperator(
        task_id="fact_sales",
        snowflake_conn_id="snowflake_default",
        sql="sql/gold_fact_sales.sql",
    )

    # DAG dependencies
    load_sales_clean >> dedup_sales
    dedup_sales >> [dim_product, dim_customer, dim_date]
    [dim_product, dim_customer, dim_date] >> fact_sales
