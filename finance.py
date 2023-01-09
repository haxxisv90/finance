import requests, json, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AlphaVantage:

    def __init__(self, key):
        self.api_key = key

    def get_intraday(self, stock_symbol, time_interval_min, api_key):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" \
              f"{stock_symbol}&interval={time_interval_min}min&apikey={api_key}"
        raw_payload = requests.get(url, verify=False)
        if raw_payload.status_code == 200:
            return json.dumps(raw_payload.json(), indent=4)
        else:
            return f"HTTP Error: {raw_payload.status_code}"


    def get_daily_ts(self, stock_symbol, api_key):

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api_key}"
        raw_payload = requests.get(url, verify=False)


        # Parsing raw API return values into clean ones
        # .rsplit method used to separate the numbers from datatype "1. open" --> "open"
        ts_data_payload = dict(raw_payload.json()["Time Series (Daily)"])
        for date, datapoints in ts_data_payload.items():
            for datapoint_type in list(datapoints):
                datapoints[datapoint_type.rsplit(". ")[-1].capitalize()] = datapoints[datapoint_type]
                del datapoints[datapoint_type]

        return json.dumps(raw_payload.json(), indent=4), {"target": stock_symbol, "payload": ts_data_payload}


if __name__ == '__main__':
    pass

