# # # from datetime import datetime
# # # import requests
# # # import pandas as pd

# # # response = requests.get(
# # #     "https://dummyjson.com/carts"
# # # )

# # # data = response.json()
# # # load_timestamp = datetime.now()

# # # cart_rows = []
# # # product_rows = []

# # # for cart in data["carts"]:

# # #     cart_rows.append({
# # #         "cart_id": cart["id"],
# # #         "user_id": cart["userId"],
# # #         "total": cart["total"],
# # #         "discounted_total": cart["discountedTotal"],
# # #         "total_products": cart["totalProducts"],
# # #         "total_quantity": cart["totalQuantity"],
# # #         "load_timestamp": load_timestamp

# # #     })

# # #     for product in cart["products"]:

# # #         product_rows.append({
# # #             "cart_id": cart["id"],
# # #             "product_id": product["id"],
# # #             "title": product["title"],
# # #             "price": product["price"],
# # #             "quantity": product["quantity"],
# # #             "total": product["total"],
# # #             "load_timestamp": load_timestamp

# # #         })

# # # carts_df = pd.DataFrame(cart_rows)
# # # products_df = pd.DataFrame(product_rows)

# # # print(carts_df.head())
# # # print(products_df.head())


# # # # Ensure Schema Matches DDL

# # # # Cart Schema
# # # EXPECTED_CART_COLUMNS = [
# # #     "cart_id",
# # #     "user_id",
# # #     "total",
# # #     "discounted_total",
# # #     "total_products",
# # #     "total_quantity",
# # #     "load_timestamp"
# # # ]
# # # # Product Schema
# # # EXPECTED_PRODUCT_COLUMNS = [
# # #     "cart_id",
# # #     "product_id",
# # #     "title",
# # #     "price",
# # #     "quantity",
# # #     "total",
# # #     "load_timestamp"
# # # ]

# # # # Validate:

# # # assert list(carts_df.columns) == EXPECTED_CART_COLUMNS
# # # assert list(products_df.columns) == EXPECTED_PRODUCT_COLUMNS

# # # print("Schema validation passed")



# # from datetime import datetime
# # import requests
# # import pandas as pd
# # import json
# # import os

# # # -------------------------------
# # # Constants
# # # -------------------------------

# # API_URL = "https://dummyjson.com/carts"

# # EXPECTED_CART_COLUMNS = [
# #     "cart_id",
# #     "user_id",
# #     "total",
# #     "discounted_total",
# #     "total_products",
# #     "total_quantity",
# #     "load_timestamp"
# # ]

# # EXPECTED_PRODUCT_COLUMNS = [
# #     "cart_id",
# #     "product_id",
# #     "title",
# #     "price",
# #     "quantity",
# #     "total",
# #     "discount_percentage",
# #     "discounted_total",
# #     "load_timestamp"
# # ]


# # # -------------------------------
# # # Extract Data
# # # -------------------------------

# # def extract_data():

# #     try:
# #         response = requests.get(
# #             API_URL,
# #             timeout=30
# #         )

# #         response.raise_for_status()

# #         data = response.json()

# #         if "carts" not in data:
# #             raise KeyError(
# #                 "'carts' key not found in API response"
# #             )

# #         print("API extraction successful")

# #         return data

# #     except requests.exceptions.Timeout:
# #         print("API request timed out")
# #         raise

# #     except requests.exceptions.HTTPError as e:
# #         print(f"HTTP Error: {e}")
# #         raise

# #     except ValueError:
# #         print("Invalid JSON response")
# #         raise

# #     except Exception as e:
# #         print(f"Unexpected Error: {e}")
# #         raise


# # # -------------------------------
# # # Save Raw JSON
# # # -------------------------------

# # def save_raw_json(data, load_timestamp):

# #     os.makedirs(
# #         "data/raw_json",
# #         exist_ok=True
# #     )

# #     filename = (
# #         f"data/raw_json/"
# #         f"carts_{load_timestamp.strftime('%Y%m%d_%H%M%S')}.json"
# #     )

# #     with open(filename, "w") as file:
# #         json.dump(
# #             data,
# #             file,
# #             indent=4
# #         )

