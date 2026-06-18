select

    p.cart_id,

    p.product_id,

    c.user_id,

    p.quantity,

    p.price,

    p.total as gross_sales,

    p.discount_percentage,

    p.discounted_total as net_sales,

    (p.total - p.discounted_total)
        as discount_amount,

    c.load_timestamp

from {{ ref('stg_cart_products') }} p

join {{ ref('stg_carts') }} c

    on p.cart_id = c.cart_id