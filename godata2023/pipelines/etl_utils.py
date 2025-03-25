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

def ingest_data_to_delta(
    load_df,
    table_name: str,
    mode='append',
    storage_path='s3a://godata2023/delta'):
    # Write DataFrame to Delta format
    pass

def read_data_from_delta(
    table_name: str,
    spark: SparkSession,
    filter_confition: str=None,
    storage_path='s3a://godata2023/delta'
    ):
   pass


def deduplication(table_name: str, spark: SparkSession, filter_condition: str=None, storage_path='s3a://godata2023/delta'):
    pass


def run_data_validations(
        df,
        data_asset_name: str,
        root_dir: str='/opt/spark/work-dir/godata2023/data_quality',
    ):
    pass
    
    