# #     print(f"Raw JSON saved: {filename}")


# # # -------------------------------
# # # Transform Data
# # # -------------------------------

# # def transform_data(data, load_timestamp):

# #     cart_rows = []
# #     product_rows = []

# #     for cart in data["carts"]:

# #         cart_rows.append({
# #             "cart_id": cart["id"],
# #             "user_id": cart["userId"],
# #             "total": cart["total"],
# #             "discounted_total": cart["discountedTotal"],
# #             "total_products": cart["totalProducts"],
# #             "total_quantity": cart["totalQuantity"],
# #             "load_timestamp": load_timestamp
# #         })

# #         for product in cart["products"]:

# #             product_rows.append({
# #                 "cart_id": cart["id"],
# #                 "product_id": product["id"],
# #                 "title": product["title"],
# #                 "price": product["price"],
# #                 "quantity": product["quantity"],
# #                 "total": product["total"],
# #                 "discount_percentage": product["discountPercentage"],
# #                 "discounted_total": product["discountedTotal"],
# #                 "load_timestamp": load_timestamp
# #             })

# #     carts_df = pd.DataFrame(cart_rows)
# #     products_df = pd.DataFrame(product_rows)

# #     return carts_df, products_df


# # # -------------------------------
# # # Validate Schema
# # # -------------------------------

# # def validate_schema(carts_df, products_df):

# #     assert list(carts_df.columns) == EXPECTED_CART_COLUMNS, \
# #         "Cart schema does not match DDL"

# #     assert list(products_df.columns) == EXPECTED_PRODUCT_COLUMNS, \
# #         "Product schema does not match DDL"

# #     print("Schema validation passed")


# # # -------------------------------
# # # Main
# # # -------------------------------

# # def main():

# #     print("Starting ingestion process...")

# #     load_timestamp = datetime.now()

# #     data = extract_data()

# #     save_raw_json(
# #         data,
# #         load_timestamp
# #     )

# #     carts_df, products_df = transform_data(
# #         data,
# #         load_timestamp
# #     )

# #     validate_schema(
# #         carts_df,
# #         products_df
# #     )

# #     print("\nCart Data Preview:")
# #     print(carts_df.head())

# #     print("\nProduct Data Preview:")
# #     print(products_df.head())

# #     print(f"\nCart records: {len(carts_df)}")
# #     print(f"Product records: {len(products_df)}")

# #     print("\nIngestion completed successfully")


# # if __name__ == "__main__":
# #     main()



# from datetime import datetime
# import requests
# import pandas as pd
# import os
# import snowflake.connector
# from snowflake.connector.pandas_tools import write_pandas

# # -------------------------------
# # CONFIG
# # -------------------------------

# API_URL = "https://dummyjson.com/carts"

# EXPECTED_CART_COLUMNS = [
#     "cart_id",
#     "user_id",
#     "total",
#     "discounted_total",
#     "total_products",
#     "total_quantity",
#     "load_timestamp"
# ]

# EXPECTED_PRODUCT_COLUMNS = [
#     "cart_id",
#     "product_id",
#     "title",
#     "price",
#     "quantity",
#     "total",
#     "discount_percentage",
#     "discounted_total",
#     "load_timestamp"
# ]


# # -------------------------------
# # SNOWFLAKE CONNECTION
# # -------------------------------

# def get_snowflake_connection():
#     return snowflake.connector.connect(
#         user=os.getenv("SNOWFLAKE_USER"),
#         password=os.getenv("SNOWFLAKE_PASSWORD"),
#         account=os.getenv("SNOWFLAKE_ACCOUNT"),
#         warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
#         database=os.getenv("SNOWFLAKE_DATABASE"),
#         schema=os.getenv("SNOWFLAKE_SCHEMA"),
#         role=os.getenv("SNOWFLAKE_ROLE")
#     )


# # -------------------------------
# # EXTRACT
# # -------------------------------

# def extract_data():
#     try:
#         response = requests.get(API_URL, timeout=30)
#         response.raise_for_status()

#         data = response.json()

