def transform_data(data, load_timestamp):

    logger.info("Transforming data")

    cart_rows = []
    product_rows = []

    # FORCE CLEAN STRING (MOST IMPORTANT FIX)
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





# ---------------------------------------------------
# VALIDATION
# ---------------------------------------------------
def validate_schema(carts_df, products_df):

    if set(EXPECTED_CART_COLUMNS) != set(carts_df.columns):
        raise ValueError("Cart schema mismatch")

    if set(EXPECTED_PRODUCT_COLUMNS) != set(products_df.columns):
        raise ValueError("Product schema mismatch")

    logger.info("Schema validation passed")

# ---------------------------------------------------
# LOAD TO SNOWFLAKE
# ---------------------------------------------------
def load_to_snowflake(carts_df, products_df):

    conn = None

    try:
        logger.info("Connecting to Snowflake")
        conn = get_snowflake_connection()

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
            logger.info("Connection closed")

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
def main():

    logger.info("Pipeline started")

    data = extract_data()

    carts_df, products_df = transform_data(data, datetime.now(timezone.utc))

    validate_schema(carts_df, products_df)

    load_to_snowflake(carts_df, products_df)

    logger.info("Pipeline completed successfully")

# ---------------------------------------------------
# RUN
# ---------------------------------------------------
if __name__ == "__main__":
    load_timestamp = datetime.now(timezone.utc).isoformat()
    main()