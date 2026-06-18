select distinct

    product_id,

    product_name,

    price

from {{ ref('stg_cart_products') }}