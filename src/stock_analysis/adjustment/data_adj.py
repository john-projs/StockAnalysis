"""
Perform data adjustment to account for stock splits and dividends
"""
from numpy.typing import ArrayLike
import numpy as np
from stock_analysis.ticker import Ticker


def adjust_ticker(
    ticker: Ticker,
    split_dates: ArrayLike,
    split_ratio: ArrayLike,
    dividend_dates: ArrayLike = None,
    dividends: ArrayLike = None,
) -> Ticker:
    adjusted_data = ticker.data

    # First apply Stock Split adjustment
    split_info = sorted(zip(split_dates, split_ratio), key=lambda x: x[0], reverse=True)
    for split in split_info:
        adjusted_data = np.where(
            ticker.index <= split[0], adjusted_data * (1 / split[1]), adjusted_data
        )

    # Apply Dividend adjustment
    dividend_info = sorted(
        zip(dividend_dates, dividends), key=lambda x: x[0], reverse=True
    )
    for dividend in dividend_info:
        ex_date_lags = np.argwhere(ticker.index <= dividend[0])
        # If no dates before dividend date, historical data does not extend far enough, break
        if len(ex_date_lags) == 0:
            break
        ex_date_lag_1 = np.max(np.argwhere(ticker.index <= dividend[0])) - 1
        closing_price = float(adjusted_data[ex_date_lag_1])
        dividend_ratio = get_dividend_ratio(
            dividend=dividend[1], closing_price=closing_price
        )
        adjusted_data = np.where(
            ticker.index <= dividend[0],
            adjusted_data * dividend_ratio,
            adjusted_data,
        )

    ticker_adj = Ticker(ticker.name+"_adj", adjusted_data, ticker.index)
    return ticker_adj


def get_dividend_ratio(dividend: float, closing_price: float):
    return 1 - (dividend / closing_price)
