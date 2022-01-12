import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import time #format some variable
import requests
from PIL import Image
import bs4
import datetime

st.write("""
# Simple Stock Price App
""")

st.title('S&P 500')

image = Image.open("StockPicture.jfif")
st.image(image, use_column_width=True)


st.markdown("""
    This website retrieves the list of the S&P 500 and its corresponding **stock closing price** (year-to-data)!        
        * **Data source:**[Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).    
            """)
st.sidebar.header('User Input Features')

@st.cache
def data_load():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    #we only want the first table
    df = html[0]
    return df

df = data_load()
#type of company
sector = df.groupby('GICS Sector')

#soreted sector and we will list them in the sidebar
sorted_unique_sector = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_unique_sector, sorted_unique_sector)

#filtering data
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

# https://pypi.org/project/yfinance/


st.write("Display Companies in Selected Sector")
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and '+ str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)
    
# streamlit run .\StockPrice.py

########################################################################

st.write(" ## Enter the Stock to see its change over time")
# cheat sheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
# http://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
# how to deploy your websitre https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app

# define the ticker symbol
# https://stockanalysis.com/stocks/

data = yf.download(
        tickers = list(df_selected_sector[:501].Symbol),
        period = "ytd",
        interval = "1wk",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )
def price_plot_high(company):
    df = pd.DataFrame(data[company].High)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.High, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.High, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(company, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('High Price', fontweight='bold')
    return st.pyplot()

def price_plot_low(company):
    df = pd.DataFrame(data[company].Low)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Low, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Low, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(company, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Low Price', fontweight='bold')
    return st.pyplot()

def price_plot_close(company):
    df = pd.DataFrame(data[company].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(company, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Close Price', fontweight='bold')
    return st.pyplot()

tickerSymbol = st.text_input("Enter your stock", max_chars=10)
page_names = ['High', 'Low', 'Closed']
page = st.radio('Select an option', page_names)
st.write("**The variable 'page' returns:**", page)
if page == 'High':
    for i in list(df_selected_sector.Symbol):
        if i == tickerSymbol:
            price_plot_high(i)
            
if page == 'Low':
    for i in list(df_selected_sector.Symbol):
        if i == tickerSymbol:
            price_plot_low(i)

if page == 'Closed':
    for i in list(df_selected_sector.Symbol):
        if i == tickerSymbol:
            price_plot_close(i)

def getWeather(fieldtext):
    #get the input from the user
    city = fieldtext
    #api from the website, 2 inputs: api key and the city
    api ="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=12d02cb722709709e0889db756957fca"
    #JSON is a syntax for storing and exchanging data.
    # https://www.delftstack.com/howto/python/python-get-json-from-url/#:~:text=Get%20and%20Access%20JSON%20Data%20in%20Python%201,format.%20...%203%20Access%20the%20JSON%20Data.%20
    # The first step we have to perform here is to fetch the JSON data using the requests library.
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] -273.15)
    min_temp = int(json_data['main']['temp_min'] -273.15)   
    max_temp = int(json_data['main']['temp_max'] -273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['pressure']
    wind_speed = json_data['wind']['speed']
    #strftime: Convert a time tuple to a string according to a format specification
    # %I:%M:%M: hours minute seconds in 12 hour format
    # %H:%M:%M: hours minute seconds in 24 hour format
    sunrise = time.strftime("%I:%M:%M", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%H:%M:%M", time.gmtime(json_data['sys']['sunset'] - 21600))
    
    #we will define two strings to carry our data
    final_data = condition + "\n" + str(temp) + "°C" + ", Max Temp: " + str(max_temp) +  ", Min Temp: " + str(min_temp) +  ", Pressure: " + str(pressure) +  ", Humidity: " + str(humidity) +  ", Wind Speed: " + str(wind_speed) + ", Sun Rise: " + str(sunrise)  + ", Sun Set: " + str(sunset) 
    
    #config is used to access an object's attributes after its initialisation.
    # config is used to access an object's attributes after its initialisation. For example, here, you define
    # l = Label(root, bg="ivory", fg="darkgreen")
    # but then you want to set its text attribute, so you use config:
    #l.config(text="Correct answer!")
    return final_data

def get_html_data(url):
    data = requests.get(url)
    return data

#get the request url
def get_covid_data():
    # web browser is now a client
    # server is url
    url = "https://www.worldometers.info/coronavirus/"
    #request response protocol: "get" request. You are requesting data from the server
    #https://www.youtube.com/watch?v=pHFWGN-upGM&ab_channel=Udacity
    html_data = get_html_data(url)
    #use bs4 to beutify our data
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    #this is how we find the data in a html file, we find the covid cases
    #content inner is the whole content info of the website
    #then we will locate the child of the conten-inner which is the maincounter wrap
    info_div = bs.find("div", class_ ="content-inner").findAll("div", id="maincounter-wrap")
    all_data =""
    
    #our task is to find the amount of deaths and recovered => we will find each separately
    #each info (#deaths and #recovered) is stored as a block
    #a block is a piece of Python program text that is executed as a unit
    for block in info_div:
        #Coronavirus cases is in the h1, so we will find the info in h1
        text = block.find("h1", class_ = None).get_text()
        
        count = block.find("span", class_ = None).get_text()
        
        all_data = all_data + text + " " +  count + ". "
    return all_data

def reload():
    new_data = get_covid_data()
    return new_data

#get a random country details  
def get_country_data():
    name = country123
    text = "Country not found"
    url = "https://www.worldometers.info/coronavirus/country/"+name
    html_data = get_html_data(url)
    #use bs4 to beutify our data
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_ ="content-inner").findAll("div", id="maincounter-wrap")
    all_data =""
    if html_data == None:
        st.sidebar.write("Error")
    #because there is three values that we are looking for so we make a loop
    for i in range(3):
        text = info_div[i].find("h1", class_ = None).get_text()
        
        count = info_div[i].find("span", class_ = None).get_text()
        
        all_data = all_data + text + " " +  count + ". "
        
    return all_data

# add button2 within the button1 and make it to work: https://discuss.streamlit.io/t/button-inside-button/12046/4
# https://www.youtube.com/watch?v=EnXJBsCIl_A&t=29s&ab_channel=Streamlit

original_list = ['Select options','Covid Tracking', 'Weather']
option = st.sidebar.selectbox('What options would you like to pick?', original_list)
if option != 'Select options':
    st.sidebar.write('You selected: ', option)
    if option == 'Covid Tracking':
        st.sidebar.write(get_covid_data())
        button2 = st.sidebar.checkbox("Reload")
        button3 = st.sidebar.checkbox("Get Data")
        if button2:
            st.sidebar.write(reload())
        if button3:
            country123 = st.sidebar.text_input("Enter the country you want to check")
            if country123:
                st.sidebar.write("The data for the country", country123, ":")
                st.sidebar.write(get_country_data())
            
    if option == 'Weather':
        fieldtext1 = st.sidebar.text_input("Enter your city for the weather", max_chars=10)
        if fieldtext1:
            st.sidebar.write("The temperature for your city "+ fieldtext1 + " :")
            st.sidebar.write(getWeather(fieldtext1))
