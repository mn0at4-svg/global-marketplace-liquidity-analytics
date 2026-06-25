WITH source AS (

    SELECT *
    FROM {{ source('marketplace', 'ticket_listings') }}

)

, cleaned AS (

    SELECT
        TO_HEX(MD5(CONCAT(
            COALESCE(CAST(listing_id AS STRING), ''),
            '|',
            COALESCE(CAST(snapshot_at AS STRING), '')
        ))) AS listing_snapshot_key,

        TRIM(CAST(listing_id AS STRING)) AS listing_id,
        TRIM(CAST(event_id AS STRING)) AS event_id,
        TRIM(CAST(seller_id AS STRING)) AS seller_id,

        SAFE_CAST(snapshot_at AS TIMESTAMP) AS snapshot_at,
        DATE(SAFE_CAST(snapshot_at AS TIMESTAMP)) AS snapshot_date,

        SAFE_CAST(event_start_at AS TIMESTAMP) AS event_start_at,
        DATE(SAFE_CAST(event_start_at AS TIMESTAMP)) AS event_date,

        TRIM(CAST(event_name AS STRING)) AS event_name,
        LOWER(TRIM(CAST(event_category AS STRING))) AS event_category,
        UPPER(TRIM(CAST(market_country AS STRING))) AS market_country_code,

        LOWER(TRIM(CAST(listing_status AS STRING))) AS listing_status,
        LOWER(TRIM(CAST(seller_type AS STRING))) AS seller_type,

        TRIM(CAST(section_name AS STRING)) AS section_name,
        TRIM(CAST(row_name AS STRING)) AS row_name,

        COALESCE(SAFE_CAST(quantity_listed AS INT64), 0) AS quantity_listed,
        COALESCE(SAFE_CAST(quantity_available AS INT64), 0) AS quantity_available,

        COALESCE(SAFE_CAST(list_price_usd AS NUMERIC), 0) AS list_price_usd,
        COALESCE(SAFE_CAST(face_value_usd AS NUMERIC), 0) AS face_value_usd,

        SAFE_CAST(_ingested_at AS TIMESTAMP) AS ingested_at

    FROM source

    WHERE listing_id IS NOT NULL
      AND event_id IS NOT NULL
      AND snapshot_at IS NOT NULL
      AND event_start_at IS NOT NULL

)

SELECT *
FROM cleaned