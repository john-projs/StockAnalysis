import os, sys, json, requests, csv

import pandas as pd
import numpy as np

from typing import Union


class FetchAPIData:
    """
    Helper class to fetch and write data from AlphaVantage's API and save locally
    """

    def __init__(
        self,
        path: str,
        function: str,
        api_url: str,
        api_key: str,
        datatype: str,
        interval: str,
        truncate: bool = False,
    ):
        self.path = path
        self._api_url = api_url
        self._api_key = api_key
        self._function = function
        self._datatype = datatype
        self._interval = interval
        self._truncate = "compact" if truncate else "full"

    @property
    def api_url(self):
        return self._api_url

    @property
    def function(self):
        return self._function

    @property
    def datatype(self):
        return self._datatype

    @property
    def truncate(self):
        return self._truncate

    @property
    def interval(self):
        return self._interval

    def api_key(self):
        with open("api_key.txt") as f:
            api_key = f.read()
        return api_key

    def create_request(self, ticker, month: str = None):
        # Pull user api key
        api_key = self.api_key()
        _request = {
            "function": self.function,
            "symbol": ticker,
            "outputsize": self.truncate,
            "datatype": self.datatype,
            "apikey": api_key,
            "interval": self.interval,
            "month": month,
        }
        return _request

    def download_one_ticker(self, ticker: str, month: str = None):
        request = self.create_request(ticker, month)
        print("Requesting ticker ", ticker)
        payload = requests.get(self.api_url, request)
        return payload

    def json_to_pandas(self, data):
        return None

    def write_ticker_data(self, payload, ticker, month: str = None):
        if self.datatype == "json":
            data = payload.json()
            self.json_to_pandas(data)
        elif self.datatype == "csv":
            # Create nice name and place for files
            if month:
                _month = "_" + month.replace("-", "M")
            else:
                _month = ""

            filename = "historical_ticker_" + ticker + _month + ".csv"
            filedir = os.path.join(path, self.function.lower(), _month[1:])

            # Check if directory exists and create if needed
            if not os.path.exists(filedir):
                print(f"Creating file directory for {self.function.lower()}")
                os.makedirs(filedir)

            # Write out file to CSV
            filepath = os.path.join(filedir, filename)
            with open(filepath, "w") as f:
                writer = csv.writer(f)
                for line in payload.iter_lines():
                    writer.writerow(line.decode("utf-8").split(","))

    def download_single(self, ticker, month: str = None):
        if isinstance(ticker, str):
            payload = self.download_one_ticker(ticker, month)
            self.write_ticker_data(payload, ticker, month)
        elif isinstance(ticker, list):
            for _ticker in ticker:
                payload = self.download_one_ticker(_ticker, month)
                self.write_ticker_data(payload, _ticker, month)

    def download_all(self, ticker, month: str = None):
        if isinstance(month, list):
            for _month in month:
                self.download_single(ticker, _month)
        elif isinstance(month, str):
            self.download_single(ticker, month)
        elif not month:
            self.download_single(ticker)
        print("Finished")


if __name__ == "__main__":
    path = ""
    function = "TIME_SERIES_DAILY"
    api_url = "https://www.alphavantage.co/query?"
    api_key = ""
    ticker = ["MSFT", "IBM"]
    datatype = "csv"
    interval = "1min"
    month = None

    dp = FetchAPIData(
        path=path,
        function=function,
        api_url=api_url,
        api_key=api_key,
        datatype=datatype,
        interval=interval,
    )
    dp.download_all(ticker, month)
