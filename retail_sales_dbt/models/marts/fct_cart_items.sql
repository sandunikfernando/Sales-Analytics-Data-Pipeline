-- select

--     p.cart_id,

--     p.product_id,

--     c.user_id,

--     p.quantity,

--     p.price,

--     p.total as gross_sales,

--     p.discount_percentage,

--     p.discounted_total as net_sales,

--     (p.total - p.discounted_total)
--         as discount_amount,

--     c.load_timestamp

-- from {{ ref('stg_cart_products') }} p

-- join {{ ref('stg_carts') }} c

--     on p.cart_id = c.cart_id







with products as (

    select *
    from {{ ref('stg_cart_products') }}

),

carts as (

    select *
    from {{ ref('stg_carts') }}

),

final as (

    select

        p.cart_id,

        p.product_id,

        c.user_id,

        p.quantity,

        p.price,

        p.total as gross_sales,

        p.discount_percentage,

        p.discounted_total as net_sales,

        p.total - p.discounted_total
            as discount_amount,

        case

            when p.discount_percentage < 10
                then 'Low'

            when p.discount_percentage < 20
                then 'Medium'

            else 'High'

        end as discount_band,

        c.load_timestamp

    from products p

    inner join carts c
        on p.cart_id = c.cart_id

)

select *
from final