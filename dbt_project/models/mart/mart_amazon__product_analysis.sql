{{config(
    materialized = 'incremental',
    unique_key = 'asin'
)}}

with 
staged as (
    select * from {{ ref('stg_amazon__product_details') }}
    {% if is_incremental() %} 
    where load_at >= (select max(load_at) from {{ this }})
    {% endif%}
),

product_price_cleaned as (
    select * from {{ ref('int_amazon__products_cleaned') }}
),

product_rating_flattened as (
    select * from {{ ref('int_amazon__product_ratings') }}
),

sales_volume_cleaned as (
    select * from {{ ref('int_amazon__sale_volume_cleaned') }}
),

joined as (
    select 
        s.product_title,
        s.asin,
        p.product_price,
        p.original_price,
        sv.sales_volume,
        s.product_star_rating,
        s.num_rating,
        s.is_amazon_choice,
        s.is_best_seller,
        r.star_1_pct,
        r.star_2_pct,
        r.star_3_pct,
        r.star_4_pct,
        r.star_5_pct,
        s.load_at
    from staged s left join product_price_cleaned p on s.asin = p.asin
    left join product_rating_flattened r on s.asin = r.asin
    left join sales_volume_cleaned sv on s.asin = sv.asin
),

metric as (
    select *,
        (star_5_pct + star_4_pct) as positive_percentage,
        100*((original_price - product_price)/nullif(original_price,0)) as discount_percentage,
        case
            when (num_rating < 20000) and (positive_percentage > 80) and (discount_percentage > 30.0) then 'Opportunity Product'
            else 'High Supplied Product'
        end as product_classfify
    from joined
)

select * from metric