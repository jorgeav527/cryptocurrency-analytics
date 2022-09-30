import streamlit as st
import static
import api_ccxt
import pandas as pd

st.set_page_config(page_icon=":dog:", layout="wide", initial_sidebar_state="auto")


def calculator():
    """
    This function gets two coins selected in the sidebar then generate de dataframe
    for each coin then we convert an inputed value to some other currency by the rate
    funtion.
    rate = from_coin_price / to_coin_price
    converted_amount = amount * rate
    """

    # Sidebar
    coin_01 = st.sidebar.selectbox(
        "Convert:",
        static.symbols_names,
        key="coin_01",
        index=0,
    )
    coin_02 = st.sidebar.selectbox(
        "To",
        static.symbols_names,
        key="coin_02",
        index=0,
    )
    market_coin_01 = pd.DataFrame(api_ccxt.exchange.markets[f"{coin_01}/USD"])
    market_coin_02 = pd.DataFrame(api_ccxt.exchange.markets[f"{coin_02}/USD"])

    # Body
    st.title("Currency Converter")
    col1, col2 = st.columns(2)
    amount = col1.number_input(
        f"Amount to Comvert ({coin_01})", min_value=0.0, value=1.0
    )

    if coin_01 == coin_02:
        return col2.metric(f"Converted ({coin_02})", amount)
    else:
        rate = float(market_coin_01["info"]["price"]) / float(
            market_coin_02["info"]["price"]
        )
        return col2.metric(f"Converted ({coin_02})", amount * rate)


if __name__ == "__main__":
    calculator()
