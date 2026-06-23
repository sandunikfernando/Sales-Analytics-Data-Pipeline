# FROM apache/airflow:2.9.3

# USER root

# RUN pip install astronomer-cosmos
# RUN pip install dbt-snowflake
# RUN pip install snowflake-connector-python
# RUN pip install pandas requests

# USER airflow



FROM apache/airflow:2.9.3

USER airflow

RUN pip install --no-cache-dir astronomer-cosmos
RUN pip install --no-cache-dir dbt-snowflake
RUN pip install --no-cache-dir snowflake-connector-python
RUN pip install --no-cache-dir pandas requests
RUN pip install --no-cache-dir astronomer-cosmos
RUN pip install --no-cache-dir dbt-snowflake