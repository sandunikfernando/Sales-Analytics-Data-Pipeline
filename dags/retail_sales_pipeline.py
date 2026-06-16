# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime

# from scripts.create_raw_tables import create_tables
# from scripts.ingest_api import load_raw_data

# with DAG(
#     dag_id="retail_sales_pipeline",
#     start_date=datetime(2025, 1, 1),
#     schedule="@daily",
#     catchup=False
# ) as dag:

#     create_tables_task = PythonOperator(
#         task_id="create_tables",
#         python_callable=create_tables
#     )

#     load_raw_data_task = PythonOperator(
#         task_id="ingest_raw_data",
#         python_callable=load_raw_data
#     )

#     create_tables_task >> load_raw_data_task







from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main

with DAG(
    dag_id="retail_sales_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
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