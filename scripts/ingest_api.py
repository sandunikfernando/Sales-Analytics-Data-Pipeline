from datetime import datetime
from dotenv import load_dotenv
import requests
import pandas as pd
import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

# -------------------------------
# CONFIG
# -------------------------------

API_URL = "https://dummyjson.com/carts"

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

# -------------------------------
# SNOWFLAKE CONNECTION
# -------------------------------

def get_snowflake_connection():

    required_vars = [
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_ROLE"
    ]

    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        raise ValueError(f"Missing env vars: {missing}")

    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

# -------------------------------
# EXTRACT
# -------------------------------

def extract_data():

    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "carts" not in data:
        raise KeyError("Missing 'carts' key in API response")

    print("API extraction successful")
    return data

# -------------------------------
# TRANSFORM
# -------------------------------

def transform_data(data, load_timestamp):

    cart_rows = []
    product_rows = []

    for cart in data["carts"]:

        cart_rows.append({
            "cart_id": cart["id"],
            "user_id": cart["userId"],
            "total": cart["total"],
            "discounted_total": cart["discountedTotal"],
            "total_products": cart["totalProducts"],
            "total_quantity": cart["totalQuantity"],
            "load_timestamp": load_timestamp
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
                "load_timestamp": load_timestamp
            })

    carts_df = pd.DataFrame(cart_rows)
    products_df = pd.DataFrame(product_rows)

    # enforce schema consistency
    carts_df.columns = carts_df.columns.str.lower()
    products_df.columns = products_df.columns.str.lower()

    return carts_df, products_df


# -------------------------------
# VALIDATION
# -------------------------------

def validate_schema(carts_df, products_df):

    missing_cart = set(EXPECTED_CART_COLUMNS) - set(carts_df.columns)
    extra_cart = set(carts_df.columns) - set(EXPECTED_CART_COLUMNS)

    missing_prod = set(EXPECTED_PRODUCT_COLUMNS) - set(products_df.columns)
    extra_prod = set(products_df.columns) - set(EXPECTED_PRODUCT_COLUMNS)

    if missing_cart or extra_cart:
        raise ValueError(
            f"CART schema issue\nMissing: {missing_cart}\nExtra: {extra_cart}"
        )

    if missing_prod or extra_prod:
        raise ValueError(
            f"PRODUCT schema issue\nMissing: {missing_prod}\nExtra: {extra_prod}"
        )

    print("Schema validation passed")

# -------------------------------
# LOAD TO SNOWFLAKE
# -------------------------------

def load_to_snowflake(carts_df, products_df):

    conn = None

    try:
        print("🔗 Connecting to Snowflake...")
        conn = get_snowflake_connection()

        # 🔥 FIX: enforce Snowflake-compatible schema
        carts_df.columns = carts_df.columns.str.upper()
        products_df.columns = products_df.columns.str.upper()

        print("Loading RAW_CARTS...")
        success_cart, _, cart_rows, _ = write_pandas(
            conn,
            carts_df,
            table_name="RAW_CARTS",
            schema="RAW"
        )

        print("Loading RAW_CART_PRODUCTS...")
        success_products, _, product_rows, _ = write_pandas(
            conn,
            products_df,
            table_name="RAW_CART_PRODUCTS",
            schema="RAW"
        )

        print(f"RAW_CARTS loaded: {success_cart}")
        print(f"RAW_CART_PRODUCTS loaded: {success_products}")

    except Exception as e:
        print(f"Snowflake load failed: {e}")
        raise

    finally:
        if conn:
            conn.close()
            print("Connection closed")

# -------------------------------
# MAIN
# -------------------------------

def main():

    print("Starting ingestion pipeline...")

    # load_timestamp = datetime.now()
    load_timestamp = pd.to_datetime(datetime.now())

    data = extract_data()

    carts_df, products_df = transform_data(data, load_timestamp)

    validate_schema(carts_df, products_df)

    load_to_snowflake(carts_df, products_df)

    print("🎉 Ingestion completed successfully!")

# -------------------------------
# RUN
# -------------------------------

if __name__ == "__main__":
    main()