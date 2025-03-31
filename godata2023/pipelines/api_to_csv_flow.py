from api_utils.api_factory import APIHandler
from api_utils.get_api_data import normalize_events_to_csv
from prefect import flow, task
from typing import Optional

DEFAULT_PARAMS = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': 'NVDA',
    'interval': '1min',
    'outputsize': 'full',
}

## task
# get stock data
@task
def get_stock_data(stock_params: dict):
    trade_api = APIHandler(request_params=stock_params)
    api_endpoint = trade_api.get_endpoint()
    data = trade_api.request_data(api_endpoint)
    return data

# load to csv
@task
def save_to_csv(data: dict):
    normalize_events_to_csv(data)

## flow
# create a flow
@flow
def ingest_api_data_to_csv(stock_params: Optional[dict]=DEFAULT_PARAMS):
    data = get_stock_data(stock_params)
    save_to_csv(data)

if __name__ == "__main__":
    ingest_api_data_to_csv.serve(name="prefect-stock-api-to-csv-deployment", cron="0 0 * * *")