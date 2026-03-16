

# Customer Data Engineering Capstone Project

**Medallion Architecture · Apache Airflow · Snowflake · Docker**
**Student:** `<Bigyan Koirala>` · **Snowflake DB:** `MBUST_25MDS02` · **Warehouse:** `COMPUTE_WH`

---

## Project Overview

This project implements an **end-to-end Customer Data ETL pipeline** using the Medallion Architecture. Data flows from raw ingestion (Bronze), through cleaning and transformation (Silver), to analytics-ready star schema (Gold). The pipeline handles **customer transactional data** and supports **SCD Type 2** for tracking customer changes over time.

**Key Features:**

* ETL pipeline: automated extraction, transformation, loading
* Medallion architecture: Bronze → Silver → Gold
* Data quality: deduplication, type casting, and validation
* SCD2 implementation: track customer attribute changes
* Daily reporting: pipeline metrics and summaries
* Fully containerized: Docker + Airflow

---

## System Architecture

```
CSV / JSON Data
      │
      ▼
Apache Airflow (Docker) ── orchestrates ETL ──▶ Snowflake
      │
      ▼
Bronze Layer (raw ingestion)
      │
      ▼
Silver Layer (cleaned & typed)
      │
      ▼
Gold Layer (analytics-ready star schema + reports)
```

**Components:**

| Component     | Technology            | Role                                        |
| ------------- | --------------------- | ------------------------------------------- |
| Data source   | CSV/JSON              | Raw customer and transaction data           |
| Orchestration | Apache Airflow        | DAG-based scheduling and task orchestration |
| Connection    | SnowflakeHook         | Secure connection to Snowflake              |
| Bronze Layer  | Snowflake VARIANT     | Raw ingestion of source files               |
| Silver Layer  | Snowflake tables      | Cleaned, typed, deduplicated staging tables |
| Gold Layer    | Snowflake Star Schema | Fact + Dimensions for analytics             |
| Failure Alert | Airflow + Gmail SMTP  | Email notifications on task failure         |

---

## Pipeline DAG

**DAG:** `customer_data_pipeline`
**Tasks flow:**

1. `extract_data` → load raw CSV/JSON
2. `load_bronze` → store raw data in Bronze tables
3. `transform_silver` → clean, typecast, deduplicate
4. `build_gold` → create star schema (Fact + Dimensions)
5. `send_daily_summary_report` → email pipeline metrics

**Engineering Standards:**

* XCom-driven modular tasks
* Idempotent by batch_date
* Retry-based self-healing (retries=2, delay=5m)
* Secrets managed via Airflow Connection (`snowflake_default`)

---

## Medallion Layers

### Bronze (RAW)

* Schema: `BRONZE.CUSTOMER_RAW`
* Raw ingestion of CSV/JSON data
* Columns: `customer_id`, `customer_name`, `email`, `signup_date`, `transaction_id`, `transaction_date`, `amount`, `ingested_at`, `batch_date`, `record_hash`

### Silver (STAGING)

* Schema: `SILVER.CUSTOMER_CLEAN`
* Cleaned, typed, deduplicated data
* Type casting, trimming, normalization
* Columns include calculated fields, e.g., `total_spent`, `days_since_signup`

### Gold (PROD / STAR SCHEMA)

* Fact Table: `GOLD.FACT_TRANSACTIONS`
* Dimensions: `GOLD.DIM_CUSTOMER` (SCD2), `GOLD.DIM_DATE`, `GOLD.DIM_PRODUCT`, `GOLD.DIM_REGION`
* SCD2 Implementation:

  * Tracked attributes: `customer_name`, `email`, `region`
  * Old rows expire (`is_current=FALSE`) and new versions inserted with `valid_from` / `valid_to`
* Daily summary table: `GOLD.DAILY_SUMMARY_REPORT`

---

## Star Schema (ER Diagram)

```
DIM_CUSTOMER ──< FACT_TRANSACTIONS >── DIM_PRODUCT
         │
         ▼
      DIM_DATE
         │
         ▼
      DIM_REGION
```

* Surrogate keys (`_SK`) used for all joins
* Natural keys (`_ID`) preserved from source data

---

## Data Dictionary (Key Tables)

**FACT_TRANSACTIONS**

| Column         | Type    | Description                     |
| -------------- | ------- | ------------------------------- |
| TRANSACTION_SK | NUMBER  | Surrogate key                   |
| TRANSACTION_ID | VARCHAR | Original transaction ID         |
| CUSTOMER_SK    | NUMBER  | FK → DIM_CUSTOMER               |
| PRODUCT_SK     | NUMBER  | FK → DIM_PRODUCT                |
| DATE_SK        | NUMBER  | FK → DIM_DATE                   |
| REGION_SK      | NUMBER  | FK → DIM_REGION                 |
| AMOUNT         | FLOAT   | Transaction amount              |
| STATUS         | VARCHAR | Completed / Pending / Cancelled |

**DIM_CUSTOMER** (SCD2)

| Column               | Type    | Description              |
| -------------------- | ------- | ------------------------ |
| CUSTOMER_SK          | NUMBER  | Surrogate PK             |
| CUSTOMER_ID          | VARCHAR | Source ID                |
| CUSTOMER_NAME        | VARCHAR | Full name                |
| EMAIL                | VARCHAR | Tracked for SCD2 changes |
| REGION               | VARCHAR | Tracked for SCD2 changes |
| EFFECTIVE_START_DATE | DATE    | Active from              |
| EFFECTIVE_END_DATE   | DATE    | Active until             |
| IS_CURRENT           | BOOLEAN | TRUE = latest version    |

Other dimensions: `DIM_PRODUCT`, `DIM_DATE`, `DIM_REGION` (Type 1 merges)

---

