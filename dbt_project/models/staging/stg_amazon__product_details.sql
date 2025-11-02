{{ config(
    materialized='incremental',
    unique_key='asin'
) }}

with source as (
    select * from {{ source('amazon', 'product_details') }}
),
renamed as (
    select
        details_raw:product_title::varchar as product_title,
        details_raw:asin::varchar as asin,
        details_raw:product_price::varchar as product_price,
        details_raw:currency::varchar as currency,
        details_raw:product_description::varchar as description,
        details_raw:product_original_price::varchar as original_price,
        details_raw:product_star_rating::float as product_star_rating,
        details_raw:product_num_ratings::int as num_rating,
        details_raw:sales_volume::varchar as sales_volume,
        details_raw:is_amazon_choice::boolean as is_amazon_choice,
        details_raw:is_best_seller::boolean as is_best_seller,
        details_raw:rating_distribution::variant as rating_distribution,
        load_at
    from source
    {% if is_incremental() %}
    where load_at >= (select max(load_at) from {{ this }})
    {% endif %}
)
select * from renamed