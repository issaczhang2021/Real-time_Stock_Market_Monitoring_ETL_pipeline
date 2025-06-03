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

## 🔀 Project Phases

This project is organized into two distinct phases to balance development speed, cost control, and production readiness:

> **Why split into two phases?**  
> Phase 1 focuses on validating architecture and core logic in a low-cost, open-source environment (MinIO, Prefect, PySpark) so we can iterate quickly without incurring excessive cloud fees. Once the design is proven, Phase 2 migrates the pipeline to AWS for production‐grade needs—supporting serverless scaling, SLA compliance, and seamless integration with BI/ML services.

> **Why MinIO in Phase 1?**  
> MinIO is an open-source, S3-compatible object storage platform that can run locally or on any cloud provider (including Azure). By building on MinIO, the pipeline is cloud-agnostic and easily portable. This design choice reduces vendor lock-in, allowing future migration from AWS to other clouds (like Azure, GCP) with minimal storage layer changes.

---
### Business Considerations for Phase 2 AWS Deployment

The choice of AWS services and minute ingestion interval should be aligned with enterprise-specific factors such as:

- **Budget Constraints:**  
  Serverless architectures (Lambda, Glue, Athena) provide pay-per-use pricing, ideal for organizations seeking cost control and elasticity without upfront infrastructure investment.

- **Data Freshness Requirements:**  
  For firms requiring near real-time analytics (e.g., minute-level), shorter invocation intervals can be used, balancing frequency and cost. For less time-sensitive analytics, longer intervals (e.g., 5 minutes) reduce cost and operational complexity.

- **Operational Complexity and Reliability:**  
  Glue’s batch-oriented ETL simplifies data processing pipelines, favoring stability and maintainability over ultra-low latency streaming.

- **Scalability Needs:**  
  Managed services scale transparently with demand, benefiting businesses with variable or growing data volumes.

  This flexible design approach demonstrates a practical understanding of how to deploy data pipelines that fit diverse business priorities—from startups controlling cloud spend to enterprises demanding real-time SLA compliance.
---

### Phase 1: Prototype & Validation (5-Minute Interval Pipeline)
- **Goal**: Quickly build a proof-of-concept (POC) using open-source tools to validate overall design, test ingestion/transformation logic, and control costs.
- **Key Activities**:
  - Developed a config-driven Python API handler to fetch 5-minute interval data for multiple symbols.
  - Orchestrated ingestion workflows with Prefect and applied PySpark transformations to clean, standardize, and write data into partitioned Parquet format.
  - Structured a Bronze (raw JSON) layer and Silver (cleaned Parquet) layer on Delta Lake in MinIO, ensuring traceability and clean snapshots via schema evolution.
  - Modeled a Gold layer by aggregating Silver data to compute trading signals (e.g., P/E Ratio Alert, Volume Spike % Alert) for strategy development.
  - Implemented deduplication with incremental merge, partitioning, and late-arriving data correction to keep historical records consistent.
  - Integrated Soda Core for data quality checks (freshness, null rates, duplication) via YAML-defined scan definitions.
  - Containerized the entire pipeline using Docker Compose to ensure a reproducible dev environment compatible with future AWS migration.

### Phase 2: AWS Migration & Productionization (Configurable Interval)
- **Goal**: Migrate the validated prototype to a serverless, fully managed AWS architecture for elastic, SLA-compliant operations with flexible ingestion intervals according to business needs.
- **Key Activities**:
  - Refactored the Python API handler into an AWS Lambda function triggered by EventBridge, allowing configurable invocation intervals (e.g., 1-minute or 5-minute) based on workload and budget.
  - Deployed transformation logic to AWS Glue (PySpark) with Delta Lake on S3, enabling serverless batch or micro-batch processing and scalable late-arriving data correction.  
    **Note:** AWS Glue is optimized for batch/micro-batch ETL workloads rather than continuous streaming. For true streaming or sub-minute latency, streaming services like Amazon Kinesis or MSK are recommended.
  - Reused Soda YAML scan checks on Athena tables to enforce data freshness, duplication prevention, and schema consistency in production.
  - Provided downstream analytics endpoints via Athena and QuickSight for Gold-layer factor dashboards, quantitative signals, and ML retraining pipelines.
  - Ensured cost efficiency and operational scalability by leveraging AWS managed services, making the architecture suitable for businesses with variable budget scales and compliance requirements.

