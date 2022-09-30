from multiprocessing import Value
import streamlit as st
import static
import api_ccxt
import pandas as pd
from datetime import date, datetime
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_icon=":dog:", layout="wide", initial_sidebar_state="auto")


def eda():
    """
    A simple exploratory EDA for each single bitcoin (ohlcv) using pandas_profiling
    report to get a good perspective of the data.
    """
    # Sidebar and options
    coin = st.sidebar.radio("Select a coin:", static.symbols_names)
    start_day = st.sidebar.date_input("Started Day", value=date(2022, 1, 1))
    end_day = st.sidebar.date_input("End Day", value=datetime.now())
    st.sidebar.markdown(
        "GitHub🔥 [jorgeav527-DTS03-PI03](https://github.com/jorgeav527/cryptocurrency-analytics.git)"
    )

    # Body
    st.title(f"EDA for {coin}", anchor="title")
    for key, value in static.symbols_descriptions.items():
        st.markdown(f"* {key}: {value}")
    frec = st.radio(
        "Choose the fecuence", static.frequency_keys, horizontal=True, index=5
    )
    # Let's create a df to generete the profile
    period = [start_day.strftime("%Y%m%d"), end_day.strftime("%Y%m%d")]
    df = api_ccxt.ohlcv(period, pair=f"{coin}/USD", period=f"{frec}")
    pr = ProfileReport(df, explorative=True)
    st_profile_report(pr)


if __name__ == "__main__":
    eda()
