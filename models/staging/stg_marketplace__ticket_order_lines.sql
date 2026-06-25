WITH source AS (

    SELECT *
    FROM {{ source('marketplace', 'ticket_order_lines') }}

)

, cleaned AS (

    SELECT
        TRIM(CAST(order_line_id AS STRING)) AS order_line_id,
        TRIM(CAST(order_id AS STRING)) AS order_id,
        TRIM(CAST(listing_id AS STRING)) AS listing_id,
        TRIM(CAST(event_id AS STRING)) AS event_id,
        TRIM(CAST(buyer_id AS STRING)) AS buyer_id,
        TRIM(CAST(seller_id AS STRING)) AS seller_id,

        SAFE_CAST(order_created_at AS TIMESTAMP) AS order_created_at,
        DATE(SAFE_CAST(order_created_at AS TIMESTAMP)) AS order_date,

        SAFE_CAST(event_start_at AS TIMESTAMP) AS event_start_at,
        DATE(SAFE_CAST(event_start_at AS TIMESTAMP)) AS event_date,

        LOWER(TRIM(CAST(order_status AS STRING))) AS order_status,
        LOWER(TRIM(CAST(sales_channel AS STRING))) AS sales_channel,
        UPPER(TRIM(CAST(market_country AS STRING))) AS market_country_code,

        COALESCE(SAFE_CAST(quantity_purchased AS INT64), 0) AS quantity_purchased,

        COALESCE(SAFE_CAST(gross_ticket_value_usd AS NUMERIC), 0) AS gross_ticket_value_usd,
        COALESCE(SAFE_CAST(buyer_fee_usd AS NUMERIC), 0) AS buyer_fee_usd,
        COALESCE(SAFE_CAST(seller_fee_usd AS NUMERIC), 0) AS seller_fee_usd,
        COALESCE(SAFE_CAST(discount_usd AS NUMERIC), 0) AS discount_usd,
        COALESCE(SAFE_CAST(seller_payout_usd AS NUMERIC), 0) AS seller_payout_usd,

        SAFE_CAST(_ingested_at AS TIMESTAMP) AS ingested_at

    FROM source

    WHERE order_line_id IS NOT NULL
      AND order_id IS NOT NULL
      AND event_id IS NOT NULL
      AND order_created_at IS NOT NULL

)

SELECT *
FROM cleaned