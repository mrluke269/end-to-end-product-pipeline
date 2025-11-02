{{ config(
    materialized='incremental',
    unique_key='asin'
) }}

with source as (
    select * 
    from {{ ref('stg_amazon__product_details') }}
),

flattened as (
    select 
        asin,
        rating_distribution['5']::int as star_5_pct,
        rating_distribution['4']::int as star_4_pct,
        rating_distribution['3']::int as star_3_pct,
        rating_distribution['2']::int as star_2_pct,
        rating_distribution['1']::int as star_1_pct,
        load_at
    from source
    {% if is_incremental() %}
    where load_at >= (select max(load_at) from {{ this }})
    {% endif %}
)

select * from flattened