
# 🧭 AWS Deployment for Real-Time Stock ETL Pipeline

This document describes how to deploy the `Real-time_Stock_Market_Monitoring_ETL_pipeline` on AWS to support **1-minute interval real-time data ingestion**, using a fully managed, serverless architecture.

---

## 🧠 Why Use AWS Serverless for This Project?

### ✅ Real-Time Data Capture
- Continuously fetch updated stock prices every **minute** from public APIs (e.g., Alpha Vantage).
- Immediately store and track market insights with low latency.

### ✅ Cost-Effective
- Use **AWS Free Tier**: Lambda, S3, EventBridge, Glue (all have generous free limits).

### ✅ Scalable & Serverless
- No infrastructure to manage.
- Fully managed execution, monitoring, and scaling handled by AWS.

---

## 🧱 Architecture Overview

```
EventBridge (Every 1 min)
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

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Package the Lambda Function

```bash
cd godata2023/AWS\ Deployment
bash deploy/build_lambda_package.sh
```

This will:
- Copy `fetch_stock_data.py`
- Install `requests` and `boto3` into a temp folder
- Zip everything into `lambda_function.zip`

---

### Step 2: Deploy to AWS Lambda

```bash
bash deploy/deploy_lambda.sh
```

This script will:
- Create an IAM role and attach `lambda_iam_policy.json`
- Deploy the Lambda function using `lambda_function.zip`
- Set handler to `fetch_stock_data.lambda_handler`

---

### Step 3: IAM Role Permissions

**deploy/lambda_iam_policy.json**

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

---

### Step 4: Schedule with EventBridge

```bash
bash deploy/create_eventbridge_rule.sh
```

This will:
- Create a 1-minute cron rule
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

## 🔎 Monitoring

- Lambda Logs: **CloudWatch → /aws/lambda/StockDataFetcher**
- Scheduled Rule: **Amazon EventBridge → Rules**
- Glue Logs: **AWS Glue → Jobs → Run history**

---

## 💰 Cost Summary

| Service     | Free Tier                   |
|-------------|-----------------------------|
| Lambda      | 1M invocations/month         |
| S3          | 5GB storage/month            |
| Glue        | 10 DPU hours/month           |
| EventBridge | 100k invocations/month       |

---

## 🧼 Best Practices

- Use environment variables for API keys (e.g., Alpha Vantage)
- Alert on Lambda failures using CloudWatch Alarms
- Set lifecycle rules on your S3 bucket to manage old raw data

---

For help or questions, open an issue or contact [@issaczhang2021](https://github.com/issaczhang2021).
