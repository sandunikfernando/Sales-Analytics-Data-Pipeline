import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main

from cosmos import DbtTaskGroup
from cosmos.config import ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

# -----------------------------------
# DEFAULT ARGS
# -----------------------------------

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# -----------------------------------
# DAG
# -----------------------------------

with DAG(
    dag_id="retail_sales_cosmos_pipeline",
    description="Retail Sales Pipeline with Cosmos + dbt",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["retail", "snowflake", "dbt", "cosmos"],
) as dag:

    # Create raw tables
    create_tables_task = PythonOperator(
        task_id="create_raw_tables",
        python_callable=create_tables
    )

    # Ingest API data
    ingest_raw_data_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=main
    )

    # dbt models
    dbt_transformations = DbtTaskGroup(
        group_id="dbt_transformations",

        project_config=ProjectConfig(
            "/opt/airflow/retail_sales_dbt"
        ),

        profile_config=ProfileConfig(
            profile_name="retail_sales_dbt",
            target_name="dev",

            profile_mapping=SnowflakeUserPasswordProfileMapping(
                conn_id="snowflake_default"
            )
        ),

        execution_config=ExecutionConfig()
    )

    create_tables_task >> ingest_raw_data_task >> dbt_transformations