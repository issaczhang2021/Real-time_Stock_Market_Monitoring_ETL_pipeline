import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession
from datetime import datetime
from pyspark.sql.functions import col, current_timestamp, expr, lit, to_date, monotonically_increasing_id, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
import json
from soda.scan import Scan
import boto3
from botocore.client import Config

def ingest_data_to_delta(
    load_df,
    table_name: str,
    mode='append',
    storage_path='s3a://godata2023/delta'):
    # Write DataFrame to Delta format
    delta_output_path = f"{storage_path}/{table_name}"
    load_df.write.format('delta').mode(mode).save(delta_output_path)
    print(f"data ingested to delta table: {delta_output_path}")

def read_data_from_delta(
    table_name: str,
    spark: SparkSession,
    filter_condition: str = None,
    storage_path='s3a://godata2023/delta'
    ):
    if filter_condition:
        df = (
            spark.read.format("delta")
            .load(f"{storage_path}/{table_name}")
            .filter(filter_condition)
        )
    else:
        df = spark.read.format("delta").load(f"{storage_path}/{table_name}")
    return df


def deduplication(table_name: str, spark: SparkSession, filter_condition: str=None, storage_path='s3a://godata2023/delta'):
    pass


def run_data_validations(
        df,
        data_asset_name: str,
        root_dir: str='/opt/spark/work-dir/godata2023/data_quality',
    ):
    pass

def push_to_s3(
    file_path,
    object_name,
    minio_url='http://minio:9000',
    access_key='godata2023',
    secret_key='godata2023',
    bucket_name='godata2023',
):
    s3_client = boto3.client(
        's3',
        endpoint_url=minio_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(
            f"File {file_path} uploaded successfully to"
            f" {bucket_name}/{object_name}"
        )
    except Exception as e:
        print(f"Error uploading file: {e}")
    
    
def setup_spark_session():
    spark = SparkSession.builder \
    .appName("godata2023") \
    .master('local[*]') \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2") \
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.access.key", "godata2023") \
    .config("spark.hadoop.fs.s3a.secret.key", "godata2023") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.region", "us-east-1") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .enableHiveSupport() \
    .getOrCreate()
    return spark