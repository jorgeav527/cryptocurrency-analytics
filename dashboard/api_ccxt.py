import ccxt
import calendar
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st


# https://techflare.blog/how-to-get-ohlcv-data-for-your-exchange-with-ccxt-library/

# read .env file
load_dotenv()

# Connect the FTX-API with ccxt
exchange_id = "ftx"
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class(
    {
        "enableRateLimit": True,
        "apiKey": os.environ.get("APIKey"),
        "secret": os.environ.get("APISecret"),
    }
)


def min_ohlcv(dt, pair, limit):
    """
    This function is a recursive function that checks the minimum amount of data we are
    available to make.
    """
    since = calendar.timegm(dt.utctimetuple()) * 1000
    ohlcv1 = exchange.fetch_ohlcv(symbol=pair, timeframe="1m", since=since, limit=limit)
    ohlcv2 = exchange.fetch_ohlcv(symbol=pair, timeframe="1m", since=since, limit=limit)
    ohlcv = ohlcv1 + ohlcv2
    return ohlcv


def ohlcv(dt, pair, period="1d"):
    """
    This function handles the json data and converts it to a dataframe ready to be used for
    a Candlestick Graph. We don't have to worry about resolution, but we must have criteria
    to call the data.

    :dt: It is a list of two numbers that refer to the period of time e.g. [YYYYMMDD,YYYYMMDD]
    :pair: The market we are searching for e.g. BTC/USD
    :period: The frequency that the data is called by default, we use "1d".
    """
    ohlcv = []
    limit = 1000
    if period == "1m":
        limit = 720
    elif period == "1d":
        limit = 365
    elif period == "1h":
        limit = 24
    elif period == "5m":
        limit = 288
    for i in dt:
        start_dt = datetime.strptime(i, "%Y%m%d")
        since = calendar.timegm(start_dt.utctimetuple()) * 1000
        if period == "1m":
            ohlcv.extend(min_ohlcv(start_dt, pair, limit))
        else:
            ohlcv.extend(
                exchange.fetch_ohlcv(
                    symbol=pair, timeframe=period, since=since, limit=limit
                )
            )
    df = pd.DataFrame(ohlcv, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
    df["Time"] = [datetime.fromtimestamp(float(time) / 1000) for time in df["Time"]]
    df["Open"] = df["Open"].astype(np.float64)
    df["High"] = df["High"].astype(np.float64)
    df["Low"] = df["Low"].astype(np.float64)
    df["Close"] = df["Close"].astype(np.float64)
    df["Volume"] = df["Volume"].astype(np.float64)
    # df.set_index("Time", inplace=True)
    return df
