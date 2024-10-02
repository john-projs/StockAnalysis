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
import datetime

class Ticker:
    def __init__(self, name, data: ArrayLike, index: ArrayLike):
        self.name = name
        self.data = data
        self.index = index
        self._adjusted = None

    def __str__(self):
        return f"Ticker: {self.name}\nIndex: {self.index} dtype:{self.index.dtype}\nData: {self.data} dtype:{self.data.dtype}"

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
        if isinstance(data, (pd.Series, pd.DataFrame)):
            self._data = data.to_numpy(dtype=float)
        else:
            self._data = np.array(data, dtype=float)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if isinstance(index, (pd.Series, pd.DataFrame)):
            self._index = index.to_numpy(dtype="datetime64[D]")
        else:
            self._index = np.array(index)
