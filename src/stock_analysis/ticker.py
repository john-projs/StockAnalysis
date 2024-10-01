"""
Create a Ticker object purely to store data
"""

import os
import sys
import warnings
from typing import Union
from numpy.typing import ArrayLike
import numpy as np
import pandas as pd


class Ticker:
    def __init__(
        self, name, data: ArrayLike, index: ArrayLike
    ):
        self._name = name
        self._data = data
        self._index = index
        self._adjusted = None

    def __str__(self):
        return f"Ticker: {self.name}\n{self.index}\n{self.data}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @staticmethod
    def dividend_ratio(dividend: float, closing_price: float):
        return 1 - (dividend / closing_price)

    def calc_adjusted_data(
        self,
        split_dates: ArrayLike,
        split_ratio: ArrayLike,
        dividend_dates: ArrayLike = None,
        dividends: ArrayLike = None,
    ) -> ArrayLike:
        adjusted_data = self._data

        # First apply Stock Split adjustment
        split_info = sorted(
            zip(split_dates, split_ratio), key=lambda x: x[0], reverse=True
        )
        for split in split_info:
            adjusted_data = np.where(
                self._index <= split[0], adjusted_data * (1 / split[1]), adjusted_data
            )

        # Apply Dividend adjustment
        dividend_info = sorted(
            zip(dividend_dates, dividends), key=lambda x: x[0], reverse=True
        )
        for dividend in dividend_info:
            ex_date_lags = np.argwhere(self._index <= dividend[0])
            # If no dates before dividend date, historical data does not extend far enough, break
            if len(ex_date_lags) == 0:
                break
            ex_date_lag_1 = np.max(np.argwhere(self._index <= dividend[0])) - 1
            dividend_ratio = self.dividend_ratio(
                dividend=dividend[1], closing_price=adjusted_data[ex_date_lag_1]
            )
            adjusted_data = np.where(
                self._index <= dividend[0],
                adjusted_data * dividend_ratio,
                adjusted_data,
            )
        self._adjusted = adjusted_data
        return adjusted_data
