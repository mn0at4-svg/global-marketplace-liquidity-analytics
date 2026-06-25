import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# App Configuration
# ============================================================

st.set_page_config(
    page_title="Enterprise Marketplace Liquidity Cockpit",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "Enterprise Marketplace Liquidity Cockpit"
APP_SUBTITLE = (
    "Executive simulation layer for a global two-sided live event marketplace "
    "with high-velocity, perishable inventory."
)

DEFAULT_TABLE_FQN = os.getenv(
    "MARKETPLACE_MART_FQN",
    "your_project.your_dataset.fct_event_marketplace_liquidity_daily",
)


# ============================================================
# Design System
# ============================================================

st.markdown(
    """
<style>
    :root {
        --bg-primary: #080B12;
        --bg-secondary: #111827;
        --card-bg: rgba(17, 24, 39, 0.78);
        --card-border: rgba(255, 255, 255, 0.10);
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --accent: #8B5CF6;
        --accent-2: #22D3EE;
        --good: #34D399;
        --warn: #FBBF24;
        --bad: #FB7185;
        --shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
    }

    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                     "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(139, 92, 246, 0.22), transparent 34%),
            radial-gradient(circle at top right, rgba(34, 211, 238, 0.14), transparent 30%),
            linear-gradient(135deg, #070A12 0%, #0B1020 45%, #111827 100%);
        color: var(--text-primary);
    }

    section[data-testid="stSidebar"] {
        background: rgba(8, 11, 18, 0.86);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .hero {
        padding: 30px 34px;
        border: 1px solid var(--card-border);
        border-radius: 26px;
        background:
            linear-gradient(135deg, rgba(139,92,246,0.18), rgba(34,211,238,0.08)),
            rgba(15, 23, 42, 0.70);
        box-shadow: var(--shadow);
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 42px;
        line-height: 1.05;
        letter-spacing: -0.04em;
        margin: 0 0 10px 0;
        color: #FFFFFF;
    }

    .hero p {
        font-size: 16px;
        color: var(--text-secondary);
        margin: 0;
        max-width: 980px;
    }

    .pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 18px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.06);
        color: #E5E7EB;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .metric-card {
        padding: 20px 20px 18px 20px;
        border-radius: 22px;
        border: 1px solid var(--card-border);
        background: var(--card-bg);
        box-shadow: var(--shadow);
        min-height: 132px;
    }

    .metric-label {
        font-size: 12px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 30px;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #FFFFFF;
    }

    .metric-note {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 8px;
    }

    .section-card {
        padding: 24px;
        border-radius: 24px;
        border: 1px solid var(--card-border);
        background: rgba(15, 23, 42, 0.74);
        box-shadow: var(--shadow);
        margin-top: 14px;
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .section-caption {
        color: var(--text-muted);
        font-size: 13px;
        margin-bottom: 14px;
    }

    .status-good {
        color: var(--good);
        font-weight: 800;
    }

    .status-warn {
        color: var(--warn);
        font-weight: 800;
    }

    .status-bad {
        color: var(--bad);
        font-weight: 800;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF;
    }

    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
    }

    footer {
        visibility: hidden;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# Utility Functions
# ============================================================

def format_number(value, decimals=0):
    if pd.isna(value):
        return "—"
    try:
        value = float(value)
    except Exception:
        return str(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{decimals}f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    return f"{value:.{decimals}f}"


def format_currency(value, decimals=1):
    if pd.isna(value):
        return "—"
    return f"${format_number(value, decimals)}"


def safe_divide(numerator, denominator):
    denominator = denominator.replace(0, np.nan) if isinstance(denominator, pd.Series) else denominator
    return numerator / denominator


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, caption=""):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-caption">{caption}</div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Data Loading
# ============================================================

@st.cache_data(show_spinner=False)
def generate_sample_data(n_events=260, seed=7):
    rng = np.random.default_rng(seed)

    today = pd.Timestamp.today().normalize()
    categories = ["sports", "music", "theater", "festival", "comedy"]
    countries = ["US", "GB", "DE", "FR", "CA", "AU", "JP"]
    segments = [
        "supply_constrained",
        "perishable_inventory_risk",
        "high_demand_low_supply",
        "oversupplied",
        "balanced",
    ]

    rows = []
    for i in range(n_events):
        event_id = f"EVT-{100000 + i}"
        days_to_event = int(rng.integers(1, 90))
        event_date = today + pd.Timedelta(days=days_to_event)
        category = rng.choice(categories, p=[0.36, 0.32, 0.12, 0.12, 0.08])
        country = rng.choice(countries)

        tickets_available = int(max(0, rng.normal(850, 520)))
        tickets_sold_28d = int(max(0, rng.normal(450, 330)))

        if days_to_event <= 7:
            tickets_sold_28d = int(tickets_sold_28d * rng.uniform(1.15, 2.0))

        avg_list_price = float(max(18, rng.normal(145, 75)))
        avg_transaction_price = float(avg_list_price * rng.uniform(0.75, 1.18))

        gross_28d = tickets_sold_28d * avg_transaction_price
        take_rate = float(rng.uniform(0.10, 0.19))
        fee_revenue = gross_28d * take_rate

        sell_through = tickets_sold_28d / max(tickets_sold_28d + tickets_available, 1)
        avg_daily = tickets_sold_28d / 28
        days_of_supply = tickets_available / avg_daily if avg_daily > 0 else np.nan

        if tickets_available == 0 and tickets_sold_28d > 0:
            segment = "supply_constrained"
            signal = "increase_supply"
        elif days_to_event <= 7 and tickets_available > tickets_sold_28d and sell_through < 0.25:
            segment = "perishable_inventory_risk"
            signal = "discount_to_clear"
        elif sell_through >= 0.70 and tickets_available < tickets_sold_28d:
            segment = "high_demand_low_supply"
            signal = "raise_price_or_promote_seller_supply"
        elif tickets_available > tickets_sold_28d * 3:
            segment = "oversupplied"
            signal = "improve_buyer_demand_generation"
        else:
            segment = "balanced"
            signal = "maintain"

        time_decay = (
            1.00 if days_to_event <= 0 else
            0.95 if days_to_event <= 3 else
            0.85 if days_to_event <= 7 else
            0.65 if days_to_event <= 14 else
            0.40 if days_to_event <= 30 else
            0.20
        )

        demand_pressure = min(
            max(sell_through * 0.45 + time_decay * 0.25 + rng.uniform(0.03, 0.25), 0),
            1,
        )

        supply_pressure = min(
            max(
                0.85 if tickets_available > tickets_sold_28d * 3
                else 0.55 if tickets_available > tickets_sold_28d
                else 0.25,
                0,
            ),
            1,
        )

        rows.append(
            {
                "event_market_snapshot_key": f"KEY-{i}",
                "snapshot_date": today,
                "event_id": event_id,
                "event_date": event_date,
                "event_name": f"{category.title()} Event {i + 1}",
                "event_category": category,
                "market_country_code": country,
                "days_to_event": days_to_event,
                "active_listing_count": int(max(1, tickets_available / rng.uniform(1.5, 4.5))),
                "tickets_available": tickets_available,
                "avg_list_price_usd": avg_list_price,
                "min_list_price_usd": avg_list_price * rng.uniform(0.55, 0.88),
                "max_list_price_usd": avg_list_price * rng.uniform(1.2, 2.6),
                "avg_face_value_usd": avg_list_price * rng.uniform(0.45, 0.95),
                "tickets_sold_28d": tickets_sold_28d,
                "gross_ticket_value_usd_28d": gross_28d,
                "platform_fee_revenue_usd_28d": fee_revenue,
                "seller_payout_usd_28d": gross_28d - fee_revenue,
                "completed_order_count_28d": int(max(0, tickets_sold_28d / rng.uniform(1.2, 2.6))),
                "unique_buyers_28d": int(max(0, tickets_sold_28d / rng.uniform(1.0, 2.1))),
                "avg_transaction_price_usd_28d": avg_transaction_price,
                "avg_daily_tickets_sold_28d": avg_daily,
                "sell_through_rate_28d": sell_through,
                "days_of_supply": days_of_supply,
                "price_gap_vs_recent_transactions_pct": (
                    (avg_list_price - avg_transaction_price) / avg_transaction_price
                    if avg_transaction_price else np.nan
                ),
                "platform_take_rate_28d": take_rate,
                "time_to_event_decay_factor": time_decay,
                "demand_pressure_score": demand_pressure,
                "supply_pressure_score": supply_pressure,
                "marketplace_liquidity_segment": segment,
                "dynamic_pricing_signal": signal,
                "mart_generated_at": pd.Timestamp.now(),
            }
        )

    return pd.DataFrame(rows)


@st.cache_data(show_spinner=True)
def load_bigquery_data(table_fqn, custom_sql=None):
    try:
        from google.cloud import bigquery
    except ImportError as exc:
        raise ImportError(
            "google-cloud-bigquery is not installed. Add it to requirements.txt."
        ) from exc

    client = bigquery.Client()

    if custom_sql and custom_sql.strip():
        sql = custom_sql
    else:
        sql = f"""
        SELECT *
        FROM `{table_fqn}`
        """

    return client.query(sql).to_dataframe()


def normalize_data(df):
    df = df.copy()

    date_cols = ["snapshot_date", "event_date", "mart_generated_at"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    numeric_cols = [
        "days_to_event",
        "active_listing_count",
        "tickets_available",
        "avg_list_price_usd",
        "min_list_price_usd",
        "max_list_price_usd",
        "avg_face_value_usd",
        "tickets_sold_28d",
        "gross_ticket_value_usd_28d",
        "platform_fee_revenue_usd_28d",
        "seller_payout_usd_28d",
        "completed_order_count_28d",
        "unique_buyers_28d",
        "avg_transaction_price_usd_28d",
        "avg_daily_tickets_sold_28d",
        "sell_through_rate_28d",
        "days_of_supply",
        "price_gap_vs_recent_transactions_pct",
        "platform_take_rate_28d",
        "time_to_event_decay_factor",
        "demand_pressure_score",
        "supply_pressure_score",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required_defaults = {
        "event_name": "Unknown Event",
        "event_category": "unknown",
        "market_country_code": "UNKNOWN",
        "marketplace_liquidity_segment": "unknown",
        "dynamic_pricing_signal": "maintain",
    }

    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default
        df[col] = df[col].fillna(default)

    return df


def validate_required_columns(df):
    required_cols = [
        "event_market_snapshot_key",
        "snapshot_date",
        "event_id",
        "event_date",
        "event_name",
        "event_category",
        "market_country_code",
        "days_to_event",
        "tickets_available",
        "avg_list_price_usd",
        "tickets_sold_28d",
        "platform_fee_revenue_usd_28d",
        "avg_transaction_price_usd_28d",
        "sell_through_rate_28d",
        "days_of_supply",
        "platform_take_rate_28d",
        "demand_pressure_score",
        "supply_pressure_score",
        "marketplace_liquidity_segment",
        "dynamic_pricing_signal",
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        st.error(
            "The loaded mart is missing required columns. "
            "Please confirm that your dbt mart is `fct_event_marketplace_liquidity_daily`."
        )
        st.code("\n".join(missing))
        st.stop()


# ============================================================
# Simulation Logic
# ============================================================

def apply_pricing_simulation(
    df,
    price_adjustment_pct,
    demand_elasticity,
    marketing_lift_pct,
    seller_supply_uplift_pct,
    take_rate_override_pct,
):
    sim = df.copy()

    price_change = price_adjustment_pct / 100
    marketing_lift = marketing_lift_pct / 100
    supply_uplift = seller_supply_uplift_pct / 100

    base_price = sim["avg_list_price_usd"].fillna(sim["avg_transaction_price_usd_28d"]).fillna(0)
    base_available = sim["tickets_available"].fillna(0)
    base_daily_demand = sim["avg_daily_tickets_sold_28d"].fillna(
        sim["tickets_sold_28d"].fillna(0) / 28
    )

    days_window = sim["days_to_event"].fillna(0).clip(lower=0, upper=28)

    demand_multiplier = 1 + marketing_lift + (demand_elasticity * price_change)
    demand_multiplier = max(demand_multiplier, 0)

    sim["simulated_avg_price_usd"] = base_price * (1 + price_change)
    sim["simulated_ticket_supply"] = base_available * (1 + supply_uplift)

    sim["projected_demand_until_event"] = base_daily_demand * days_window * demand_multiplier

    sim["projected_units_sold_until_event"] = np.minimum(
        sim["projected_demand_until_event"],
        sim["simulated_ticket_supply"],
    )

    sim["projected_unsold_tickets_at_event"] = (
        sim["simulated_ticket_supply"] - sim["projected_units_sold_until_event"]
    ).clip(lower=0)

    sim["simulated_sell_through_rate"] = safe_divide(
        sim["projected_units_sold_until_event"],
        sim["simulated_ticket_supply"],
    ).fillna(0)

    if take_rate_override_pct is not None:
        take_rate = take_rate_override_pct / 100
    else:
        take_rate = sim["platform_take_rate_28d"].fillna(0.14)

    sim["simulated_gross_ticket_value_usd"] = (
        sim["projected_units_sold_until_event"] * sim["simulated_avg_price_usd"]
    )

    sim["simulated_platform_fee_revenue_usd"] = (
        sim["simulated_gross_ticket_value_usd"] * take_rate
    )

    baseline_future_units = np.minimum(
        base_daily_demand * days_window,
        base_available,
    )

    sim["baseline_projected_platform_fee_revenue_usd"] = (
        baseline_future_units
        * base_price
        * sim["platform_take_rate_28d"].fillna(0.14)
    )

    sim["incremental_platform_fee_revenue_usd"] = (
        sim["simulated_platform_fee_revenue_usd"]
        - sim["baseline_projected_platform_fee_revenue_usd"]
    )

    sim["simulated_price_gap_vs_recent_txn_pct"] = safe_divide(
        sim["simulated_avg_price_usd"] - sim["avg_transaction_price_usd_28d"],
        sim["avg_transaction_price_usd_28d"],
    )

    conditions = [
        (sim["simulated_ticket_supply"] <= 0) & (sim["projected_demand_until_event"] > 0),
        (sim["days_to_event"] <= 7)
        & (sim["projected_unsold_tickets_at_event"] > 0)
        & (sim["simulated_sell_through_rate"] < 0.35),
        (sim["simulated_sell_through_rate"] >= 0.75)
        & (sim["simulated_ticket_supply"] <= sim["projected_demand_until_event"] * 1.15),
        (sim["projected_unsold_tickets_at_event"] > sim["projected_units_sold_until_event"] * 1.5),
    ]

    segment_values = [
        "supply_constrained",
        "perishable_inventory_risk",
        "high_demand_low_supply",
        "oversupplied",
    ]

    sim["simulated_liquidity_segment"] = np.select(
        conditions,
        segment_values,
        default="balanced",
    )

    action_conditions = [
        sim["simulated_liquidity_segment"].eq("supply_constrained"),
        sim["simulated_liquidity_segment"].eq("perishable_inventory_risk"),
        sim["simulated_liquidity_segment"].eq("high_demand_low_supply"),
        sim["simulated_liquidity_segment"].eq("oversupplied"),
        sim["simulated_price_gap_vs_recent_txn_pct"].fillna(0) > 0.20,
    ]

    action_values = [
        "increase_supply",
        "discount_to_clear",
        "raise_price_or_promote_seller_supply",
        "improve_buyer_demand_generation",
        "review_price_competitiveness",
    ]

    sim["simulated_dynamic_pricing_signal"] = np.select(
        action_conditions,
        action_values,
        default="maintain",
    )

    return sim


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown("## Data Source")

    data_source = st.radio(
        "Choose input mode",
        ["Demo sample", "CSV upload", "BigQuery mart"],
        index=0,
    )

    uploaded_csv = None
    table_fqn = DEFAULT_TABLE_FQN
    custom_sql = ""

    if data_source == "CSV upload":
        uploaded_csv = st.file_uploader(
            "Upload exported mart CSV",
            type=["csv"],
            help="Upload a CSV exported from fct_event_marketplace_liquidity_daily.",
        )

    if data_source == "BigQuery mart":
        table_fqn = st.text_input(
            "BigQuery table FQN",
            value=DEFAULT_TABLE_FQN,
            help="Example: project.dataset.fct_event_marketplace_liquidity_daily",
        )

        with st.expander("Optional SQL override"):
            custom_sql = st.text_area(
                "Custom SQL",
                value="",
                height=140,
                placeholder="SELECT * FROM `project.dataset.fct_event_marketplace_liquidity_daily`",
            )

    st.markdown("---")
    st.markdown("## Executive Filters")


# ============================================================
# Load Data
# ============================================================

try:
    if data_source == "Demo sample":
        raw_df = generate_sample_data()
        source_label = "Demo sample generated in-memory"

    elif data_source == "CSV upload":
        if uploaded_csv is None:
            st.info("Upload a CSV, or switch to Demo sample mode.")
            st.stop()
        raw_df = pd.read_csv(uploaded_csv)
        source_label = "Uploaded CSV"

    else:
        raw_df = load_bigquery_data(table_fqn=table_fqn, custom_sql=custom_sql)
        source_label = f"BigQuery mart: {table_fqn}"

except Exception as exc:
    st.error("Could not load data.")
    st.exception(exc)
    st.stop()

df = normalize_data(raw_df)
validate_required_columns(df)


# ============================================================
# Sidebar Filters
# ============================================================

with st.sidebar:
    category_options = sorted(df["event_category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Event category",
        options=category_options,
        default=category_options,
    )

    country_options = sorted(df["market_country_code"].dropna().unique().tolist())
    selected_countries = st.multiselect(
        "Market",
        options=country_options,
        default=country_options,
    )

    segment_options = sorted(df["marketplace_liquidity_segment"].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Liquidity segment",
        options=segment_options,
        default=segment_options,
    )

    min_days = int(np.nanmin(df["days_to_event"])) if len(df) else 0
    max_days = int(np.nanmax(df["days_to_event"])) if len(df) else 90

    days_range = st.slider(
        "Days to event",
        min_value=max(0, min_days),
        max_value=max(max_days, 1),
        value=(max(0, min_days), max(max_days, 1)),
    )

    search_term = st.text_input("Search event name", value="")

filtered = df[
    df["event_category"].isin(selected_categories)
    & df["market_country_code"].isin(selected_countries)
    & df["marketplace_liquidity_segment"].isin(selected_segments)
    & df["days_to_event"].between(days_range[0], days_range[1])
].copy()

if search_term.strip():
    filtered = filtered[
        filtered["event_name"].str.contains(search_term.strip(), case=False, na=False)
    ]


# ============================================================
# Hero
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
        <div class="pill-row">
            <div class="pill">Two-Sided Marketplace</div>
            <div class="pill">Perishable Inventory</div>
            <div class="pill">Dynamic Pricing</div>
            <div class="pill">AI-Ready Decision Mart</div>
            <div class="pill">Source: {source_label}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI Overview
# ============================================================

total_events = filtered["event_id"].nunique()
total_available = filtered["tickets_available"].sum()
total_sold_28d = filtered["tickets_sold_28d"].sum()
total_fee_revenue = filtered["platform_fee_revenue_usd_28d"].sum()
avg_sell_through = filtered["sell_through_rate_28d"].mean()
risk_count = filtered[
    filtered["marketplace_liquidity_segment"].isin(
        ["perishable_inventory_risk", "supply_constrained", "oversupplied"]
    )
]["event_id"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    metric_card(
        "Active Events",
        format_number(total_events, 0),
        "Filtered event universe",
    )

with k2:
    metric_card(
        "Tickets Available",
        format_number(total_available, 0),
        "Remaining marketplace supply",
    )

with k3:
    metric_card(
        "Tickets Sold 28D",
        format_number(total_sold_28d, 0),
        "Trailing demand signal",
    )

with k4:
    metric_card(
        "Fee Revenue 28D",
        format_currency(total_fee_revenue, 1),
        "Platform monetization",
    )

with k5:
    metric_card(
        "Avg Sell-through",
        f"{avg_sell_through:.1%}" if pd.notna(avg_sell_through) else "—",
        f"{risk_count} events need attention",
    )


# ============================================================
# Main Tabs
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Executive Cockpit",
        "Pricing Simulator",
        "Event Drilldown",
        "Governance & Data Quality",
    ]
)


# ============================================================
# Tab 1: Executive Cockpit
# ============================================================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Marketplace Health",
        "Portfolio view of liquidity risk, perishable inventory, and pricing pressure.",
    )

    c1, c2 = st.columns([1.2, 1])

    with c1:
        if len(filtered):
            fig = px.scatter(
                filtered,
                x="days_to_event",
                y="sell_through_rate_28d",
                size="tickets_available",
                color="marketplace_liquidity_segment",
                hover_name="event_name",
                hover_data={
                    "market_country_code": True,
                    "event_category": True,
                    "tickets_available": ":,.0f",
                    "tickets_sold_28d": ":,.0f",
                    "avg_list_price_usd": ":$,.2f",
                    "platform_fee_revenue_usd_28d": ":$,.0f",
                    "days_to_event": True,
                    "sell_through_rate_28d": ":.1%",
                },
                title="Sell-through vs. Days to Event",
                labels={
                    "days_to_event": "Days to Event",
                    "sell_through_rate_28d": "Sell-through Rate 28D",
                    "marketplace_liquidity_segment": "Liquidity Segment",
                    "tickets_available": "Available Tickets",
                },
            )

            fig.update_layout(
                template="plotly_dark",
                height=460,
                margin=dict(l=10, r=10, t=55, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend_title_text="Segment",
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data after filters.")

    with c2:
        segment_summary = (
            filtered.groupby("marketplace_liquidity_segment", dropna=False)
            .agg(
                events=("event_id", "nunique"),
                tickets_available=("tickets_available", "sum"),
                fee_revenue_28d=("platform_fee_revenue_usd_28d", "sum"),
            )
            .reset_index()
            .sort_values("events", ascending=False)
        )

        fig_bar = px.bar(
            segment_summary,
            x="events",
            y="marketplace_liquidity_segment",
            orientation="h",
            text="events",
            title="Event Count by Liquidity Segment",
            labels={
                "events": "Events",
                "marketplace_liquidity_segment": "Segment",
            },
        )

        fig_bar.update_layout(
            template="plotly_dark",
            height=460,
            margin=dict(l=10, r=10, t=55, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(categoryorder="total ascending"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Executive Action Queue",
        "Events ranked by urgency, revenue exposure, and liquidity imbalance.",
    )

    action_queue = filtered.copy()
    action_queue["urgency_score"] = (
        (1 - action_queue["days_to_event"].clip(lower=0, upper=90) / 90) * 0.35
        + action_queue["demand_pressure_score"].fillna(0) * 0.35
        + action_queue["supply_pressure_score"].fillna(0) * 0.30
    )

    action_queue = action_queue.sort_values(
        ["urgency_score", "platform_fee_revenue_usd_28d"],
        ascending=[False, False],
    )

    display_cols = [
        "event_name",
        "event_category",
        "market_country_code",
        "days_to_event",
        "tickets_available",
        "tickets_sold_28d",
        "sell_through_rate_28d",
        "days_of_supply",
        "platform_fee_revenue_usd_28d",
        "marketplace_liquidity_segment",
        "dynamic_pricing_signal",
    ]

    st.dataframe(
        action_queue[display_cols].head(30),
        use_container_width=True,
        hide_index=True,
        column_config={
            "platform_fee_revenue_usd_28d": st.column_config.NumberColumn(
                "Fee Revenue 28D",
                format="$%.0f",
            ),
            "sell_through_rate_28d": st.column_config.ProgressColumn(
                "Sell-through",
                format="%.1f%%",
                min_value=0,
                max_value=1,
            ),
            "days_of_supply": st.column_config.NumberColumn(
                "Days of Supply",
                format="%.1f",
            ),
        },
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Tab 2: Pricing Simulator
# ============================================================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Dynamic Pricing Scenario Simulator",
        "Model how price, demand elasticity, seller supply, and marketing lift affect projected fee revenue and clearance risk.",
    )

    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        price_adjustment_pct = st.slider(
            "Price adjustment",
            min_value=-50,
            max_value=50,
            value=-8,
            step=1,
            help="Negative values simulate discounting. Positive values simulate price increases.",
        )

    with s2:
        demand_elasticity = st.slider(
            "Demand elasticity",
            min_value=-3.0,
            max_value=0.0,
            value=-1.2,
            step=0.1,
            help="If price decreases by 10%, elasticity -1.2 implies demand rises by roughly 12%.",
        )

    with s3:
        marketing_lift_pct = st.slider(
            "Marketing demand lift",
            min_value=0,
            max_value=100,
            value=10,
            step=5,
        )

    with s4:
        seller_supply_uplift_pct = st.slider(
            "Seller supply uplift",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
        )

    with s5:
        take_rate_override_pct = st.slider(
            "Take-rate override",
            min_value=5,
            max_value=30,
            value=14,
            step=1,
        )

    simulated = apply_pricing_simulation(
        filtered,
        price_adjustment_pct=price_adjustment_pct,
        demand_elasticity=demand_elasticity,
        marketing_lift_pct=marketing_lift_pct,
        seller_supply_uplift_pct=seller_supply_uplift_pct,
        take_rate_override_pct=take_rate_override_pct,
    )

    base_revenue = simulated["baseline_projected_platform_fee_revenue_usd"].sum()
    sim_revenue = simulated["simulated_platform_fee_revenue_usd"].sum()
    incremental_revenue = simulated["incremental_platform_fee_revenue_usd"].sum()
    projected_units = simulated["projected_units_sold_until_event"].sum()
    projected_unsold = simulated["projected_unsold_tickets_at_event"].sum()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Baseline Projected Fee Revenue",
            format_currency(base_revenue, 1),
            "Expected without scenario changes",
        )

    with c2:
        metric_card(
            "Simulated Fee Revenue",
            format_currency(sim_revenue, 1),
            "Scenario-adjusted outcome",
        )

    with c3:
        delta_note = "Incremental vs. baseline"
        metric_card(
            "Revenue Impact",
            format_currency(incremental_revenue, 1),
            delta_note,
        )

    with c4:
        metric_card(
            "Projected Unsold Tickets",
            format_number(projected_unsold, 0),
            f"{format_number(projected_units, 0)} projected tickets sold",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Scenario Impact by Event",
        "Prioritized list of where the simulation creates or destroys economic value.",
    )

    sim_display = simulated.sort_values(
        "incremental_platform_fee_revenue_usd",
        ascending=False,
    )

    scenario_cols = [
        "event_name",
        "market_country_code",
        "days_to_event",
        "tickets_available",
        "tickets_sold_28d",
        "simulated_avg_price_usd",
        "projected_units_sold_until_event",
        "projected_unsold_tickets_at_event",
        "simulated_sell_through_rate",
        "simulated_platform_fee_revenue_usd",
        "incremental_platform_fee_revenue_usd",
        "simulated_liquidity_segment",
        "simulated_dynamic_pricing_signal",
    ]

    st.dataframe(
        sim_display[scenario_cols].head(50),
        use_container_width=True,
        hide_index=True,
        column_config={
            "simulated_avg_price_usd": st.column_config.NumberColumn(
                "Sim Price",
                format="$%.2f",
            ),
            "simulated_platform_fee_revenue_usd": st.column_config.NumberColumn(
                "Sim Fee Revenue",
                format="$%.0f",
            ),
            "incremental_platform_fee_revenue_usd": st.column_config.NumberColumn(
                "Revenue Impact",
                format="$%.0f",
            ),
            "simulated_sell_through_rate": st.column_config.ProgressColumn(
                "Sim Sell-through",
                format="%.1f%%",
                min_value=0,
                max_value=1,
            ),
        },
    )

    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        fig_impact = px.bar(
            (
                simulated.groupby("simulated_dynamic_pricing_signal", dropna=False)
                .agg(
                    incremental_revenue=("incremental_platform_fee_revenue_usd", "sum"),
                    events=("event_id", "nunique"),
                )
                .reset_index()
                .sort_values("incremental_revenue", ascending=True)
            ),
            x="incremental_revenue",
            y="simulated_dynamic_pricing_signal",
            orientation="h",
            title="Incremental Fee Revenue by Simulated Action",
            labels={
                "incremental_revenue": "Incremental Fee Revenue",
                "simulated_dynamic_pricing_signal": "Action",
            },
            text="events",
        )

        fig_impact.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10, r=10, t=55, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_impact, use_container_width=True)

    with c2:
        fig_clearance = px.scatter(
            simulated,
            x="days_to_event",
            y="simulated_sell_through_rate",
            size="projected_unsold_tickets_at_event",
            color="simulated_liquidity_segment",
            hover_name="event_name",
            title="Simulated Clearance Risk",
            labels={
                "days_to_event": "Days to Event",
                "simulated_sell_through_rate": "Simulated Sell-through",
                "simulated_liquidity_segment": "Sim Segment",
            },
        )
        fig_clearance.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10, r=10, t=55, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig_clearance.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_clearance, use_container_width=True)


# ============================================================
# Tab 3: Event Drilldown
# ============================================================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Event-Level Decision View",
        "Inspect one event and translate marketplace signals into an executive action.",
    )

    if len(filtered) == 0:
        st.warning("No event available after filters.")
    else:
        event_options = (
            filtered.sort_values(["days_to_event", "platform_fee_revenue_usd_28d"], ascending=[True, False])
            .assign(label=lambda x: x["event_name"] + " | " + x["market_country_code"] + " | " + x["days_to_event"].astype(str) + " days")
        )

        selected_label = st.selectbox(
            "Select event",
            event_options["label"].tolist(),
        )

        selected_event = event_options[event_options["label"] == selected_label].iloc[0]

        e1, e2, e3, e4 = st.columns(4)
        with e1:
            metric_card("Days to Event", format_number(selected_event["days_to_event"], 0), "Perishability clock")
        with e2:
            metric_card("Tickets Available", format_number(selected_event["tickets_available"], 0), "Current supply")
        with e3:
            metric_card("Sell-through 28D", f"{selected_event['sell_through_rate_28d']:.1%}", "Demand conversion")
        with e4:
            metric_card("Fee Revenue 28D", format_currency(selected_event["platform_fee_revenue_usd_28d"], 1), "Recent monetization")

        detail_df = pd.DataFrame(
            {
                "Metric": [
                    "Event Name",
                    "Category",
                    "Market",
                    "Current Liquidity Segment",
                    "Current Pricing Signal",
                    "Average List Price",
                    "Average Transaction Price 28D",
                    "Price Gap vs Recent Transactions",
                    "Demand Pressure Score",
                    "Supply Pressure Score",
                    "Days of Supply",
                ],
                "Value": [
                    selected_event["event_name"],
                    selected_event["event_category"],
                    selected_event["market_country_code"],
                    selected_event["marketplace_liquidity_segment"],
                    selected_event["dynamic_pricing_signal"],
                    format_currency(selected_event["avg_list_price_usd"], 2),
                    format_currency(selected_event["avg_transaction_price_usd_28d"], 2),
                    f"{selected_event['price_gap_vs_recent_transactions_pct']:.1%}"
                    if pd.notna(selected_event["price_gap_vs_recent_transactions_pct"])
                    else "—",
                    f"{selected_event['demand_pressure_score']:.2f}",
                    f"{selected_event['supply_pressure_score']:.2f}",
                    f"{selected_event['days_of_supply']:.1f}"
                    if pd.notna(selected_event["days_of_supply"])
                    else "—",
                ],
            }
        )

        st.dataframe(detail_df, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# Tab 4: Governance & Data Quality
# ============================================================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Governance Contract",
        "Operational checks that make this mart safe for BI, experimentation, and AI feature consumption.",
    )

    checks = []

    def add_check(name, condition, severity="error"):
        checks.append(
            {
                "Check": name,
                "Status": "PASS" if condition else "FAIL",
                "Severity": severity,
            }
        )

    add_check("Primary key is unique", df["event_market_snapshot_key"].is_unique)
    add_check("Primary key is not null", df["event_market_snapshot_key"].notna().all())
    add_check("Event ID is not null", df["event_id"].notna().all())
    add_check("Snapshot date is not null", df["snapshot_date"].notna().all())
    add_check("Event date is not null", df["event_date"].notna().all())
    add_check("Tickets available is non-negative", (df["tickets_available"].fillna(0) >= 0).all())
    add_check("Tickets sold 28D is non-negative", (df["tickets_sold_28d"].fillna(0) >= 0).all())
    add_check("Sell-through rate is between 0 and 1", df["sell_through_rate_28d"].dropna().between(0, 1).all())
    add_check("Take rate is between 0 and 1", df["platform_take_rate_28d"].dropna().between(0, 1).all())
    add_check("Demand pressure score is between 0 and 1", df["demand_pressure_score"].dropna().between(0, 1).all())
    add_check("Supply pressure score is between 0 and 1", df["supply_pressure_score"].dropna().between(0, 1).all())

    checks_df = pd.DataFrame(checks)

    st.dataframe(
        checks_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Status"),
            "Severity": st.column_config.TextColumn("Severity"),
        },
    )

    failed_checks = checks_df[checks_df["Status"] == "FAIL"]

    if len(failed_checks) == 0:
        st.success("All governance checks passed. This mart is ready for executive analytics and AI feature consumption.")
    else:
        st.error("One or more governance checks failed. Treat this as fail-closed and block downstream consumption.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header(
        "Expected dbt Mart Contract",
        "This app expects the final mart to expose the following columns.",
    )

    expected_cols = pd.DataFrame(
        {
            "Column": [
                "event_market_snapshot_key",
                "snapshot_date",
                "event_id",
                "event_date",
                "event_name",
                "event_category",
                "market_country_code",
                "days_to_event",
                "tickets_available",
                "tickets_sold_28d",
                "avg_list_price_usd",
                "avg_transaction_price_usd_28d",
                "sell_through_rate_28d",
                "days_of_supply",
                "platform_take_rate_28d",
                "demand_pressure_score",
                "supply_pressure_score",
                "marketplace_liquidity_segment",
                "dynamic_pricing_signal",
            ],
            "Purpose": [
                "Primary grain",
                "Snapshot date",
                "Event identifier",
                "Event date",
                "Executive-readable event name",
                "Event classification",
                "Market dimension",
                "Perishability clock",
                "Supply quantity",
                "Demand signal",
                "Current supply-side price",
                "Recent realized transaction price",
                "Demand conversion",
                "Inventory clearance risk",
                "Platform monetization ratio",
                "Demand-side pressure",
                "Supply-side pressure",
                "Executive risk segment",
                "Recommended action signal",
            ],
        }
    )

    st.dataframe(expected_cols, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)