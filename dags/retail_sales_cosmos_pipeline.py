import sys
import logging
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email

from scripts.create_raw_tables import create_tables
from scripts.ingest_api import main

from cosmos import DbtTaskGroup
from cosmos.config import ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping


# ALERTING
def alert_on_failure(context):
    """Custom failure alert - sends email and logs details."""
    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("logical_date") or context.get("execution_date")
    log_url = task_instance.log_url
    exception = context.get("exception")

    subject = f"[Airflow Alert] Task Failed: {dag_id}.{task_id}"
    body = f"""
    <h3>Task Failure Alert</h3>
    <p><b>DAG:</b> {dag_id}</p>
    <p><b>Task:</b> {task_id}</p>
    <p><b>Execution Date:</b> {execution_date}</p>
    <p><b>Exception:</b> {exception}</p>
    <p><b>Log URL:</b> <a href="{log_url}">{log_url}</a></p>
    """

    logging.error(f"Task failed: {dag_id}.{task_id} - {exception}")

    try:
        send_email(
            to=["sandunifdo28@gmail.com"],
            subject=subject,
            html_content=body
        )
    except Exception as e:
        logging.error(f"Failed to send alert email: {e}")



# DEFAULT ARGS
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    # "retry_delay": timedelta(minutes=5),
    "retry_delay": timedelta(seconds=30),

    # Email alerts
    "email": ["ALERT_EMAIL"],
    "email_on_failure": True,
    "email_on_retry": False,

    # Custom failure callback
    "on_failure_callback": alert_on_failure,

    "execution_timeout": timedelta(minutes=30)
}

# DAG
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

    create_tables_task = PythonOperator(
        task_id="create_raw_tables",
        python_callable=create_tables
    )

    ingest_raw_data_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=main
    )

    dbt_transformations = DbtTaskGroup(
        group_id="dbt_transformations",
        project_config=ProjectConfig("/opt/airflow/retail_sales_dbt"),
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

