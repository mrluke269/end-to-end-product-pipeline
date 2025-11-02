{{ config(
    materialized='incremental',
    unique_key='asin'
) }}


with source as(
    select * from {{ ref('stg_amazon__product_details') }}
),

cleaned as (
    select 
        asin,
        product_price::DECIMAL(10,2) as product_price,
        REPLACE(original_price, '$', '')::DECIMAL(10,2) as original_price,
        load_at
    from source
    {% if is_incremental() %}
    where load_at >= (select max(load_at) from {{ this }})
    {% endif %}
)

select * from cleaned
