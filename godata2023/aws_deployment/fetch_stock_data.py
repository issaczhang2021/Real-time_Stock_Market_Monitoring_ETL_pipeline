import os
import json
import boto3
import requests


def _get_api_key() -> str:
    """Read API key from environment variable or config file."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if api_key:
        return api_key
    config_path = os.path.join(
        os.path.dirname(__file__), '..', 'config', 'config.ini'
    )
    if os.path.exists(config_path):
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)
        return config.get('API', 'api_key')
    raise ValueError('API key not provided')


def fetch_stock_data(symbol: str, interval: str = '1min') -> dict:
    """Fetch stock data from Alpha Vantage."""
    api_key = _get_api_key()
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'outputsize': 'compact',
        'apikey': api_key,
    }
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def upload_to_s3(data: dict, bucket: str, prefix: str, symbol: str) -> None:
    s3 = boto3.client('s3')
    key = f"{prefix}/{symbol}/{int(__import__('time').time())}.json"
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data))


def lambda_handler(event, context):
    symbol_list = os.getenv('SYMBOL_LIST', 'NVDA').split(',')
    bucket = os.getenv('RAW_BUCKET', 'stock-raw-data')
    prefix = os.getenv('PREFIX', 'events')
    for symbol in symbol_list:
        data = fetch_stock_data(symbol.strip())
        upload_to_s3(data, bucket, prefix, symbol.strip())
    return {'status': 'ok', 'symbols': symbol_list}
