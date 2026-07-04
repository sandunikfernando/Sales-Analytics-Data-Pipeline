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
dags/ — Airflow DAG definition
retail_sales_dbt/models/staging/ — Cleaning models
retail_sales_dbt/models/mart/ — Analytics models
scripts/ — Raw table DDL SQL & RAW data ingestion


## How to Run
Clone this repo
Copy .env.example to .env and fill in your Snowflake credentials
Run docker compose up
Open http://localhost:8080 (user: airflow, pass: airflow)
Toggle on retail_sales_cosmos_pipeline and trigger it



