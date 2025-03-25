from etl_utils import ingest_data_to_delta, read_data_from_delta, deduplication,run_data_validations
from transform import stock_events_normalizer
from api_utils.api_factory import APIHandler
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql.functions import col, current_timestamp, expr, lit, to_date, monotonically_increasing_id, to_timestamp
from pyspark.sql import DataFrame, SparkSession

nvd_params = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': 'NVDA',
    'interval': '1min',
    'outputsize': 'full',
}

# entry point for calling stock-etl during deployment
if __name__ == '__main__':
    spark = (
        SparkSession.builder.appName("godata2023")
        .enableHiveSupport()
        .getOrCreate()
    )
    print('Welcome to godata2023 DE project!!!')
    pass