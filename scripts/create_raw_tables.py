# from dotenv import load_dotenv
# import os
# import snowflake.connector

# # Load environment variables
# load_dotenv()

# # Connect to Snowflake
# conn = snowflake.connector.connect(
#     user=os.getenv("SNOWFLAKE_USER"),
#     password=os.getenv("SNOWFLAKE_PASSWORD"),
#     account=os.getenv("SNOWFLAKE_ACCOUNT"),
#     warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
#     database=os.getenv("SNOWFLAKE_DATABASE"),
#     schema=os.getenv("SNOWFLAKE_SCHEMA")
# )

# cursor = conn.cursor()

# # Create RAW_CARTS table
# cursor.execute("""
# CREATE OR REPLACE TABLE RAW.RAW_CARTS (
#     cart_id INTEGER,
#     user_id INTEGER,
#     total FLOAT,
#     discounted_total FLOAT,
#     total_products INTEGER,
#     total_quantity INTEGER,
#     load_timestamp TIMESTAMP
    
# )
# """)

# # Create RAW_CART_PRODUCTS table
# cursor.execute("""
# CREATE OR REPLACE TABLE RAW.RAW_CART_PRODUCTS (
#     cart_id INTEGER,
#     product_id INTEGER,
#     title STRING,
#     price FLOAT,
#     quantity INTEGER,
#     total FLOAT,
#     discount_percentage FLOAT,
#     discounted_total FLOAT,
#     load_timestamp TIMESTAMP
# )
# """)

# print("Tables created successfully!")

# cursor.close()
# conn.close()




from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")   # ⚠️ ADD THIS (important)
)

cursor = conn.cursor()

try:

    # -----------------------
    # DROP TABLES FIRST (IMPORTANT)
    # -----------------------
    cursor.execute("DROP TABLE IF EXISTS RAW.RAW_CARTS")
    cursor.execute("DROP TABLE IF EXISTS RAW.RAW_CART_PRODUCTS")

    # -----------------------
    # CREATE RAW_CARTS
    # -----------------------
    cursor.execute("""
        CREATE TABLE RAW.RAW_CARTS (
            CART_ID INTEGER,
            USER_ID INTEGER,
            TOTAL FLOAT,
            DISCOUNTED_TOTAL FLOAT,
            TOTAL_PRODUCTS INTEGER,
            TOTAL_QUANTITY INTEGER,
            LOAD_TIMESTAMP TIMESTAMP
        )
    """)

    # -----------------------
    # CREATE RAW_CART_PRODUCTS
    # -----------------------
    cursor.execute("""
        CREATE TABLE RAW.RAW_CART_PRODUCTS (
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

    print("✅ Tables created successfully!")

finally:
    cursor.close()
    conn.close()