#         if "carts" not in data:
#             raise KeyError("'carts' key not found in API response")

#         print("API extraction successful")
#         return data

#     except Exception as e:
#         print(f"Extraction failed: {e}")
#         raise


# # -------------------------------
# # TRANSFORM
# # -------------------------------

# def transform_data(data, load_timestamp):

#     cart_rows = []
#     product_rows = []

#     for cart in data["carts"]:

#         cart_rows.append({
#             "cart_id": cart["id"],
#             "user_id": cart["userId"],
#             "total": cart["total"],
#             "discounted_total": cart["discountedTotal"],
#             "total_products": cart["totalProducts"],
#             "total_quantity": cart["totalQuantity"],
#             "load_timestamp": load_timestamp
#         })

#         for product in cart["products"]:

#             product_rows.append({
#                 "cart_id": cart["id"],
#                 "product_id": product["id"],
#                 "title": product["title"],
#                 "price": product["price"],
#                 "quantity": product["quantity"],
#                 "total": product["total"],
#                 "discount_percentage": product["discountPercentage"],
#                 "discounted_total": product["discountedTotal"],
#                 "load_timestamp": load_timestamp
#             })

#     carts_df = pd.DataFrame(cart_rows)
#     products_df = pd.DataFrame(product_rows)

#     return carts_df, products_df


# # -------------------------------
# # VALIDATION
# # -------------------------------

# def validate_schema(carts_df, products_df):

#     if set(carts_df.columns) != set(EXPECTED_CART_COLUMNS):
#         raise ValueError(f"Cart schema mismatch: {carts_df.columns}")

#     if set(products_df.columns) != set(EXPECTED_PRODUCT_COLUMNS):
#         raise ValueError(f"Product schema mismatch: {products_df.columns}")

#     print("Schema validation passed")


# # -------------------------------
# # LOAD TO SNOWFLAKE
# # -------------------------------

# def load_to_snowflake(carts_df, products_df):

#     conn = get_snowflake_connection()

#     try:
#         success_cart, _, _, _ = write_pandas(
#             conn,
#             carts_df,
#             table_name="RAW_CARTS",
#             schema="RAW"
#         )

#         success_products, _, _, _ = write_pandas(
#             conn,
#             products_df,
#             table_name="RAW_CART_PRODUCTS",
#             schema="RAW"
#         )

#         print(f"Carts loaded: {success_cart}")
#         print(f"Products loaded: {success_products}")

#     finally:
#         conn.close()


# # -------------------------------
# # MAIN
# # -------------------------------

# def main():

#     print("Starting ingestion pipeline...")

#     load_timestamp = datetime.now()

#     # Extract
#     data = extract_data()

#     # Transform
#     carts_df, products_df = transform_data(data, load_timestamp)

#     # Validate
#     validate_schema(carts_df, products_df)

#     # Load to Snowflake RAW layer
#     load_to_snowflake(carts_df, products_df)

#     print("\nIngestion completed successfully 🚀")


# if __name__ == "__main__":
#     main()




# from datetime import datetime
# from dotenv import load_dotenv
# import requests
# import pandas as pd
# import os
# import snowflake.connector
# from snowflake.connector.pandas_tools import write_pandas

# # -------------------------------
# # LOAD ENVIRONMENT VARIABLES
# # -------------------------------

# load_dotenv()

# # -------------------------------
# # CONFIG
# # -------------------------------

# API_URL = "https://dummyjson.com/carts"

# EXPECTED_CART_COLUMNS = [
#     "CART_ID",
#     "USER_ID",
#     "TOTAL",
#     "DISCOUNTED_TOTAL",
#     "TOTAL_PRODUCTS",
#     "TOTAL_QUANTITY",
#     "LOAD_TIMESTAMP"
# ]

# EXPECTED_PRODUCT_COLUMNS = [
#     "CART_ID",
#     "PRODUCT_ID",
#     "TITLE",
#     "PRICE",
#     "QUANTITY",
#     "TOTAL",
#     "DISCOUNTED_PERCENTAGE",
#     "DISCOUNTED_TOTAL",
#     "LOAD_TIMESTAMP"
# ]

