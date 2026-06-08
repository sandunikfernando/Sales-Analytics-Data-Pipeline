import requests
import pandas as pd

response = requests.get(
    "https://dummyjson.com/carts"
)

data = response.json()

cart_rows = []
product_rows = []

for cart in data["carts"]:

    cart_rows.append({
        "cart_id": cart["id"],
        "user_id": cart["userId"],
        "total": cart["total"],
        "discounted_total": cart["discountedTotal"],
        "total_products": cart["totalProducts"],
        "total_quantity": cart["totalQuantity"]
    })

    for product in cart["products"]:

        product_rows.append({
            "cart_id": cart["id"],
            "product_id": product["id"],
            "title": product["title"],
            "price": product["price"],
            "quantity": product["quantity"],
            "total": product["total"]
        })

carts_df = pd.DataFrame(cart_rows)

products_df = pd.DataFrame(product_rows)

print(carts_df.head())
print(products_df.head())