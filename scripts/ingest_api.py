# from datetime import datetime
# import requests
# import pandas as pd

# response = requests.get(
#     "https://dummyjson.com/carts"
# )

# data = response.json()
# load_timestamp = datetime.now()

# cart_rows = []
# product_rows = []

# for cart in data["carts"]:

#     cart_rows.append({
#         "cart_id": cart["id"],
#         "user_id": cart["userId"],
#         "total": cart["total"],
#         "discounted_total": cart["discountedTotal"],
#         "total_products": cart["totalProducts"],
#         "total_quantity": cart["totalQuantity"],
#         "load_timestamp": load_timestamp

#     })

#     for product in cart["products"]:

#         product_rows.append({
#             "cart_id": cart["id"],
#             "product_id": product["id"],
#             "title": product["title"],
#             "price": product["price"],
#             "quantity": product["quantity"],
#             "total": product["total"],
#             "load_timestamp": load_timestamp

#         })

# carts_df = pd.DataFrame(cart_rows)
# products_df = pd.DataFrame(product_rows)

# print(carts_df.head())
# print(products_df.head())


# # Ensure Schema Matches DDL

# # Cart Schema
# EXPECTED_CART_COLUMNS = [
#     "cart_id",
#     "user_id",
#     "total",
#     "discounted_total",
#     "total_products",
#     "total_quantity",
#     "load_timestamp"
# ]
# # Product Schema
# EXPECTED_PRODUCT_COLUMNS = [
#     "cart_id",
#     "product_id",
#     "title",
#     "price",
#     "quantity",
#     "total",
#     "load_timestamp"
# ]

# # Validate:

# assert list(carts_df.columns) == EXPECTED_CART_COLUMNS
# assert list(products_df.columns) == EXPECTED_PRODUCT_COLUMNS

# print("Schema validation passed")



from datetime import datetime
import requests
import pandas as pd
import json
import os

# -------------------------------
# Constants
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
# Extract Data
# -------------------------------

def extract_data():

    try:
        response = requests.get(
            API_URL,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "carts" not in data:
            raise KeyError(
                "'carts' key not found in API response"
            )

        print("API extraction successful")

        return data

    except requests.exceptions.Timeout:
        print("API request timed out")
        raise

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        raise

    except ValueError:
        print("Invalid JSON response")
        raise

    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise


# -------------------------------
# Save Raw JSON
# -------------------------------

def save_raw_json(data, load_timestamp):

    os.makedirs(
        "data/raw_json",
        exist_ok=True
    )

    filename = (
        f"data/raw_json/"
        f"carts_{load_timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(filename, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"Raw JSON saved: {filename}")


# -------------------------------
# Transform Data
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

    return carts_df, products_df


# -------------------------------
# Validate Schema
# -------------------------------

def validate_schema(carts_df, products_df):

    assert list(carts_df.columns) == EXPECTED_CART_COLUMNS, \
        "Cart schema does not match DDL"

    assert list(products_df.columns) == EXPECTED_PRODUCT_COLUMNS, \
        "Product schema does not match DDL"

    print("Schema validation passed")


# -------------------------------
# Main
# -------------------------------

def main():

    print("Starting ingestion process...")

    load_timestamp = datetime.now()

    data = extract_data()

    save_raw_json(
        data,
        load_timestamp
    )

    carts_df, products_df = transform_data(
        data,
        load_timestamp
    )

    validate_schema(
        carts_df,
        products_df
    )

    print("\nCart Data Preview:")
    print(carts_df.head())

    print("\nProduct Data Preview:")
    print(products_df.head())

    print(f"\nCart records: {len(carts_df)}")
    print(f"Product records: {len(products_df)}")

    print("\nIngestion completed successfully")


if __name__ == "__main__":
    main()