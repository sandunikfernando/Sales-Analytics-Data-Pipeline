<!-- RAW_CARTS -->
| Column           | Type      |
| ---------------- | --------- |
| cart_id          | INTEGER   |
| user_id          | INTEGER   |
| total            | FLOAT     |
| discounted_total | FLOAT     |
| total_products   | INTEGER   |
| total_quantity   | INTEGER   |
| load_timestamp   | TIMESTAMP |


<!-- RAW_CART_PRODUCTS -->
| Column              | Type      |
| ------------------- | --------- |
| cart_id             | INTEGER   |
| product_id          | INTEGER   |
| title               | STRING    |
| price               | FLOAT     |
| quantity            | INTEGER   |
| total               | FLOAT     |
| discount_percentage | FLOAT     |
| discounted_total    | FLOAT     |
| load_timestamp      | TIMESTAMP |
