WITH listing_snapshots AS (

    SELECT *
    FROM {{ ref('stg_marketplace__ticket_listings') }}

)

, supply_by_event_day AS (

    SELECT
        TO_HEX(MD5(CONCAT(
            COALESCE(CAST(snapshot_date AS STRING), ''),
            '|',
            COALESCE(CAST(event_id AS STRING), ''),
            '|',
            COALESCE(market_country_code, '')
        ))) AS event_market_snapshot_key,

        snapshot_date,
        event_id,
        event_date,
        market_country_code,

        ANY_VALUE(event_name) AS event_name,
        ANY_VALUE(event_category) AS event_category,

        DATE_DIFF(event_date, snapshot_date, DAY) AS days_to_event,

        COUNT(DISTINCT listing_id) AS active_listing_count,

        SUM(
            CASE
                WHEN listing_status = 'active' THEN quantity_available
                ELSE 0
            END
        ) AS tickets_available,

        AVG(
            CASE
                WHEN listing_status = 'active' AND list_price_usd > 0 THEN list_price_usd
            END
        ) AS avg_list_price_usd,

        MIN(
            CASE
                WHEN listing_status = 'active' AND list_price_usd > 0 THEN list_price_usd
            END
        ) AS min_list_price_usd,

        MAX(
            CASE
                WHEN listing_status = 'active' AND list_price_usd > 0 THEN list_price_usd
            END
        ) AS max_list_price_usd,

        AVG(
            CASE
                WHEN listing_status = 'active' AND face_value_usd > 0 THEN face_value_usd
            END
        ) AS avg_face_value_usd

    FROM listing_snapshots

    WHERE snapshot_date IS NOT NULL
      AND event_date IS NOT NULL

    GROUP BY 1, 2, 3, 4, 5, 8

)

, daily_sales AS (

    SELECT *
    FROM {{ ref('int_event_daily_sales') }}

)

, rolling_28d AS (

    SELECT
        supply.event_market_snapshot_key,

        COALESCE(SUM(sales.tickets_sold), 0) AS tickets_sold_28d,
        COALESCE(SUM(sales.gross_ticket_value_usd), 0) AS gross_ticket_value_usd_28d,
        COALESCE(SUM(sales.platform_fee_revenue_usd), 0) AS platform_fee_revenue_usd_28d,
        COALESCE(SUM(sales.seller_payout_usd), 0) AS seller_payout_usd_28d,
        COALESCE(SUM(sales.completed_order_count), 0) AS completed_order_count_28d,
        COALESCE(SUM(sales.unique_buyers), 0) AS unique_buyers_28d,

        SAFE_DIVIDE(
            COALESCE(SUM(sales.gross_ticket_value_usd), 0),
            NULLIF(COALESCE(SUM(sales.tickets_sold), 0), 0)
        ) AS avg_transaction_price_usd_28d

    FROM supply_by_event_day AS supply

    LEFT JOIN daily_sales AS sales
        ON supply.event_id = sales.event_id
       AND supply.market_country_code = sales.market_country_code
       AND sales.order_date BETWEEN DATE_SUB(supply.snapshot_date, INTERVAL 27 DAY)
                                AND supply.snapshot_date

    GROUP BY 1

)

, final AS (

    SELECT
        supply.event_market_snapshot_key,
        supply.snapshot_date,
        supply.event_id,
        supply.event_date,
        supply.event_name,
        supply.event_category,
        supply.market_country_code,
        supply.days_to_event,

        supply.active_listing_count,
        supply.tickets_available,
        supply.avg_list_price_usd,
        supply.min_list_price_usd,
        supply.max_list_price_usd,
        supply.avg_face_value_usd,

        rolling.tickets_sold_28d,
        rolling.gross_ticket_value_usd_28d,
        rolling.platform_fee_revenue_usd_28d,
        rolling.seller_payout_usd_28d,
        rolling.completed_order_count_28d,
        rolling.unique_buyers_28d,
        rolling.avg_transaction_price_usd_28d

    FROM supply_by_event_day AS supply

    LEFT JOIN rolling_28d AS rolling
        ON supply.event_market_snapshot_key = rolling.event_market_snapshot_key

)

SELECT *
FROM final