---





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
![Stock ETL Data Model](https://github.com/issaczhang2021/Real-time_Stock_Market_Monitoring_ETL_pipeline/blob/730dd9b33c94f3bbbe3ba230d6c367152a170136/Github.png)
  
---
## 🎯 4. Design FAQ
This project reflects key architectural and operational decisions as follows:

- **Data Quality Assurance**  
  Data quality is enforced using a YAML-based rule system that supports null checks, range validation, and type enforcement. In Phase 1, these checks run in Prefect via Soda Core against the Bronze/Silver Delta tables in MinIO. In Phase 2, the same Soda YAML scans run against Athena tables to validate freshness, null rates, and duplication in S3-backed Silver datasets.

- **Handling Upstream API Failures or Incomplete Data**  
  - **Phase 1**: Prefect tasks retry failed API calls (e.g., due to 5-calls/min rate limits) and apply a “waiting window” before marking data as missing.  
  - **Phase 2**: AWS Lambda functions are invoked by EventBridge with built-in retry logic. Failed Lambda executions trigger CloudWatch Alarms and can be replayed manually or via a dead-letter queue.

- **Rationale for Using Delta Lake over Parquet**  
  - **Phase 1**: Delta Lake in MinIO provides ACID compliance, schema evolution, and time travel for local prototyping.  
  - **Phase 2**: Delta Lake on S3 via AWS Glue supports the same ACID guarantees at scale, with Glue catalog tables exposed in Athena for SQL analytics and QuickSight dashboards.

- **Workflow Modularity and Orchestration**  
  - **Phase 1**: Prefect flows organize ingestion → cleaning → modeling tasks.  
  - **Phase 2**: Serverless orchestration is split between EventBridge schedules (Lambda triggers) for ingestion and AWS Glue workflows (PySpark jobs) for batch transformations. Prefect is no longer required in production.

- **Scalability Across Symbols and Volume**  
  - **Phase 1**: Spark jobs running in Docker containers parallelize by symbol.  
  - **Phase 2**: Lambda concurrency handles parallel API ingestion, and AWS Glue auto-scales to process large volumes of JSON or Parquet in S3. Athena partitions (by symbol, trade_date) ensure performant queries.

- **Why Prefect over Airflow (Phase 1)**:  
  - Lightweight, easy local Docker deployment, quick iteration.  

- **Why AWS Lambda & EventBridge (Phase 2)**:  
  - True serverless, zero-ops ingestion. EventBridge cron rules support 1-minute intervals without managing servers.

- **Why AWS Glue & Athena (Phase 2)**:  
  - Glue’s PySpark integration with Delta on S3 enables elastic batch processing and late-arriving data correction. Athena provides interactive SQL on S3/Glue tables for downstream analytics without provisioning clusters.

- **Why Delta Lake in AWS (Phase 2)**:  
  - Maintains the same familiar Delta features (ACID, time travel) on top of S3. Glue Catalog integration enables schema management and versioned data.

- **Why Bronze/Silver/Gold (Both Phases)**:  
  - Separates raw payloads (traceability) from cleaned data (consistency) and aggregated metrics (dashboard/ML readiness). This layering enforces quality gates and clear audit trails.

---


## 🔁 5. Extensibility
  
- **Phase 1 (Local Prototype):**  
  - Add new symbols by updating `config/config.ini`. Prefect flows automatically pick up new symbols for ingestion.  
  - Extend to other asset classes (crypto, FX, news) by writing additional API handlers and incorporating them into the same Prefect/Spark framework.  
  - Add ML feature computation in the Gold layer by appending new transform scripts under `pipelines/transform.py`.

- **Phase 2 (AWS Production):**  
  - Add new symbols by updating the Lambda environment variable `SYMBOL_LIST` (or read from a DynamoDB table). EventBridge rules automatically trigger ingestion for all configured symbols.  
  - Extend to new data sources (crypto, FX, news) by creating new Lambda functions or EventBridge rules, and updating Glue jobs to incorporate additional datasets into the Delta Lake on S3.  
  - Integrate downstream ML pipelines by pointing SageMaker Processing jobs or Step Functions to the Gold-layer Athena tables.  
  - Support additional AWS services (e.g., Kinesis for streaming or SNS for push alerts) by adding notification logic in Lambda or Glue jobs.

---

  
## 🧪 6. Testing & Monitoring
  
- **Phase 1 (Local Testing):**  
  - Unit tests for API handler logic (`api_utils/get_api_data.py`).  
  - Prefect’s local test mode to validate workflow dependencies and edge cases.  
  - Soda Core CLI scans in CI pipelines to catch schema violations before container builds.  
  - Manual Docker Compose runs to verify Bronze/Silver/Gold writes and incremental merges.

- **Phase 2 (AWS Monitoring):**  
  - **Lambda Logs & Metrics**: Monitor invocation counts, error rates, and duration in CloudWatch. Configure CloudWatch Alarms for throttling or failures.  
  - **Glue Job Monitoring**: Use Glue job runs and metrics (DPU usage, success/failure) in CloudWatch. Set alerts for failed runs or job timeouts.  
  - **Athena Query Validation**: Schedule periodic AWS Glue Data Quality (Soda) scans via AWS Step Functions or a Lambda to run prebuilt SQL queries against Athena tables, checking for null rates, duplicate keys, and stale partitions.  
  - **Cost Monitoring**: Use AWS Cost Explorer and budget alarms to track S3 storage growth, Glue DPU hours, and Lambda invocations.  
  - **End-to-End SLA Checks**: Create CloudWatch Synthetic Canaries or Lambda heartbeats that test ingestion → transformation → table-availability in Athena, alerting on delays beyond SLA.

---

  
## 🧰 7. Technology Stack
  
- **Phase 1 (Open-Source Prototype):**  
  - **Python**: Core scripting, API handlers, Prefect flows  
  - **PySpark**: Distributed data processing in Dockerized Spark containers  
  - **Delta Lake**: ACID storage on MinIO (S3-compatible)  
  - **MinIO**: Local S3-compatible object storage  
  - **Prefect**: Workflow orchestration, retries, and logging  
  - **Soda Core**: YAML-defined data quality checks  
  - **Docker & Docker Compose**: Reproducible environment for local development  

- **Phase 2 (AWS Production):**  
  - **AWS Lambda**: Serverless ingestion with Python-based API handler (1-minute triggers via EventBridge)  
  - **Amazon EventBridge**: Cron-based scheduler for Lambda invocations  
  - **Amazon S3**: Scalable object storage for raw JSON and Parquet Delta tables  
  - **AWS Glue (PySpark)**: Serverless ETL for cleaning, transformations, incremental merges, and late-arriving data correction with Delta Lake on S3  
  - **AWS Glue Data Catalog**: Central metadata store for Delta tables, used by Athena and QuickSight  
  - **Amazon Athena**: Interactive SQL analytics on S3-backed Delta tables for downstream dashboards and ML feature pipelines  
  - **Amazon QuickSight**: BI dashboards for Gold-layer factor metrics and trading signals  
  - **CloudWatch**: Centralized logging, metrics, and alarms for Lambda and Glue  
  - **Soda Core (via Athena)**: Data quality checks on production datasets  
  - **AWS CLI / Terraform (optional)**: Infrastructure-as-code for deploying Lambda, EventBridge, and Glue resources  

---


  
## 📂 8. Project Structure

```
spark_etl_JZ/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── config/
│ └── config.ini # Phase 1: 5-min interval symbols, API keys
├── data_quality/
│ └── trade.yml # Phase 1: Soda Core YAML checks
├── delta_tables/
│ ├── create_bronze_layer.py
│ └── create_silver_layer.py
├── pipelines/ # Phase 1 ETL code
│ ├── api_utils/
│ │ ├── api_factory.py
│ │ └── get_api_data.py
│ ├── api_to_csv_flow.py
│ ├── dq_utils.py
│ ├── etl_utils.py
│ ├── stock_etl.py
│ └── transform.py
├── sample_files/
│ └── trade_*.csv
├── README.md
└── godata2023/ # Phase 2: AWS deployment artifacts
├── AWS Deployment/
│ ├── fetch_stock_data.py # Lambda handler (configurable ingestion interval)
│ ├── glue_etl_job.py # Glue PySpark transformation job
│ ├── deploy/
│ │ ├── build_lambda_package.sh # Package Lambda code
│ │ ├── deploy_lambda.sh # Deploy Lambda & IAM role
│ │ ├── create_eventbridge_rule.sh# Schedule Lambda trigger
│ │ └── lambda_iam_policy.json # IAM policy for Lambda
│ └── infrastructure/ # (Optional) Terraform/CloudFormation templates
│ ├── lambda.tf
│ ├── glue.tf
│ └── eventbridge.tf
```
---


  
## 🚀 9. Quick Start

- **This section describes how to deploy the pipeline on AWS to support 1-minute interval real-time data ingestion using a fully managed, serverless architecture.**

Why Use AWS Serverless for This Project?
  - **Real-Time Data Capture: Continuously fetch updated stock prices every minute from public APIs (e.g., Alpha Vantage) with low latency.

  - **Cost-Effective: Utilizes AWS Free Tier services like Lambda, S3, EventBridge, and Glue with generous free limits.

  - **Scalable & Serverless: No infrastructure management required, with fully managed execution, monitoring, and scaling.

  
```bash
git clone https://github.com/issaczhang2021/Real-time_Stock_Market_Monitoring_ETL_pipeline
cd Real-time_Stock_Market_Monitoring_ETL_pipeline
docker-compose build
```

1. Register for a free [Alphavantage API key](https://www.alphavantage.co/support/#api-key)
2. Update your `config/config.ini` with the key
3. Run the ETL pipeline:
```bash
docker-compose up
```
---

## 📄 10. AWS Deployment Overview

This section describes how to deploy the pipeline on AWS to support **5-minute interval real-time data ingestion** using a fully managed, serverless architecture.

### Why Use AWS Serverless for This Project?

- **Real-Time Data Capture:**  
  Continuously fetch updated stock prices every **minute** from public APIs (e.g., Alpha Vantage) with low latency.

- **Cost-Effective:**  
  Utilizes AWS Free Tier services like Lambda, S3, EventBridge, and Glue with generous free limits.

- **Scalable & Serverless:**  
  No infrastructure management required, with fully managed execution, monitoring, and scaling.

### Architecture Overview

```
EventBridge (Every 5 min)
       ↓
 AWS Lambda (fetch_stock_data.py)
       ↓
Stock API (e.g., Alpha Vantage)
       ↓
Amazon S3 (Raw JSON: stock-raw-data/)
       ↓
(Optional) AWS Glue Job
       ↓
Amazon S3 (Cleaned Parquet: stock-cleaned-data/)
       ↓
Power BI / QuickSight / Athena
```

### Step-by-Step Deployment Instructions

#### Package Lambda Function

```bash
cd godata2023/AWS\ Deployment
bash deploy/build_lambda_package.sh
```

#### Deploy to AWS Lambda

```bash
bash deploy/deploy_lambda.sh
```

#### IAM Role Permissions

See `deploy/lambda_iam_policy.json` for required permissions.

#### Schedule with EventBridge

```bash
bash deploy/create_eventbridge_rule.sh
```

This sets up a 5-minute cron trigger for Lambda.

### Optional: Glue Job for Batch Processing

Glue PySpark job cleans and converts raw JSON to Parquet for downstream analytics.

### Monitoring

- Lambda logs via CloudWatch  
- EventBridge Rule management  
- Glue job run history  

### Cost Summary

| Service     | Free Tier                 |
|-------------|---------------------------|
| Lambda      | 1M invocations/month      |
| S3          | 5GB storage/month         |
| Glue        | 10 DPU hours/month        |
| EventBridge | 100k invocations/month    |

### Best Practices

- Use environment variables for API keys  
- Set CloudWatch alarms for failures  
- Implement S3 lifecycle rules for data retention




## 📄 11.Step-by-Step Deployment Instructions

### Step 1: Package the Lambda Function

```bash
cd godata2023/AWS\ Deployment
bash deploy/build_lambda_package.sh
```

This will:
- Copy `fetch_stock_data.py`
- Install `requests` and `boto3` into a temp folder
- Zip everything into `lambda_function.zip`

### Step 2: Deploy to AWS Lambda

```bash
bash deploy/deploy_lambda.sh
```

This script will:
- Create an IAM role and attach `lambda_iam_policy.json`
- Deploy the Lambda function using `lambda_function.zip`
- Set handler to `fetch_stock_data.lambda_handler`

### Step 3: IAM Role Permissions

Filename: `deploy/lambda_iam_policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

### Step 4: Schedule with EventBridge

```bash
bash deploy/create_eventbridge_rule.sh
```

This will:
- Create a 5-minute cron rule
- Authorize EventBridge to trigger your Lambda
- Set EventBridge target to your Lambda function

---

## 🧪 Optional: Run Glue Job for Batch Processing

If you want to clean and convert raw stock JSON data from S3:

```python
# glue_etl_job.py
from awsglue.context import GlueContext
from pyspark.context import SparkContext

glueContext = GlueContext(SparkContext.getOrCreate())
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://stock-raw-data/"]},
    format="json"
)
df_clean = df.drop_null_fields().drop_duplicates()
glueContext.write_dynamic_frame.from_options(
    frame=df_clean,
    connection_type="s3",
    connection_options={"path": "s3://stock-cleaned-data/"},
    format="parquet"
)
```

> ✅ Run this manually or set up Glue scheduling if needed.

---
## 🤝 12. Contribution
- Open issues for bugs or feature requests
- Submit PRs for enhancements or feedback

## 📄 13. License
Distributed under the MIT License. See `LICENSE` for full details.

## 📄 14. License
Distributed under the MIT License. See `LICENSE` for more details.
