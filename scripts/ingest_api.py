import os
import logging
import requests
import pandas as pd

from datetime import datetime, timezone
from dotenv import load_dotenv

import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas



# LOAD ENV VARIABLES
load_dotenv()

# LOGGER
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# EXPECTED SCHEMA
EXPECTED_CART_COLUMNS = [
    "cart_id",
    "user_id",
    "total",
    "discounted_total",
    "total_products",
    "total_quantity",
    "load_timestamp"
]

EXPECTED_PRODUCT_COLUMNS = [
    "cart_id",
    "product_id",
    "title",
    "price",
    "quantity",
    "total",
    "discount_percentage",
    "discounted_total",
    "load_timestamp"
]


# SNOWFLAKE CONNECTION
def get_snowflake_connection():

    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    role = os.getenv("SNOWFLAKE_ROLE")

   
    if not account:
        raise ValueError("SNOWFLAKE_ACCOUNT is not set in environment variables")

    return snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role
    )



# EXTRACT
def extract_data():

    API_URL = os.getenv("API_URL")

    logger.info("Extracting data from API")

    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()

    logger.info(f"Retrieved {len(data['carts'])} carts")

    return data


# TRANSFORM
def transform_data(data, load_timestamp):

    logger.info("Transforming data")

    cart_rows = []
    product_rows = []

    load_ts = str(load_timestamp)

    for cart in data["carts"]:

        cart_rows.append({
            "cart_id": cart["id"],
            "user_id": cart["userId"],
            "total": cart["total"],
            "discounted_total": cart["discountedTotal"],
            "total_products": cart["totalProducts"],
            "total_quantity": cart["totalQuantity"],
            "load_timestamp": load_ts
        })

        for product in cart["products"]:

            product_rows.append({
                "cart_id": cart["id"],
                "product_id": product["id"],
                "title": product["title"],
                "price": product["price"],
                "quantity": product["quantity"],
                "total": product["total"],
                "discount_percentage": product["discountPercentage"],
                "discounted_total": product["discountedTotal"],
                "load_timestamp": load_ts
            })

    return pd.DataFrame(cart_rows), pd.DataFrame(product_rows)


# VALIDATION
def validate_schema(carts_df, products_df):

    if set(EXPECTED_CART_COLUMNS) != set(carts_df.columns):
        raise ValueError(
            f"Cart schema mismatch. Expected: {EXPECTED_CART_COLUMNS}"
        )

    if set(EXPECTED_PRODUCT_COLUMNS) != set(products_df.columns):
        raise ValueError(
            f"Product schema mismatch. Expected: {EXPECTED_PRODUCT_COLUMNS}"
        )

    logger.info("Schema validation passed")


# LOAD TO SNOWFLAKE
def load_to_snowflake(carts_df, products_df):

    conn = None

    try:
        logger.info("Connecting to Snowflake")

        conn = get_snowflake_connection()

        # Snowflake expects uppercase columns
        carts_df.columns = carts_df.columns.str.upper()
        products_df.columns = products_df.columns.str.upper()

        logger.info("Loading RAW_CARTS")

        success1, _, rows1, _ = write_pandas(
            conn,
            carts_df,
            table_name="RAW_CARTS",
            schema="RAW"
        )

        logger.info(f"RAW_CARTS loaded: {success1}, rows={rows1}")

        logger.info("Loading RAW_CART_PRODUCTS")

        success2, _, rows2, _ = write_pandas(
            conn,
            products_df,
            table_name="RAW_CART_PRODUCTS",
            schema="RAW"
        )

        logger.info(f"RAW_CART_PRODUCTS loaded: {success2}, rows={rows2}")

    finally:
        if conn:
            conn.close()
            logger.info("Snowflake connection closed")


# MAIN
def main():

    logger.info("Pipeline started")

    data = extract_data()

    load_timestamp = datetime.now(timezone.utc)

    carts_df, products_df = transform_data(data, load_timestamp)

    validate_schema(carts_df, products_df)

    load_to_snowflake(carts_df, products_df)

    logger.info("Pipeline completed successfully")


# RUN
if __name__ == "__main__":
    main()