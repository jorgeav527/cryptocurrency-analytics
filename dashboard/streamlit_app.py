from datetime import date, datetime
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas_ta as ta

import static
import api_ccxt

pio.renderers.default = "browser"
st.set_page_config(page_icon=":dog:", layout="wide", initial_sidebar_state="auto")


# Dashboard
def main_page():
    """
    This function displays:
    1. Image, title, sidebar and some options to get data.
    2. Metricks.
    3. Candlestick Graph
    4. Table Data
    """
    # Image
    image = Image.open("dashboard/image.jpg")
    st.image(image, width=650)
    st.title("TOP 10 Cryptocurrency FTX API", anchor="title")

    # Sidebar and options
    coin = st.sidebar.radio("Select a coin:", static.symbols_names)
    start_day = st.sidebar.date_input("Started Day", value=date(2022, 1, 1))
    end_day = st.sidebar.date_input("End Day", value=datetime.now())
    st.sidebar.markdown(
        "GitHub🔥 [jorgeav527-DTS03-PI03](https://github.com/jorgeav527/cryptocurrency-analytics.git)"
    )
    frec = st.radio(
        "Choose the fecuence", static.frequency_keys, horizontal=True, index=5
    )
    period = [start_day.strftime("%Y%m%d"), end_day.strftime("%Y%m%d")]

    # Let's create a dataframe with the helper module ccxt from api_ccxt
    df = api_ccxt.ohlcv(period, pair=f"{coin}/USD", period=f"{frec}")

    st.subheader("Metrics")
    col1, col2 = st.columns(2)
    # Adding the Rolling Average Close
    df["RAC"] = df["Close"].rolling(window=5, center=True).mean()

    # Let's crete some metris or KPIs
    kpis = pd.DataFrame(api_ccxt.exchange.markets[f"{coin}/USD"])
    col1.metric("variance".capitalize(), round(np.var(df["Close"]), 2))
    col1.metric("price".capitalize(), kpis["info"]["price"])
    col1.metric("change in 1h".capitalize(), kpis["info"]["change1h"])
    col1.metric("change in 24h".capitalize(), kpis["info"]["change24h"])
    col2.metric("quote volume in 24h".capitalize(), kpis["info"]["quoteVolume24h"])
    col2.metric("volume usd in 24h".capitalize(), kpis["info"]["volumeUsd24h"])
    col2.metric("price high in 24h".capitalize(), kpis["info"]["priceHigh24h"])
    col2.metric("price low in 24h".capitalize(), kpis["info"]["priceLow24h"])

    # Let's crete a Candlestick Graph with plotly
    st.subheader("Candlestick Graph")
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f"{coin} Stock Price Chart", "Volume Chart"),
        row_heights=[200, 50],
    )
    fig.add_trace(
        go.Candlestick(
            x=df["Time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Time"],
            y=df["RAC"],
            line=dict(color="black", width=2, dash="dot"),
            name="RAC",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=df["Time"],
            y=df["Volume"],
            marker=dict(color=df["Volume"], colorscale="Cividis_r"),
            name="Volumen",
        ),
        row=2,
        col=1,
    )
    fig["layout"]["xaxis2"]["title"] = "Time"
    fig["layout"]["yaxis"]["title"] = "Price"
    fig["layout"]["yaxis2"]["title"] = "Volume"
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_xaxes(rangeslider_visible=False)

    st.plotly_chart(fig, use_container_width=True)

    # Let's show some table descriptions and if it is necessary, show the whole table.
    st.subheader("Table Data")
    st.dataframe(df.iloc[:, :-1].describe())
    if st.checkbox("Show data"):
        st.dataframe(df)


if __name__ == "__main__":
    main_page()
