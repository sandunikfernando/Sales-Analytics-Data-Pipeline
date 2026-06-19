select

    cast(cart_id as integer) as cart_id,
    cast(user_id as integer) as user_id,
    cast(total as decimal(10,2)) as total,
    cast(discounted_total as decimal(10,2)) as discounted_total,
    cast(total_products as integer) as total_products,
    cast(total_quantity as integer) as total_quantity,

    load_timestamp as load_timestamp

from {{ source('raw','raw_carts') }}