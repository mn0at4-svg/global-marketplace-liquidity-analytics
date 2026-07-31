# 🎟️ Enterprise Marketplace Liquidity & Perishable Inventory Optimization Platform

### Governed Analytics Architecture: dbt × Streamlit

[🚀 **Launch the Live Executive Simulator**](https://global-marketplace-liquidity.streamlit.app/)

[📂 **Explore the GitHub Repository**](https://github.com/mn0at4-svg/global-marketplace-liquidity-analytics)

> **Portfolio disclosure:** This project is a reference implementation built with synthetic data. It does not connect to a production marketplace, execute real pricing changes, or contain confidential company data.

---

## 📈 Executive Summary｜経営要約

<img width="1920" height="1937" alt="Enterprise Marketplace Liquidity Cockpit" src="https://github.com/user-attachments/assets/8ba9bf16-4538-49f6-b34e-364338207103" />

### 🇺🇸 English

This project demonstrates a governed analytics and executive decision platform for a hypothetical **global two-sided live-event marketplace generating more than US$1 billion in annual revenue**.

In this business model, ticket inventory is highly perishable. Once an event begins, unsold inventory loses virtually all economic value. The central management challenge is therefore **marketplace liquidity**: balancing seller supply, buyer demand, price competitiveness, conversion velocity, and time remaining until the event.

The project translates fragmented marketplace activity into decision-ready analytical products through a three-layer dbt architecture:

```text
Staging
→ Intermediate Business Logic
→ Executive Facts and Marts
```

The curated mart is surfaced through an interactive Streamlit application that allows executives, product leaders, and analytics teams to explore:

* marketplace liquidity conditions;
* oversupply and stockout exposure;
* time-to-event inventory decay;
* price gaps versus recent transactions;
* potential fee-revenue impact;
* dynamic-pricing and demand scenarios;
* recommended management actions.

The purpose is not to automate pricing decisions without oversight. It is to demonstrate how governed data models and interactive simulations can support faster, more explainable, and more consistent executive decisions.

### 🇯🇵 日本語

本プロジェクトは、**年商10億ドル超のグローバルな二面型ライブイベント・マーケットプレイス**を想定した、ガバナンス型分析基盤および経営意思決定シミュレーターです。

ライブイベントのチケットは、イベント開始と同時に未販売在庫の経済価値がほぼ失われる、極めて消滅性の高い在庫です。

そのため、このビジネスにおける中心的な経営課題は、次の要素を継続的に調整する **Marketplace Liquidity（市場流動性）** の管理です。

* 売り手から供給されるチケット在庫
* 買い手の需要と購入速度
* 市場価格に対する競争力
* イベントまでの残り時間
* 在庫の販売率と売れ残りリスク
* プラットフォームの手数料収入

本プロジェクトでは、分断されたマーケットプレイスデータを、3層のdbtアーキテクチャによって意思決定可能なデータプロダクトへ変換します。

```text
Staging
→ Intermediate Business Logic
→ Executive Facts and Marts
```

その分析マートをStreamlitの経営コックピットへ接続し、経営者、プロダクト責任者、アナリティクス担当者が以下を対話的に検証できるようにしています。

* 市場流動性の状態
* 供給過剰と在庫不足リスク
* イベント接近に伴う在庫価値の減衰
* 直近取引価格との価格差
* 手数料収入への潜在的影響
* 価格、需要、供給に関するシナリオ
* 推奨される経営アクション

本プロジェクトの目的は、AIやシステムへ価格決定を無条件に委任することではありません。

**ガバナンスされたデータモデルとシミュレーションによって、より迅速で説明可能かつ一貫した経営判断を支援すること**を目的としています。

---

## 🚀 Live Executive Simulator

The public Streamlit application can be accessed without authentication:

### [Open the Marketplace Liquidity Cockpit](https://global-marketplace-liquidity.streamlit.app/)

### Try the simulator in 30 seconds

1. Select an event or marketplace segment from the sidebar.
2. Open the pricing or scenario-simulation area.
3. Adjust price, demand, supply, or marketing assumptions.
4. Compare baseline and simulated outcomes.
5. Review the resulting executive action signal.

### Public-demo safeguards

The public application is intentionally limited to a curated synthetic dataset.

The following development functions are not exposed in the public version:

* arbitrary SQL execution;
* editable BigQuery table references;
* cloud credentials;
* production writeback;
* automatic price changes;
* unrestricted external data uploads.

---

## 🎯 Strategic Business Dimensions｜解決する経営課題

### 1. Perishable Inventory and Time-to-Event Decay

### 消滅在庫とイベント接近リスク

**🇺🇸 Business problem**

As an event approaches, the remaining opportunity to sell inventory decreases rapidly. Static historical dashboards often identify unsold inventory only after there is little time left to intervene.

**🇯🇵 経営課題**

イベント日が近づくほど販売可能な時間は減少します。しかし、過去実績を中心とした静的なBIでは、対応可能な時間がほとんど残っていない段階で初めて売れ残りリスクが明らかになることがあります。

**🇺🇸 Analytical solution**

The dbt mart includes a governed `time_to_event_decay_factor` that helps classify inventory exposure according to the number of days remaining before each event.

**🇯🇵 分析上の解決策**

dbtマートに `time_to_event_decay_factor` を実装し、イベントまでの残り日数に応じて在庫の時間減衰リスクを分類します。

This supports earlier identification of:

* high inventory with limited selling time;
* low sales velocity near the event date;
* price levels that may require intervention;
* events requiring management attention.

これにより、以下を早期に特定できます。

* 販売期間が短いにもかかわらず在庫が多いイベント
* イベント直前でも販売速度が低い在庫
* 価格調整の検討が必要な可能性のあるイベント
* 経営判断や追加施策が必要な案件

---

### 2. Marketplace Liquidity Segmentation

### 二面市場の流動性分類

**🇺🇸 Business problem**

Ticket supply and buyer demand vary significantly by event. Without a consistent analytical framework, it is difficult to determine whether a marketplace is healthy, oversupplied, supply-constrained, or at risk of perishable inventory loss.

**🇯🇵 経営課題**

チケット供給と買い手需要のバランスは、イベントごとに大きく異なります。共通の分析基準がなければ、市場が健全なのか、供給過剰なのか、在庫不足なのか、売れ残りリスクが高いのかを一貫して判断できません。

**🇺🇸 Analytical solution**

The models combine recent transaction velocity, listing supply, buyer demand, price competitiveness, sales progress, and time remaining to classify events into interpretable liquidity segments.

Example segments include:

* Balanced;
* Oversupplied;
* Supply-Constrained;
* Perishable Inventory Risk;
* Demand Generation Opportunity.

**🇯🇵 分析上の解決策**

直近の取引速度、出品在庫、買い手需要、価格競争力、販売進捗、イベントまでの残り時間を統合し、各イベントを解釈可能な市場流動性セグメントへ分類します。

分類例：

* Balanced：需給均衡
* Oversupplied：供給過剰
* Supply-Constrained：供給不足
* Perishable Inventory Risk：消滅在庫リスク
* Demand Generation Opportunity：需要創出機会

Key analytical fields include:

* `price_gap_vs_recent_transactions_pct`
* trailing transaction velocity
* inventory sell-through
* remaining inventory
* days to event
* marketplace liquidity segment

---

### 3. Pricing and Demand Scenario Simulation

### 価格・需要シナリオ分析

**🇺🇸 Business problem**

Traditional dashboards explain what has already happened but do not always help executives understand the possible consequences of changing price, supply, demand, or promotional assumptions.

**🇯🇵 経営課題**

従来型のダッシュボードは過去の結果を説明できますが、価格、供給、需要、プロモーション条件を変更した場合に、結果がどのように変化するかまでは示せない場合があります。

**🇺🇸 Analytical solution**

The Streamlit application provides a controlled what-if environment in which users can adjust assumptions and compare simulated results with a baseline.

The simulator can illustrate possible changes in:

* projected demand;
* inventory clearance;
* stockout risk;
* unsold inventory;
* gross transaction value;
* marketplace fee revenue;
* recommended intervention.

**🇯🇵 分析上の解決策**

Streamlitアプリでは、利用者が前提条件を変更し、基準値とシミュレーション結果を比較できる統制されたWhat-if環境を提供します。

確認できる変化の例：

* 予測需要
* 在庫消化
* 在庫不足リスク
* 売れ残り在庫
* 流通取引総額
* プラットフォーム手数料収入
* 推奨アクション

The simulation is decision support, not a production pricing engine.

本シミュレーションは経営判断支援を目的としており、本番環境で価格を自動変更するシステムではありません。

---

### 4. Governed Self-Service Analytics

### ガバナンスされたセルフサービス分析

**🇺🇸 Business problem**

Executive dashboards lose credibility when KPI definitions, business rules, and data transformations are inconsistent or hidden inside individual reports.

**🇯🇵 経営課題**

KPI定義、業務ルール、データ変換がレポートごとに異なる場合、経営ダッシュボードの信頼性が低下します。

**🇺🇸 Analytical solution**

Business logic is moved upstream into governed dbt models rather than being recreated independently inside each visualization.

This creates a clearer separation between:

```text
Data transformation
Business-rule calculation
Decision simulation
Executive presentation
```

**🇯🇵 分析上の解決策**

業務ロジックを各グラフや画面内で個別実装するのではなく、上流のdbtモデルへ集約します。

これにより、以下の責任範囲を明確に分離します。

```text
データ変換
業務ルール計算
意思決定シミュレーション
経営向け表示
```

---

## ⚙️ Analytics Architecture

```text
Synthetic Marketplace Source Data
                │
                ▼
        dbt Staging Models
     Standardization and cleanup
                │
                ▼
      dbt Intermediate Models
Liquidity, pricing, demand and
time-to-event business logic
                │
                ▼
        Executive Fact Mart
fct_event_marketplace_liquidity_daily
                │
                ▼
      Streamlit Executive Cockpit
Filters, diagnostics and simulation
```

### Data and application stack

| Layer                 | Technology                        | Purpose                                                 |
| --------------------- | --------------------------------- | ------------------------------------------------------- |
| Data warehouse target | Google BigQuery                   | Cloud analytical warehouse                              |
| Transformation        | dbt                               | Modular SQL transformation and documentation            |
| Data quality          | dbt tests and business-rule tests | Validate model assumptions and output integrity         |
| Business logic        | SQL and deterministic Python      | Calculate liquidity, risk and scenario outputs          |
| Application           | Streamlit                         | Interactive executive decision interface                |
| Visualization         | Plotly                            | Interactive charts and comparisons                      |
| Version control       | GitHub                            | Source control, review history and portfolio publishing |
| Deployment            | Streamlit Community Cloud         | Public interactive application                          |

> Snowflake compatibility is an architectural extension target, not part of the current public deployment.

---

## 🧱 dbt Modeling Structure

### Staging layer

The staging layer standardizes raw marketplace records and establishes consistent field definitions.

Typical responsibilities include:

* type casting;
* null handling;
* date normalization;
* identifier standardization;
* numeric validation;
* source-field renaming.

### Intermediate layer

The intermediate layer applies reusable business logic such as:

* recent transaction velocity;
* supply-demand relationships;
* price-gap calculations;
* sales progress;
* time-to-event exposure;
* liquidity classification;
* pricing and intervention signals.

### Mart layer

The executive fact mart consolidates the metrics required by the Streamlit application.

Primary model:

```text
fct_event_marketplace_liquidity_daily
```

The mart is designed to provide a reusable analytical contract for executive reporting, scenario analysis, and future automation.

---

## 🛡️ Data Quality and Governance

The project uses dbt tests and deterministic checks to prevent invalid analytical outputs from silently reaching the executive layer.

Representative controls include:

* required identifiers must not be null;
* accepted categorical values;
* non-negative ticket and monetary values;
* valid event dates;
* consistent marketplace segments;
* bounded percentage metrics;
* unique analytical grain;
* documented business definitions.

Where required inputs are missing or logically invalid, the intended design principle is **fail closed rather than fabricate a decision signal**.

---

## 🧠 Decision Authority Boundary

This project separates deterministic calculations from explanatory or advisory functions.

### Deterministic logic is responsible for

* sales and inventory calculations;
* time-to-event measures;
* price-gap calculations;
* liquidity segmentation;
* simulated revenue outcomes;
* threshold and risk classification.

### Human decision-makers remain responsible for

* final pricing decisions;
* commercial policy changes;
* marketplace interventions;
* production deployment;
* customer- or seller-facing actions.

### AI or natural-language extensions may support

* executive summaries;
* anomaly explanations;
* scenario interpretation;
* presentation of approved analytical results.

AI is not authorized to alter source metrics, execute unrestricted SQL, or make unapproved production changes.

---

## 📊 Executive Questions Supported

The platform is designed to help answer questions such as:

* Which events have the highest unsold-inventory exposure?
* Where is supply materially greater than demand?
* Which events are likely to stock out?
* Which listings are priced above recent transaction benchmarks?
* How does time remaining affect recommended intervention?
* What could happen to inventory and fee revenue under a pricing change?
* Which marketplace segments require immediate management attention?
* Which business rule produced the recommendation?

---

## 💼 Business and Career Relevance

This portfolio demonstrates the ability to connect:

```text
Executive strategy
→ Governed analytics engineering
→ Business-rule modeling
→ Interactive decision products
→ Explainable management actions
```

It is designed to be relevant to roles and projects involving:

* Analytics Engineering
* Data Product Management
* Marketplace Analytics
* Pricing and Revenue Analytics
* Product Analytics
* Decision Intelligence
* Modern Data Stack Architecture
* Executive BI
* Business Transformation
* Data and AI Governance

---

## 🧪 Project Status

| Capability                         | Status          |
| ---------------------------------- | --------------- |
| dbt three-layer architecture       | Implemented     |
| Marketplace liquidity mart         | Implemented     |
| Synthetic demo dataset             | Implemented     |
| Local Streamlit application        | Implemented     |
| Public Streamlit deployment        | Implemented     |
| Interactive scenario simulation    | Implemented     |
| Public-demo input restrictions     | Implemented     |
| Arbitrary SQL in public app        | Disabled        |
| Production marketplace integration | Not implemented |
| Automated production pricing       | Not implemented |
| Real customer or seller data       | Not used        |

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/mn0at4-svg/global-marketplace-liquidity-analytics.git
cd global-marketplace-liquidity-analytics
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 📁 Repository Overview

```text
global-marketplace-liquidity-analytics/
├── app.py
├── requirements.txt
├── README.md
├── dbt_project.yml
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── macros/
├── seeds/
├── tests/
└── documentation/
```

The exact structure may evolve as deployment, testing, and portfolio evidence are expanded.

---

## 🔭 Potential Next Extensions

Possible future enhancements include:

* BigQuery-backed read-only deployment;
* CI/CD validation for dbt and Streamlit;
* model contracts and freshness controls;
* automated screenshot and release evidence;
* demand-elasticity calibration;
* experiment measurement;
* semantic-layer integration;
* role-specific executive views;
* controlled AI-generated executive summaries;
* Cloud Run deployment with least-privilege IAM.

These are extension opportunities and should not be interpreted as currently deployed production capabilities.

---

## 👤 Project Positioning

This project forms part of a broader portfolio focused on translating executive business problems into governed data products, decision simulations, and auditable AI-enabled workflows.

Related themes include:

* marketplace liquidity and dynamic pricing;
* manufacturing quotation and margin governance;
* working capital and supplier resilience;
* deterministic financial controls;
* human-controlled AI operations.

### Positioning statement

> I translate business strategy into governed analytics products, interactive decision systems, and auditable AI workflows.

---

## 📬 Contact

**Atsushi Mano**

GitHub: [mn0at4-svg](https://github.com/mn0at4-svg)

Live application: [global-marketplace-liquidity.streamlit.app](https://global-marketplace-liquidity.streamlit.app/)

---

## Disclaimer

This repository is an independent portfolio project.

All organizations, marketplace conditions, transactions, financial values, events, users, sellers, and operational scenarios are simulated. Any resemblance to a real company or dataset is coincidental.

The project does not provide production pricing recommendations, financial advice, or authorization to execute commercial actions.
