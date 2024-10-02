"""
Create a Ticker object purely to store data
"""

from numpy.typing import ArrayLike
import numpy as np
import pandas as pd


class Ticker:
    """
    Ticker dataclass object to store ticker(e.g. AAPL, MSFT, IBM) data, using numpy arrays
    as the underlying objects
    """
    def __init__(self, name, data: ArrayLike, index: ArrayLike):
        self.name = name
        self.data = data
        self.index = index

    def __str__(self):
        """Return string representation of ticker object"""
        return (
            f"Ticker: {self.name}\n"
            f"Index: {self.index} dtype:{self.index.dtype}\n"
            f"Data: {self.data} dtype:{self.data.dtype}"
        )

    @property
    def name(self):
        """Get ticker name"""
        return self._name

    @name.setter
    def name(self, name):
        """Set ticker name"""
        self._name = name

    @property
    def data(self):
        """Get ticker data"""
        return self._data

    @data.setter
    def data(self, data):
        """Set ticker data, convert to numpy array if it is a Pandas object"""
        if isinstance(data, (pd.Series, pd.DataFrame)):
            self._data = data.to_numpy(dtype=float)
        else:
            self._data = np.array(data, dtype=float)

    @property
    def index(self):
        """Get ticker index, usually a timestamp"""
        return self._index

    @index.setter
    def index(self, index):
        """Set ticker index, usually a timestamp"""
        if isinstance(index, (pd.Series, pd.DataFrame)):
            self._index = index.to_numpy(dtype="datetime64")
        else:
            self._index = np.array(index)
