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
    symbol = data["Meta Data"].get('2. Symbol', 'N/A')

    # Extract time series data, 2nd element of the dict
    body = data.get(list(data.keys())[1])

    enrich_events = []
    for date, dict_value in body.items():
        dict_value['symbol'] = dict_value.get('symbol', symbol)
        dict_value['trade_timestamp'] = dict_value.get('trade_timestamp', date)
        enrich_events.append(dict_value)

    df_raw = spark.createDataFrame(enrich_events)
    # type casting
    df = df_raw.select(
        df_raw["trade_timestamp"]
        .cast(TimestampType())
        .alias("trade_timestamp"),
        df_raw["symbol"].cast(StringType()).alias("symbol"),
        df_raw["`1. open`"].cast(DoubleType()).alias("open"),
        df_raw["`2. high`"].cast(DoubleType()).alias("high"),
        df_raw["`3. low`"].cast(DoubleType()).alias("low"),
        df_raw["`4. close`"].cast(DoubleType()).alias("close"),
        df_raw["`5. volume`"].cast(IntegerType()).alias("volume"),
    )

    batch_id = current_timestamp().cast("long")
    df = df.withColumn("partition", to_date("trade_timestamp").cast("string"))
    df = df.withColumn("batch_id", lit(batch_id))
    # Show the DataFrame for testing
    # df.show()
    return df