# # -------------------------------
# # SNOWFLAKE CONNECTION
# # -------------------------------

# def get_snowflake_connection():

#     required_vars = [
#         "SNOWFLAKE_USER",
#         "SNOWFLAKE_PASSWORD",
#         "SNOWFLAKE_ACCOUNT",
#         "SNOWFLAKE_WAREHOUSE",
#         "SNOWFLAKE_DATABASE",
#         "SNOWFLAKE_SCHEMA",
#         "SNOWFLAKE_ROLE"
#     ]

#     missing_vars = [
#         var
#         for var in required_vars
#         if not os.getenv(var)
#     ]

#     if missing_vars:
#         raise ValueError(
#             f"Missing environment variables: {', '.join(missing_vars)}"
#         )

#     return snowflake.connector.connect(
#         user=os.getenv("SNOWFLAKE_USER"),
#         password=os.getenv("SNOWFLAKE_PASSWORD"),
#         account=os.getenv("SNOWFLAKE_ACCOUNT"),
#         warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
#         database=os.getenv("SNOWFLAKE_DATABASE"),
#         schema=os.getenv("SNOWFLAKE_SCHEMA"),
#         role=os.getenv("SNOWFLAKE_ROLE")
#     )

# # -------------------------------
# # EXTRACT
# # -------------------------------

# def extract_data():

#     try:

#         response = requests.get(
#             API_URL,
#             timeout=30
#         )

#         response.raise_for_status()

#         data = response.json()

#         if "carts" not in data:
#             raise KeyError(
#                 "'carts' key not found in API response"
#             )

#         print("✅ API extraction successful")

#         return data

#     except requests.exceptions.Timeout:
#         print("❌ API request timed out")
#         raise

#     except requests.exceptions.HTTPError as e:
#         print(f"❌ HTTP Error: {e}")
#         raise

#     except Exception as e:
#         print(f"❌ Extraction failed: {e}")
#         raise

# # -------------------------------
# # TRANSFORM
# # -------------------------------

# def transform_data(data, load_timestamp):

#     cart_rows = []
#     product_rows = []

#     for cart in data["carts"]:

#         cart_rows.append({
#             "CART_ID": cart["id"],
#             "USER_ID": cart["userId"],
#             "TOTAL": cart["total"],
#             "DISCOUNTED_TOTAL": cart["discountedTotal"],
#             "TOTAL_PRODUCTS": cart["totalProducts"],
#             "TOTAL_QUANTITY": cart["totalQuantity"],
#             "LOAD_TIMESTAMP": load_timestamp
#         })

#         for product in cart["products"]:

#             product_rows.append({
#                 "CART_ID": cart["id"],
#                 "PRODUCT_ID": product["id"],
#                 "TITLE": product["title"],
#                 "PRICE": product["price"],
#                 "QUANTITY": product["quantity"],
#                 "TOTAL": product["total"],
#                 "DISCOUNT_PERCENTAGE": product["discountPercentage"],
#                 "DISCOUNTED_TOTAL": product["discountedTotal"],
#                 "LOAD_TIMESTAMP": load_timestamp
#             })

#     carts_df = pd.DataFrame(cart_rows)
#     products_df = pd.DataFrame(product_rows)

#     return carts_df, products_df




# # -------------------------------
# # VALIDATE SCHEMA
# # -------------------------------

# def validate_schema(carts_df, products_df):

#     if set(carts_df.columns) != set(EXPECTED_CART_COLUMNS):
#         raise ValueError(
#             f"Cart schema mismatch.\nActual: {list(carts_df.columns)}"
#         )

#     if set(products_df.columns) != set(EXPECTED_PRODUCT_COLUMNS):
#         raise ValueError(
#             f"Product schema mismatch.\nActual: {list(products_df.columns)}"
#         )

#     print("✅ Schema validation passed")

# # -------------------------------
# # LOAD TO SNOWFLAKE
# # -------------------------------

# def load_to_snowflake(carts_df, products_df):

#     conn = None

#     try:

#         print("🔗 Connecting to Snowflake...")

#         conn = get_snowflake_connection()

