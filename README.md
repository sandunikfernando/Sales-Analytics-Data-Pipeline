**Retail-Sales-Analytics-Data-Pipeline**

End-to-End Data Engineering Pipeline using Airflow, Snowflake, and dbt


Overview

This project demonstrates an end-to-end data engineering pipeline that automates ingestion, transformation, and analytics using modern data engineering tools.


Tech Stack
- Python
- Apache Airflow
- Snowflake
- dbt
- Docker
- SQL


Architecture

Data Source (CSV / API) 

        ↓ 

Python Ingestion Layer 

        ↓ 

Snowflake Staging Layer (Raw Data) 

        ↓ 

Airflow Orchestration Layer 

        ↓ 

dbt Transformation Layer 

        ↓ 

Analytics Data Mart 

        ↓ 

Dashboard / Reporting Layer



Project Goals
- Automate data ingestion pipeline
- Build scalable transformation layer
- Implement orchestration using Airflow
- Create analytics-ready data models


Folder Structure

Sales Analytics Data Pipeline/
│
├── dags/
├── scripts/
├── data/
│   ├── raw/
│   └── processed/
├── dbt_project/
│   ├── models/
│   └── macros/
├── docker/
├── logs/
├── tests/
├── dashboards/
├── docs/
└── README.md
