# cryptocurrency-analytics

![alt text](dashboard/image.jpg)

Get information from the FTX API and get into the world of Crypto.

* This app is a basic intro to cryptocurrency. We are connecting to the API using ccxt for its simplicity to retrieve data. 
* We are creating a simple candlestick graph to read the stock market for each coin in a period of time. 
* We are checking for each crypto coin and creating a basic EDA report with the help of pandas-profiling.
* On the calculator tab, you can use the Bitcoin calculator to know the currency between Bitcoins.
* We are using the following digital coins "BTC", "ETH", "XRP", "SOL", "LTC", "USDT", "ETHW", "BNB", "DOGE", "ATOM".


## How to run the code?

* You'll need to fork and clone the repo.
* Create a env with `python3 -m venv ./venv` we also can use conda [conda](https://docs.conda.io/en/latest/). and them let's install the requirements as follows `pip install -r requeriments/dev.txt`.
* To activate venv `source venv/bin/activate`.
* Run jupyter `jupyter-notebook`.
* To deactivate `deactivate`.

This app is built on the top of
* numpy
* pandas
* matplotlib
* python
* plotly
* streamlit
* Pillow
* ccxt
* pandas-profiling
* streamlit-pandas-profiling

### + Info
### + Info
* [How to create a virtual enviroment in python](https://www.machinelearningplus.com/deployment/conda-create-environment-and-everything-you-need-to-know-to-manage-conda-virtual-environment/)
* [How to use the API credentials to connect to CCXT and retrieve data.](https://techflare.blog/how-to-get-ohlcv-data-for-your-exchange-with-ccxt-library/)
* [How to use pandas profiling to render EDA basic reports.](https://pypi.org/project/pandas-profiling/)

<img src = "https://user-images.githubusercontent.com/96025598/188937586-28575753-fbd6-42de-beca-81ae35b659e0.gif" height = 300>