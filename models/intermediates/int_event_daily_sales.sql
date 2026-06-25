WITH order_lines AS (

    SELECT *
    FROM {{ ref('stg_marketplace__ticket_order_lines') }}

)

, daily_sales AS (

    SELECT
        order_date,
        event_id,
        event_date,
        market_country_code,

        DATE_DIFF(event_date, order_date, DAY) AS days_to_event,

        SUM(
            CASE
                WHEN order_status = 'completed' THEN quantity_purchased
                ELSE 0
            END
        ) AS tickets_sold,

        SUM(
            CASE
                WHEN order_status = 'completed' THEN gross_ticket_value_usd
                ELSE 0
            END
        ) AS gross_ticket_value_usd,

        SUM(
            CASE
                WHEN order_status = 'completed' THEN buyer_fee_usd + seller_fee_usd
                ELSE 0
            END
        ) AS platform_fee_revenue_usd,

        SUM(
            CASE
                WHEN order_status = 'completed' THEN seller_payout_usd
                ELSE 0
            END
        ) AS seller_payout_usd,

        COUNT(DISTINCT CASE WHEN order_status = 'completed' THEN order_id END) AS completed_order_count,
        COUNT(DISTINCT CASE WHEN order_status = 'completed' THEN buyer_id END) AS unique_buyers,

        SAFE_DIVIDE(
            SUM(CASE WHEN order_status = 'completed' THEN gross_ticket_value_usd ELSE 0 END),
            NULLIF(SUM(CASE WHEN order_status = 'completed' THEN quantity_purchased ELSE 0 END), 0)
        ) AS avg_transaction_price_usd

    FROM order_lines

    WHERE order_date IS NOT NULL
      AND event_date IS NOT NULL

    GROUP BY 1, 2, 3, 4, 5

)

SELECT *
FROM daily_sales