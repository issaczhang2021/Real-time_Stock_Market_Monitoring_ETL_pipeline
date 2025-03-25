import requests
import pandas as pd
import csv
from datetime import datetime
from api_factory import APIHandler
import json

# base_url = 'https://www.alphavantage.co/query?'

# apikey = ''  # access through home dir


params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'SHOP.TRT',
    'outputsize': 'full',
}

nvd_params = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': 'NVDA',
    'interval': '1min',
    'outputsize': 'full',
}

# def api_request(base_url, param_dict, api_key):
#     url = f'{base_url}function={param_dict.get("function")}&symbol={param_dict.get("symbol")}&outputsize={param_dict.get("outputsize")}&apikey={apikey}'
#     r = requests.get(url)
#     data = r.json()
#     return data


def normalize_events_to_csv(data):
    # Extract "Meta Data" values for header
    meta_data = list(data["Meta Data"].values())

    symbol = data["Meta Data"].get('2. Symbol', 'N/A')

    # Extract time series data, 2nd element of the dict
    body = data.get(list(data.keys())[1])

    enrich_events = []
    for date, dict_value in body.items():
        hashmap = {}
        dict_value['symbol'] = dict_value.get('symbol',symbol)
        dict_value['trade_timestamp'] = dict_value.get('trade_timestamp',date)
        enrich_events.append(dict_value)
    print(f'writing {len(enrich_events)} trade records to csv...')

    file_creation_time=datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path=f'/opt/spark/work-dir/godata2023/sample_files/trade_{file_creation_time}.csv'
    with open(file_path, "w") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "trade_timestamp",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ],
        )

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        for event in enrich_events:
            writer.writerow({
                "trade_timestamp": event["trade_timestamp"],
                "symbol": event["symbol"],
                "open": event["1. open"],
                "high": event["2. high"],
                "low": event["3. low"],
                "close": event["4. close"],
                "volume": event["5. volume"],
                
            })


if __name__ == '__main__':
    pass