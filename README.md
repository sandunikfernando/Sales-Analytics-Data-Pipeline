# End-to-End Data Engineering Pipeline using Airflow, Snowflake, and dbt

## Project Overview

This project demonstrates a production-style end-to-end data engineering pipeline that automates data ingestion, transformation, and analytics using modern data engineering tools.

The pipeline follows a modular and scalable architecture commonly used in real-world data engineering systems.



## Tech Stack

- Python  
- Apache Airflow  
- Snowflake  
- dbt (Data Build Tool)  
- Docker  
- SQL  



## 🏗️ Architecture

<img width="996" height="481" alt="image" src="https://github.com/user-attachments/assets/d39fed04-0960-4b06-aa58-fb8339d363c0" />





## Project Objectives

- Automate end-to-end data ingestion pipeline  
- Build scalable transformation layer using dbt  
- Orchestrate workflows using Apache Airflow  
- Store data in Snowflake data warehouse  
- Create analytics-ready data models  
- Implement industry-standard project structure  



## Project Structure

Retail Sales Analytics Data Pipeline/
│
├── dags/
| ├── retail_sales_cosmos_pipeline.py
|
├── scripts/
│ ├── create_raw_tables.py
│ └── ingest_api.py
| └── test_api.py
| └── test_env.py
| └── test_snowflake.py
│
├── retail_sales_dbt/
│ ├── models/
│ │ ├── staging/
│ │ | ├── stg_cart_products.sql
| | | └──stg_carts.sql
│ │ └── marts/
│ │ | ├── dim_product.sql
| | | └── dim_user.sql
| | | └── fct_cart_items.sql
│ │ ├── schema.yml
│ │ ├── sources.yml
│ ├── profiles.yml
│ └── dbt_project.yml
│
├── docker-cmpose.yml
├── Dockerfile
├── logs/
├── dashboards/
├── docs/
| ├──raw_data_model.md
└── requirements.txt
└── README.md




