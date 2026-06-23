import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# Cosmos imports
from cosmos import DbtDag
from cosmos.config import ProjectConfig, ProfileConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main as ingest_main


# -------------------------------------------------------
# DEFAULT ARGS
# -------------------------------------------------------
default_args = {
    "owner": "airflow",
    "depends_on_past": False,

    "retries": 3,
    "retry_delay": timedelta(minutes=5),

    # Email alerts
    "email": ["sandunifdo28@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,

    "execution_timeout": timedelta(minutes=30)
}

# =======================================================
# 1. INGESTION DAG (RAW LAYER)
# =======================================================

with DAG(
    dag_id="retail_sales_ingestion_pipeline",
    description="Create RAW tables and ingest API data",
    start_date=datetime(2025, 1, 1),
    # schedule="@daily",
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=2,
    default_args=default_args,
    tags=["retail", "ingestion"]
) as ingestion_dag:

    create_tables_task = PythonOperator(
        task_id="create_raw_tables",
        python_callable=create_tables
    )

    ingest_data_task = PythonOperator(
        task_id="ingest_api_data",
        python_callable=ingest_main
    )

    create_tables_task >> ingest_data_task


# =======================================================
# 2. DBT DAG (STAGING + MART via COSMOS)
# =======================================================

dbt_dag = DbtDag(
    dag_id="retail_sales_dbt_pipeline",

    # project_config=ProjectConfig(
    #     "/opt/airflow/dbt"
    # ),
    project_config=ProjectConfig(
    "/opt/airflow/dbt/retail_sales_dbt"
),

    profile_config=ProfileConfig(
        profile_name="retail_sales_dbt",
        target_name="dev",
        profile_mapping=SnowflakeUserPasswordProfileMapping(
            conn_id="snowflake_default",
            profile_args={
                "database": "RETAIL_DB",
                "schema": "ANALYTICS",
                "warehouse": "COMPUTE_WH",
                "role": "ACCOUNTADMIN",
            }
        )
    ),

    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },

    operator_args={
        "install_deps": True,
    },

    # schedule="@daily",
    schedule="0 6 * * *",    
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["retail", "dbt", "cosmos"]
)