#         print("📥 Loading RAW_CARTS...")

#         success_cart, _, cart_rows_loaded, _ = write_pandas(
#             conn=conn,
#             df=carts_df,
#             table_name="RAW_CARTS",
#             schema="RAW"
#         )

#         print("📥 Loading RAW_CART_PRODUCTS...")

#         success_products, _, product_rows_loaded, _ = write_pandas(
#             conn=conn,
#             df=products_df,
#             table_name="RAW_CART_PRODUCTS",
#             schema="RAW"
#         )

#         print(f"✅ RAW_CARTS loaded successfully: {success_cart}")
#         print(f"✅ RAW_CART_PRODUCTS loaded successfully: {success_products}")

#         print(f"Rows loaded into RAW_CARTS: {cart_rows_loaded}")
#         print(f"Rows loaded into RAW_CART_PRODUCTS: {product_rows_loaded}")

#     except Exception as e:

#         print(f"❌ Snowflake load failed: {e}")
#         raise

#     finally:

#         if conn:
#             conn.close()
#             print("🔒 Snowflake connection closed")

# # -------------------------------
# # MAIN
# # -------------------------------

# def main():

#     print("🚀 Starting ingestion pipeline...")

#     load_timestamp = datetime.now()

#     data = extract_data()

#     carts_df, products_df = transform_data(
#         data,
#         load_timestamp
#     )

#     validate_schema(
#         carts_df,
#         products_df
#     )

#     load_to_snowflake(
#         carts_df,
#         products_df
#     )

#     print("🎉 Ingestion completed successfully!")

# # -------------------------------
# # ENTRY POINT
# # -------------------------------

# if __name__ == "__main__":
#     main()








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

    print("✅ API extraction successful")
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

    # 🔥 enforce schema consistency
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

    print("✅ Schema validation passed")

# -------------------------------
# LOAD TO SNOWFLAKE
# -------------------------------

# def load_to_snowflake(carts_df, products_df):

#     conn = None

#     try:

#         print("🔗 Connecting to Snowflake...")
#         conn = get_snowflake_connection()

#         print("📥 Loading RAW_CARTS...")

#         success_cart, _, cart_rows, _ = write_pandas(
#             conn,
#             carts_df,
#             table_name="RAW_CARTS",
#             schema="RAW"
#         )

#         print("📥 Loading RAW_CART_PRODUCTS...")

#         success_prod, _, prod_rows, _ = write_pandas(
#             conn,
#             products_df,
#             table_name="RAW_CART_PRODUCTS",
#             schema="RAW"
#         )

#         print(f"✅ RAW_CARTS loaded: {success_cart} ({cart_rows} rows)")
#         print(f"✅ RAW_CART_PRODUCTS loaded: {success_prod} ({prod_rows} rows)")

#     except Exception as e:
#         print(f"❌ Snowflake load failed: {e}")
#         raise

#     finally:
#         if conn:
#             conn.close()
#             print("🔒 Connection closed")



def load_to_snowflake(carts_df, products_df):

    conn = None

    try:
        print("🔗 Connecting to Snowflake...")
        conn = get_snowflake_connection()

        # 🔥 FIX: enforce Snowflake-compatible schema
        carts_df.columns = carts_df.columns.str.upper()
        products_df.columns = products_df.columns.str.upper()

        print("📥 Loading RAW_CARTS...")
        success_cart, _, cart_rows, _ = write_pandas(
            conn,
            carts_df,
            table_name="RAW_CARTS",
            schema="RAW"
        )

        print("📥 Loading RAW_CART_PRODUCTS...")
        success_products, _, product_rows, _ = write_pandas(
            conn,
            products_df,
            table_name="RAW_CART_PRODUCTS",
            schema="RAW"
        )

        print(f"✅ RAW_CARTS loaded: {success_cart}")
        print(f"✅ RAW_CART_PRODUCTS loaded: {success_products}")

    except Exception as e:
        print(f"❌ Snowflake load failed: {e}")
        raise

    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed")

# -------------------------------
# MAIN
# -------------------------------

def main():

    print("🚀 Starting ingestion pipeline...")

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