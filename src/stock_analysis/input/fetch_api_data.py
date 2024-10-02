"""
Data module to fetch data from AlphaVantage API
"""
import os
import csv
from typing import Union

import requests


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
        datatype: str = "csv",
        interval: str = "",
        adjusted: str = "",
        truncate: bool = False,
    ):
        self.path = path
        self._api_url = api_url
        self._api_key = api_key
        self._function = function
        self._datatype = datatype
        self._interval = interval
        self._adjusted = adjusted
        self._truncate = "compact" if truncate else "full"

    @property
    def api_url(self):
        """Get api url"""
        return self._api_url

    @property
    def api_key(self):
        """Get api key"""
        return self._api_key

    @property
    def function(self):
        """Get function"""
        return self._function

    @property
    def datatype(self):
        """Get datatype"""
        return self._datatype

    @property
    def truncate(self):
        """Get truncate"""
        return self._truncate

    @property
    def interval(self):
        """Get interval"""
        return self._interval

    @property
    def adjusted(self):
        """Get interval"""
        return self._adjusted

    def create_request(self, ticker, month: str = None):
        """
        Create request for a ticker for a given month if applicable
        """
        _request = {
            "function": self.function,
            "symbol": ticker,
            "outputsize": self.truncate,
            "datatype": self.datatype,
            "apikey": self.api_key,
            "interval": self.interval,
            "month": month,
            "adjusted": self.adjusted
        }
        return _request

    def download_one_ticker(self, ticker: str, month: str = None) -> requests.Response:
        """
        Download data for one ticker, for a given month if specified

        Args:
            ticker: Ticker name to grab
            month: Month to grab

        Returns:
            Response from request for ticker data for one ticker
        """
        request = self.create_request(ticker, month)
        print("Requesting ticker ", ticker)
        payload = requests.get(self.api_url, request, timeout=1000)
        return payload

    # TODO: Create method to convert JSON objects to Pandas DataFrame
    @staticmethod
    def json_to_pandas(data: requests.Response):
        """Empty, add in future"""
        return data

    def write_ticker_data(self, payload: requests.Response, ticker: str, month: str = None) -> None:
        """
        Save ticker data from request.Response to path specified

        Args:
            payload: Response from API for ticker data
            ticker: Ticker name to grab
            month: Month to grab

        Returns:
            None, writes files locally

        """
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
            filedir = os.path.join(self.path, self.function.lower(), _month[1:])

            # Check if directory exists and create if needed
            if not os.path.exists(filedir):
                print(f"Creating file directory for {self.function.lower()}")
                os.makedirs(filedir)

            # Write out file to CSV
            filepath = os.path.join(filedir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                for line in payload.iter_lines():
                    writer.writerow(line.decode("utf-8").split(","))

    def download_single(self, ticker: Union[str, list], month: str = None) -> None:
        """

        Download single month for a ticker
        Args:
            ticker: Ticker(s) to grab
            month: Month to grab

        Returns:
            None, requests and saves ticker data to local path

        """
        if isinstance(ticker, str):
            payload = self.download_one_ticker(ticker, month)
            self.write_ticker_data(payload, ticker, month)
        elif isinstance(ticker, list):
            for _ticker in ticker:
                payload = self.download_one_ticker(_ticker, month)
                self.write_ticker_data(payload, _ticker, month)

    def download_all(self, ticker: Union[str, list], month: str = None):
        """
        Download all months for a ticker
        Args:
            ticker: Tickers(s) to grab
            month: Month(s) to grab

        Returns:
            None, requests and saves ticker data to local path
        """
        if isinstance(month, list):
            for _month in month:
                self.download_single(ticker, _month)
        elif isinstance(month, str):
            self.download_single(ticker, month)
        elif not month:
            self.download_single(ticker)
        print("Finished")
