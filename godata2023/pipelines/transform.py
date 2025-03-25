import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession
from datetime import datetime
from pyspark.sql.functions import col, current_timestamp, expr, lit, to_date, monotonically_increasing_id, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
import json

# def trade_volume_aggregator(df):

def stock_events_normalizer(data: dict, spark: SparkSession):
    """
    take stock events and process into df
    """
    pass