from dotenv import load_dotenv
import os
import snowflake.connector
import logging

load_dotenv()

logger = logging.getLogger(__name__)


def create_tables():

    conn = None
    cursor = None

    try:

        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE")
        )

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RAW.RAW_CARTS (
            CART_ID INTEGER,
            USER_ID INTEGER,
            TOTAL FLOAT,
            DISCOUNTED_TOTAL FLOAT,
            TOTAL_PRODUCTS INTEGER,
            TOTAL_QUANTITY INTEGER,
            LOAD_TIMESTAMP TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RAW.RAW_CART_PRODUCTS (
            CART_ID INTEGER,
            PRODUCT_ID INTEGER,
            TITLE STRING,
            PRICE FLOAT,
            QUANTITY INTEGER,
            TOTAL FLOAT,
            DISCOUNT_PERCENTAGE FLOAT,
            DISCOUNTED_TOTAL FLOAT,
            LOAD_TIMESTAMP TIMESTAMP
        )
        """)

        logger.info("Raw tables verified successfully")

    except Exception as e:
        logger.error(f"Table creation failed: {e}")
        raise

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    create_tables()