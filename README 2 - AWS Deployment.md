
# 🧭 AWS Deployment for Real-Time Stock ETL Pipeline

This document describes how to deploy the `Real-time_Stock_Market_Monitoring_ETL_pipeline` on AWS to support **1-minute interval real-time data ingestion**, using a fully managed, serverless architecture.

---

## 🧠 Why Use AWS Serverless for This Project?

### ✅ Real-Time Data Capture

- You want to **fetch the most recent stock prices every minute** and make them immediately available for analytics or alerting.

### ✅ Cost-Effective

- With **AWS Free Tier**, most services like Lambda, S3, EventBridge, and Glue offer generous free limits.

### ✅ Scalability & Resilience

- Lambda functions scale automatically with traffic and fail independently.
- S3 ensures durable storage and integrates easily with analytics tools.

### ✅ No Server Management

- No need to manage EC2, cron jobs, or daemons. AWS services handle infrastructure concerns automatically.

---

## 🧱 Architecture Overview

```
EventBridge (Every 1 min)
       ↓
 AWS Lambda (fetch_stock_data.py)
       ↓
Stock Market API (e.g., Alpha Vantage)
       ↓
Amazon S3 (Raw JSON: stock-raw-data/)
       ↓
(Optional) AWS Glue Job
       ↓
Amazon S3 (Cleaned Parquet: stock-cleaned-data/)
       ↓
Downstream: Power BI, QuickSight, Athena
```

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Package the Lambda Function

**Potential issue**: Lambda has a size limit (50MB zipped). If your `fetch_stock_data.py` uses external libraries like `requests`, you must package them properly.

```bash
mkdir lambda_package
cp fetch_stock_data.py lambda_package/
pip install requests -t lambda_package/
cd lambda_package
zip -r ../lambda_function.zip .
```

> ✅ **Tip**: Use Docker-based builds if you need to support native binaries (e.g., `pandas`, `numpy`).

---

### Step 2: Deploy to AWS Lambda

```bash
aws lambda create-function   --function-name StockDataFetcher   --runtime python3.9   --role arn:aws:iam::<your-account-id>:role/<lambda-role>   --handler fetch_stock_data.lambda_handler   --zip-file fileb://lambda_function.zip
```

> ✅ **Tip**: You must create the IAM role with proper policies first (see below).

---

### Step 3: IAM Role Permissions

Attach this policy to your Lambda IAM Role:

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

**Potential issue**: Without the correct permissions, Lambda will silently fail or log `AccessDenied` errors. Check CloudWatch Logs for troubleshooting.

---

### Step 4: Schedule Lambda with EventBridge

```bash
# Create a 1-minute trigger
aws events put-rule   --name FetchStockDataEveryMinute   --schedule-expression "rate(1 minute)"

# Give EventBridge permission to invoke Lambda
aws lambda add-permission   --function-name StockDataFetcher   --statement-id EventBridgePermission   --action lambda:InvokeFunction   --principal events.amazonaws.com   --source-arn arn:aws:events:<region>:<account-id>:rule/FetchStockDataEveryMinute

# Set the EventBridge rule to target Lambda
aws events put-targets   --rule FetchStockDataEveryMinute   --targets "Id"="1","Arn"="arn:aws:lambda:<region>:<account-id>:function:StockDataFetcher"
```

> ✅ **Tip**: Test with manual `Invoke` first before automating with EventBridge.

---

## 🧪 Optional: Glue Job for Downstream Processing

When your raw data accumulates in S3, you can use AWS Glue to:

- Clean missing fields
- Convert JSON to Parquet
- Partition data for faster analytics

### Sample Glue Script (`glue_etl_job.py`)

```python
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

> **Potential issue**: Glue's default IAM role must have `S3:Read/Write` permissions for both raw and cleaned paths.

---

## 🔎 Monitoring & Debugging

- View function logs in **CloudWatch → Log Groups → /aws/lambda/StockDataFetcher**
- Use **`test event`** in Lambda console for manual runs
- Monitor scheduled triggers in **EventBridge > Rules > Metrics**

---

## 💰 Cost Consideration

| Service     | AWS Free Tier                   |
|-------------|----------------------------------|
| Lambda      | 1 million free invocations/month |
| S3          | 5 GB standard free storage       |
| Glue        | 10 free DPU hours/month          |
| EventBridge | 100,000 invocations/month        |

---

## 🧼 Best Practices

- Rotate your API keys securely with Secrets Manager or Lambda env variables
- Implement deduplication in case the same data is fetched twice
- Consider alerting if API response fails or returns null

---

For questions or suggestions, feel free to open an issue or contact [@issaczhang2021](https://github.com/issaczhang2021).
