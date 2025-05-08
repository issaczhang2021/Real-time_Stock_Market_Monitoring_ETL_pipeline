# 📈 Real-time Stock Trading ETL Pipeline

## 📘 1. Project Overview

In the world of quantitative finance, timely access to high-quality trading data is critical for building dashboards, generating signals, and managing risk. This project simulates a production-grade real-time data pipeline that ingests intraday stock data, performs validation and transformation, and models it into analytics-ready tables—all in a local, Dockerized development environment.

🔍 **Why this project matters:**
- Helps simulate stock performance monitoring and analytics workflows
- Demonstrates real-world data engineering practices (DQ, orchestration, lakehouse modeling)
- Bridges raw financial data to business-facing dashboards

🎯 **Business use cases supported:**
- Daily stock dashboards and anomaly alerts
- Signal generation feeds for quantitative strategies
- Lakehouse ingestion for financial analytics

⚙️ **Engineering highlights:**
- Automated API ingestion with dynamic parameterization
- Delta Lake modeling across Bronze → Silver → Gold layers
- Column-level data quality enforcement with Soda Core
- Orchestration using Prefect with retry, alerting, and logging
- Full containerization and reproducibility using Docker

## 🌐 Public Data Source

All stock market data in this project is sourced from the [Alphavantage API](https://www.alphavantage.co/), a publicly available financial data provider.

- Intraday and daily stock trading data are fetched using dynamically generated REST API calls
- API keys are stored in `config/config.ini` and injected at runtime
- API calls are managed centrally in `api_factory.py`, supporting flexible symbol and time resolution configuration

🧪 **Example endpoint**:
```
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=YOUR_API_KEY
```

---

## 🛠️ 2. Platform & Implementation Summary

### 🔗 API Ingestion
- **Source**: Alpha Vantage
- **Implementation**: Python handler with dynamic URL generation in `api_utils/`
- **Config-driven**: Parameters managed in `config/config.ini`

### ⚙️ Data Processing
- **Engine**: Apache Spark (PySpark)
- **Environment**: Developed in VS Code, executed via Dockerized Spark containers
- **Design**: Modular Bronze → Silver → Gold pipeline with Prefect orchestration

### 🗃️ Data Storage
- **Storage Layer**: MinIO (S3-compatible object storage)
- **Format**: Delta Lake (ACID, schema enforcement, versioning)
- **Modeling**: Bronze → Silver → Gold
- **Partitioning**: By symbol and trade date

### ✅ Data Quality
- **Tool**: Soda Core
- **Execution**: CLI-based scan during Prefect runs
- **Rules (example):**
```yaml
checks for silver_stock_clean:
  - row_count > 0
  - missing_count(symbol) = 0
  - duplicate_count(timestamp, symbol) = 0
  - schema:
      fail:
        when required column missing: [symbol, trade_dt, close]
        when wrong column type:
          volume: integer
```

---

## 🧱 3. Layered Data Lakehouse Architecture

This project uses a structured Lakehouse model to enable scalable analytics and data validation.

- **Bronze Layer**: Raw intraday API payloads stored in Delta format
- **Silver Layer**: Cleaned, schema-validated tables with `is_valid` flags
- **Gold Layer**: Aggregated daily KPIs like volume, avg price, price movement
- **BI View**: A materialized view for Power BI/Tableau with fields like `volatility_score`, `7d_avg`, `price_change_pct`

### 🖥️ Architecture Diagram
![Stock ETL Data Model](https://github.com/issaczhang2021/spark_etl_JZ/raw/master/Github.png)

---

## 🎯 4. Design FAQ
This project reflects key architectural and operational decisions as follows:

- **Data Quality Assurance**  
  Data quality is enforced using a YAML-based rule system that supports null checks, range validation, and type enforcement. These rules are embedded directly into the ETL workflow and trigger failure handling logic when violated.

- **Handling Upstream API Failures or Incomplete Data**  
  The pipeline is designed with retry logic and fault tolerance in mind. Prefect handles transient API failures gracefully, while downstream data quality gates prevent bad data from entering the lake.

- **Rationale for Using Delta Lake over Parquet**  
  Delta Lake was chosen to ensure ACID compliance, support schema evolution, enable time travel, and provide performance optimizations like Z-ordering and file compaction—essential for maintaining a reliable analytics platform.

- **Workflow Modularity and Orchestration**  
  The ETL process is modularized into discrete, reusable Prefect tasks and flows, making the system maintainable and extensible. It supports scheduling, alerting, retries, and logging out-of-the-box.

- **Scalability Across Symbols and Volume**  
  The architecture supports dynamic scaling by parallelizing ingestion by symbol. Spark handles data processing in a distributed fashion, and partitioning strategies ensure high performance at scale.

- **Why Prefect over Airflow**: Simpler to set up and easier to deploy locally or on Docker. Ideal for lightweight workflows.

- **Why Delta Lake**: Needed ACID compliance, time-travel, and scalable parquet storage.

- **Why Bronze/Silver/Gold**: Enables clear separation of concerns, quality checkpoints, and scalable analytics.

---

## 🔁 5. Extensibility

- Add more symbols with config only
- Extend to crypto, FX, or news feeds
- Plug output tables into BI tools

---

## 🧪 6. Testing & Monitoring

- Modular unit test support for ingestion and transformation
- Prefect logs all task results and failure alerts
- Sample datasets available in `/sample_files/`

---

## 🧰 7. Technology Stack
- **Python**: Core scripting language
- **PySpark**: Distributed data processing
- **Alphavantage API**: Public financial data
- **Delta Lake**: Scalable storage format with schema control
- **MinIO/S3**: S3-compatible object store
- **Prefect**: Modern orchestration engine
- **Docker + Makefile**: For repeatable setup & execution

---

## 📂 8. Project Structure
```
spark_etl_JZ/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── config/config.ini
├── data_quality/trade.yml
├── delta_tables/
│   ├── create_bronze_layer.py
│   └── create_silver_layer.py
├── pipelines/
│   ├── api_utils/
│   │   ├── api_factory.py
│   │   └── get_api_data.py
│   ├── api_to_csv_flow.py
│   ├── dq_utils.py
│   ├── etl_utils.py
│   ├── stock_etl.py
│   └── transform.py
├── sample_files/
│   └── trade_*.csv
└── README.md
```

---

## 🚀 9. Quick Start
```bash
git clone https://github.com/issaczhang2021/spark_etl_JZ
cd spark_etl_JZ
docker-compose build
```

1. Register for a free [Alphavantage API key](https://www.alphavantage.co/support/#api-key)
2. Update your `config/config.ini` with the key
3. Run the ETL pipeline:
```bash
docker-compose up
```

---

## 🔮 10. Future Work
- Kafka-based real-time ingestion
- Power BI/Tableau live integration
- Push notification alerting

## 🤝 11. Contribution
- Open issues for bugs or feature requests
- Submit PRs for enhancements or feedback

## 📄 12. License
Distributed under the MIT License. See `LICENSE` for full details.

## 📄 11. License
Distributed under the MIT License. See `LICENSE` for more details.
