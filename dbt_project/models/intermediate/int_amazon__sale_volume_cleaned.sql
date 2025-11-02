{{ config(
    materialized='incremental',
    unique_key='asin'
) }}

with source as (
  select * from {{ ref('stg_amazon__product_details') }}
),

cleaned as (
  select 
    asin,
    lower(sales_volume) as sv,
    load_at
  from source
    {% if is_incremental() %}
    where load_at >= (select max(load_at) from {{ this }})
    {% endif %}
),
parsed as (
  select 
    asin,
    case
      when sv like '%k%' then to_number(regexp_replace(sv, '[^0-9.]', '')) * 1000
      else to_number(regexp_replace(sv, '[^0-9]', ''))
    end as sales_volume,
    load_at
  from cleaned
)
select * from parsed
