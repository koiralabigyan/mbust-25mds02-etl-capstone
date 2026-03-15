# ETL Capstone Project

Student Name: Bigyan Koirala  
Roll Number: 25MDS02  

## Project Overview

This project implements an end-to-end ETL pipeline using Apache Airflow and Snowflake following the Medallion Architecture (Bronze, Silver, Gold).

## Architecture

Airflow orchestrates data ingestion and transformation into Snowflake layers.

Bronze: Raw data ingestion  
Silver: Data cleaning and schema enforcement  
Gold: Star schema for analytics  

## Dataset

Retail Sales Transactions Dataset

Columns include:

TransactionNo  
Date  
ProductNo  
ProductName  
Price  
Quantity  
CustomerNo  
Country  

## Technologies Used

Apache Airflow  
Snowflake  
Python  
Pandas  
GitHub  
Snowsight Dashboard