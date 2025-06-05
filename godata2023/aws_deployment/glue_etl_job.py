import sys
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['RAW_BUCKET', 'CLEAN_BUCKET', 'PREFIX'])

sc = SparkContext()
ctx = GlueContext(sc)

raw_path = f"s3://{args['RAW_BUCKET']}/{args['PREFIX']}"
clean_path = f"s3://{args['CLEAN_BUCKET']}/cleaned"

# Read raw JSON files
df = ctx.spark_session.read.json(raw_path)

# Basic cleaning
clean_df = df.dropna().dropDuplicates()

# Write to Parquet
clean_df.write.mode('append').parquet(clean_path)
