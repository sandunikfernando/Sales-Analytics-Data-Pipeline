select

    cast(p.cart_id as integer) as cart_id,
    cast(c.user_id as integer) as user_id,
    cast(p.product_id as integer) as product_id,
    p.product_name,
    cast(p.price as decimal(10,2)) as price,
    cast(p.quantity as integer) as quantity,
    cast(p.total as decimal(10,2)) as total,

    coalesce(cast(p.discount_percentage as decimal(10,2)), 0) as discount_percentage,
    cast(p.discounted_total as decimal(10,2)) as discounted_total,

    (p.total - p.discounted_total) as discount_amount,

    case 
        when p.discount_percentage < 10 then 'Low'
        when p.discount_percentage < 20 then 'Medium'
        else 'High'
    end as discount_band,

    c.load_timestamp

from {{ ref('stg_cart_products') }} p
join {{ ref('stg_carts') }} c
    on p.cart_id = c.cart_id