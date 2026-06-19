# import sys
# sys.path.insert(0, '/opt/airflow')

# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime

# from scripts.create_raw_tables import create_tables
# from scripts.ingest_api import main

# with DAG(
#     dag_id="retail_sales_pipeline",
#     start_date=datetime(2025, 1, 1),
#     schedule="0 6 * * *", # Runs daily at 6:00 AM UTC
#     catchup=False,
#     tags=["retail", "snowflake", "sales"]
# ) as dag:

#     create_tables_task = PythonOperator(
#         task_id="create_raw_tables",
#         python_callable=create_tables
#     )

#     ingest_raw_data_task = PythonOperator(
#         task_id="ingest_raw_data",
#         python_callable=main
#     )

#     create_tables_task >> ingest_raw_data_task




import sys
from datetime import datetime, timedelta

# Make scripts package available inside Airflow container
sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main

# -------------------------------------------------------
# DEFAULT ARGUMENTS
# -------------------------------------------------------

default_args = {
    "owner": "airflow",
    "depends_on_past": False,

    # Retry settings
    "retries": 3,
    "retry_delay": timedelta(minutes=5),

    # Notifications
    "email_on_failure": False,
    "email_on_retry": False,

    # Task execution timeout
    "execution_timeout": timedelta(minutes=30)
}

# -------------------------------------------------------
# DAG
# -------------------------------------------------------

with DAG(
    dag_id="retail_sales_pipeline",

    description="End-to-End Retail Sales Analytics Pipeline",

    start_date=datetime(2025, 1, 1),

    # Runs every day at 6 AM UTC
    schedule="0 6 * * *",

    catchup=False,

    max_active_runs=1,

    default_args=default_args,

    tags=["retail", "snowflake", "dbt", "analytics"]

) as dag:

    # ---------------------------------------------------
    # CREATE RAW TABLES
    # ---------------------------------------------------

    create_tables_task = PythonOperator(
        task_id="create_raw_tables",
        python_callable=create_tables
    )

    # ---------------------------------------------------
    # INGEST API DATA
    # ---------------------------------------------------

    ingest_raw_data_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=main
    )

    # ---------------------------------------------------
    # TASK DEPENDENCIES
    # ---------------------------------------------------

    create_tables_task >> ingest_raw_data_task