select

    cast(cart_id as integer)
        as cart_id,

    cast(product_id as integer)
        as product_id,

    trim(title)
        as product_name,

    cast(price as decimal(10,2))
        as price,

    cast(quantity as integer)
        as quantity,

    cast(total as decimal(10,2))
        as total,

    coalesce(
        cast(discount_percentage as decimal(10,2)),
        0
    ) as discount_percentage,

    cast(discounted_total as decimal(10,2))
        as discounted_total,

    load_timestamp

from {{ source('raw','raw_cart_products') }}