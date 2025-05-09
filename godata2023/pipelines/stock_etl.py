from etl_utils import setup_spark_session, ingest_data_to_delta, read_data_from_delta, deduplication,run_data_validations
from transform import stock_events_normalizer
from api_utils.api_factory import APIHandler
from dq_utils import spark_scan
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql.functions import col, current_timestamp, expr, lit, to_date, monotonically_increasing_id, to_timestamp
from pyspark.sql import DataFrame, SparkSession


company_params = [
    {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': 'NVDA',
        'interval': '1min',
        'outputsize': 'full',
    },
    # {
    #     'function': 'TIME_SERIES_INTRADAY',
    #     'symbol': 'TSLA',
    #     'interval': '1min',
    #     'outputsize': 'full',
    # },
    # {
    #     'function': 'TIME_SERIES_INTRADAY',
    #     'symbol': 'IBM',
    #     'interval': '1min',
    #     'outputsize': 'full',
    # },
    # {
    #     'function': 'TIME_SERIES_INTRADAY',
    #     'symbol': 'AAPL',
    #     'interval': '1min',
    #     'outputsize': 'full',
    # },
]

# entry point for calling stock-etl during deployment
if __name__ == '__main__':
    spark = setup_spark_session()
    for param in company_params:
        trade_api = APIHandler(request_params=param)
        api_endpoint = trade_api.get_endpoint()
        data = trade_api.request_data(api_endpoint)
        df = stock_events_normalizer(data, spark)
        spark_scan(df, spark, "trade")
        ingest_data_to_delta(df, "trade")
