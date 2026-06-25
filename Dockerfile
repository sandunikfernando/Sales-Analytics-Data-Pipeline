FROM apache/airflow:2.9.3

USER root

RUN pip install --no-cache-dir astronomer-cosmos \
    dbt-core \
    dbt-snowflake \
    snowflake-connector-python \
    pandas \
    requests \
    python-dotenv

USER airflow