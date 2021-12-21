import streamlit as st
import yfinance as yf
import datetime
from PIL import Image

st.write("""
# Simple Stock Price App

Shown are the stock closing price and volume! 
""")
# cheat sheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
# http://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
# how to deploy your websitre https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app

image = Image.open("StockPicture.jfif")
st.image(image, use_column_width=True)

# define the ticker symbol
# https://stockanalysis.com/stocks/
tickerSymbol = st.text_input("Enter your stock", max_chars=10)

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
StartDate = st.date_input("Select the start date", value = datetime.date(1995, 6, 15), 
                        min_value = datetime.date(1990, 1, 1), 
                        max_value = datetime.date(2050, 12, 31))
EndDate = st.date_input("Select the end date", value = datetime.date(1995, 6, 15), 
                        min_value = datetime.date(1990, 1, 1), 
                        max_value = datetime.date(2050, 12, 31))
tickerDf = tickerData.history(period='1d',start = StartDate, end = EndDate)
# Open                   High                  Low Close                  Volume                 Dividends              Stock Splits

if tickerSymbol:
    st.write("""
    ### Closing Price 
    """)
    st.line_chart(tickerDf.Close)

    st.write("""
    ### Volume Price 
    """)
    st.line_chart(tickerDf.Volume)