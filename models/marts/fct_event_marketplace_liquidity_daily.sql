WITH base AS (

    SELECT *
    FROM {{ ref('int_event_supply_demand_28d') }}

)

, metrics AS (

    SELECT
        event_market_snapshot_key,
        snapshot_date,
        event_id,
        event_date,
        event_name,
        event_category,
        market_country_code,
        days_to_event,

        active_listing_count,
        tickets_available,

        ROUND(avg_list_price_usd, 2) AS avg_list_price_usd,
        ROUND(min_list_price_usd, 2) AS min_list_price_usd,
        ROUND(max_list_price_usd, 2) AS max_list_price_usd,
        ROUND(avg_face_value_usd, 2) AS avg_face_value_usd,

        tickets_sold_28d,
        ROUND(gross_ticket_value_usd_28d, 2) AS gross_ticket_value_usd_28d,
        ROUND(platform_fee_revenue_usd_28d, 2) AS platform_fee_revenue_usd_28d,
        ROUND(seller_payout_usd_28d, 2) AS seller_payout_usd_28d,
        completed_order_count_28d,
        unique_buyers_28d,
        ROUND(avg_transaction_price_usd_28d, 2) AS avg_transaction_price_usd_28d,

        SAFE_DIVIDE(tickets_sold_28d, 28) AS avg_daily_tickets_sold_28d,

        SAFE_DIVIDE(
            tickets_sold_28d,
            NULLIF(tickets_sold_28d + tickets_available, 0)
        ) AS sell_through_rate_28d,

        SAFE_DIVIDE(
            tickets_available,
            NULLIF(SAFE_DIVIDE(tickets_sold_28d, 28), 0)
        ) AS days_of_supply,

        SAFE_DIVIDE(
            avg_list_price_usd - avg_transaction_price_usd_28d,
            NULLIF(avg_transaction_price_usd_28d, 0)
        ) AS price_gap_vs_recent_transactions_pct,

        SAFE_DIVIDE(
            platform_fee_revenue_usd_28d,
            NULLIF(gross_ticket_value_usd_28d, 0)
        ) AS platform_take_rate_28d,

        CASE
            WHEN days_to_event <= 0 THEN 1.00
            WHEN days_to_event <= 3 THEN 0.95
            WHEN days_to_event <= 7 THEN 0.85
            WHEN days_to_event <= 14 THEN 0.65
            WHEN days_to_event <= 30 THEN 0.40
            ELSE 0.20
        END AS time_to_event_decay_factor

    FROM base

)

, decision_layer AS (

    SELECT
        *,

        ROUND(
            LEAST(
                GREATEST(
                    COALESCE(sell_through_rate_28d, 0) * 0.45
                    + COALESCE(time_to_event_decay_factor, 0) * 0.25
                    + CASE
                        WHEN tickets_available = 0 AND tickets_sold_28d > 0 THEN 0.30
                        WHEN tickets_available < tickets_sold_28d THEN 0.20
                        ELSE 0.05
                      END,
                    0
                ),
                1
            ),
            4
        ) AS demand_pressure_score,

        ROUND(
            LEAST(
                GREATEST(
                    CASE
                        WHEN tickets_available = 0 THEN 0
                        WHEN days_of_supply IS NULL THEN 0.30
                        WHEN days_of_supply > 30 THEN 0.90
                        WHEN days_of_supply > 14 THEN 0.70
                        WHEN days_of_supply > 7 THEN 0.45
                        ELSE 0.20
                    END,
                    0
                ),
                1
            ),
            4
        ) AS supply_pressure_score

    FROM metrics

)

SELECT
    event_market_snapshot_key,
    snapshot_date,
    event_id,
    event_date,
    event_name,
    event_category,
    market_country_code,
    days_to_event,

    active_listing_count,
    tickets_available,

    avg_list_price_usd,
    min_list_price_usd,
    max_list_price_usd,
    avg_face_value_usd,

    tickets_sold_28d,
    gross_ticket_value_usd_28d,
    platform_fee_revenue_usd_28d,
    seller_payout_usd_28d,
    completed_order_count_28d,
    unique_buyers_28d,
    avg_transaction_price_usd_28d,

    ROUND(avg_daily_tickets_sold_28d, 4) AS avg_daily_tickets_sold_28d,
    ROUND(sell_through_rate_28d, 4) AS sell_through_rate_28d,
    ROUND(days_of_supply, 2) AS days_of_supply,
    ROUND(price_gap_vs_recent_transactions_pct, 4) AS price_gap_vs_recent_transactions_pct,
    ROUND(platform_take_rate_28d, 4) AS platform_take_rate_28d,
    time_to_event_decay_factor,
    demand_pressure_score,
    supply_pressure_score,

    CASE
        WHEN tickets_available = 0 AND tickets_sold_28d > 0
            THEN 'supply_constrained'
        WHEN days_to_event <= 7
             AND tickets_available > tickets_sold_28d
             AND COALESCE(sell_through_rate_28d, 0) < 0.25
            THEN 'perishable_inventory_risk'
        WHEN demand_pressure_score >= 0.70
             AND supply_pressure_score <= 0.40
            THEN 'high_demand_low_supply'
        WHEN supply_pressure_score >= 0.70
             AND demand_pressure_score <= 0.40
            THEN 'oversupplied'
        ELSE 'balanced'
    END AS marketplace_liquidity_segment,

    CASE
        WHEN tickets_available = 0 AND tickets_sold_28d > 0
            THEN 'increase_supply'
        WHEN days_to_event <= 7
             AND tickets_available > tickets_sold_28d
             AND COALESCE(sell_through_rate_28d, 0) < 0.25
            THEN 'discount_to_clear'
        WHEN demand_pressure_score >= 0.70
             AND supply_pressure_score <= 0.40
            THEN 'raise_price_or_promote_seller_supply'
        WHEN supply_pressure_score >= 0.70
             AND demand_pressure_score <= 0.40
            THEN 'improve_buyer_demand_generation'
        WHEN price_gap_vs_recent_transactions_pct > 0.20
            THEN 'review_price_competitiveness'
        ELSE 'maintain'
    END AS dynamic_pricing_signal,

    CURRENT_TIMESTAMP() AS mart_generated_at

FROM decision_layer