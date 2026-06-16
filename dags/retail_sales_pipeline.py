import sys
sys.path.insert(0, '/opt/airflow')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main

with DAG(
    dag_id="retail_sales_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *", # Runs daily at 6:00 AM UTC
    catchup=False,
    tags=["retail", "snowflake", "sales"]
) as dag:

    create_tables_task = PythonOperator(
        task_id="create_raw_tables",
        python_callable=create_tables
    )

    ingest_raw_data_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=main
    )

    create_tables_task >> ingest_raw_data_task