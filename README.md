# 🎟️ Enterprise Marketplace Liquidity & Perishable Inventory Optimization Platform
### Analytics Architecture: dbt (BigQuery) ✕ Streamlit Engine

---

## 📈 Executive Summary (経営要約)

<img width="1920" height="1937" alt="screencapture-localhost-8501-2026-06-24-17_15_03" src="https://github.com/user-attachments/assets/8ba9bf16-4538-49f6-b34e-364338207103" />


### 🇺🇸 English
This project delivers a production-grade analytics foundation and executive decision sandbox tailored for a **Global Two-Sided Live Event Marketplace Platform ($1B+ Revenue)**. 

In this business model, inventory is extremely **perishable**—a ticket's value collapses to zero the exact millisecond an event starts. The strategic bottleneck is **Marketplace Liquidity**: continuously balancing ticket supply and buyer demand while accounting for rapid **time-to-event decay**. Mispriced inventory near event dates deteriorates the marketplace health, causes seller churn, and severely damages the platform’s take-rate.

This solution completely bridges the gap between raw data and executive execution. Utilizing a governed **three-layer dbt architecture**, we transform fragmented transactional data into an AI-ready features mart. This backend is directly wired into a **Streamlit Executive Cockpit**, allowing leadership to dynamically simulate pricing elasticities, predict stockout/overstock risks, and execute automated, high-yield marketplace interventions.

### 🇯🇵 日本語
本プロジェクトは、**年商10億ドルを超えるグローバルな二面型ライブイベント・マーケットプレイス**を想定し、イベント開始と同時に価値がゼロになる「高速度・消滅型在庫」の損失をゼロにするための、エンタープライズ基準のモダンデータ基盤および経営意思決定サンドボックスです。

このビジネスの核心課題は **Marketplace Liquidity（市場流動性）** の維持です。チケットの供給、買い手の需要、価格競争力、そして「イベント日までの残り時間」をリアルタイムで調和させる必要があります。イベント直前に在庫が過剰、または割高な状態を放置すると、売り手の機会損失を招くだけでなく、プラットフォームの手数料収入（Take-rate）に致命的なダメージを与えます。

本ソリューションは、データの混沌から経営のアクションへの翻訳を完全自動化します。ガバナンスされた **3層の dbt アーキテクチャ** によって生データを信頼できる特徴量マートへと精製。この強力なバックエンドを **Streamlit 経営コックピット** とダイレクトに接続することで、経営陣がマウス一つで未来の価格弾力性をシミュレーションし、AI駆動のアクションシグナルをその場で執行できる環境を実現しました。

---

## 🎯 Strategic Business Dimensions (解決する3つの経営課題)

### 1. Perishable Inventory & Decay Tracking (消滅在庫の時間減衰ハック)
* **🇺🇸 Problem:** As the event date approaches, inventory value degrades rapidly. Traditional BI platforms only capture historical aggregations, leaving leadership blind to imminent unsold inventory risks.
* **🇯🇵 課題:** イベント日が近づくほど在庫価値は急激に劣化するが、従来のBIでは「過去の集計」しか見えず、直前の売れ残りリスクを予測できなかった。
* **🇺🇸 Solution:** Engineered the `time_to_event_decay_factor` within the dbt mart layer to automatically score asset decay risk daily based on the remaining days until the event.
* **🇯🇵 解決策:** dbtマート層に `time_to_event_decay_factor` を特徴量として実装。イベントまでの残り日数に応じた在庫劣化リスクを毎日自動的にスコアリング。

### 2. Marketplace Liquidity Segmenting (二面市場の流動性ガバナンス)
* **🇺🇸 Problem:** The balance between ticket supply (sellers) and buyer demand fluctuates wildly per event, black-boxing exactly where platform fee revenue leakage occurs.
* **🇯🇵 課題:** 売り手（供給）と買い手（需要）のバランスがイベントごとに激しくブレ、どこで手数料の機会損失が起きているかブラックボックス化していた。
* **🇺🇸 Solution:** Aggregated trailing 28-day ticket velocity and price variance (`price_gap_vs_recent_transactions_pct`) to automatically classify all events into 5 distinct liquidity segments (e.g., 'Oversupplied', 'Perishable Inventory Risk').
* **🇯🇵 解決策:** Trailing 28-day のチケット販売速度と価格ギャップ（`price_gap_vs_recent_transactions_pct`）を算出し、全イベントを『Oversupplied（供給過剰）』や『Perishable Risk（消滅リスク）』などの5つのセグメントに自動分類。

### 3. Actionable Self-Service Analytics (BIからシミュレーターへの昇華)
* **🇺🇸 Problem:** Traditional data tables act merely as static reports ("rearview mirrors"), failing to provide immediate operational guidance on which specific levers to pull to maximize platform margins.
* **🇯🇵 課題:** 従来のデータテーブル（表）は「結果のレポート」に過ぎず、経営陣が「次にどんなアクションを打てば利益が最大化するか」を判断できなかった。
* **🇺🇸 Solution:** Implemented an interactive "If-Then Simulator" via Streamlit. When executives adjust the promotion discount slider, the backend dbt logic recalculates instantly to stream real-time, actionable dynamic pricing signals like `discount_to_clear`.
* **🇯🇵 解決策:** Streamlitの「If-Thenシミュレーター」を実装。経営者がプロモーション値下げ率のスライダーを動かすと、dbtのロジックと連動して `discount_to_clear` などの具体的な「次の一手（価格シグナル）」を画面がリアルタイムに提案する。
---

## ⚙️ Modern Data Stack Architecture

* **Data Warehouse:** Google BigQuery / Snowflake (Target project deployment)
* **Transformation & Governance:** dbt (Staging ➡ Intermediate ➡ Marts with fail-closed tests)
* **Data Quality Assured:** Strict constraints via `dbt_utils` (Non-negative validation, accepted values)
* **Decision & Simulation Layer:** Streamlit Web Application (Wired to `fct_event_marketplace_liquidity_daily`)
