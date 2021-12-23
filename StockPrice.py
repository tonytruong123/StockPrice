import streamlit as st
import yfinance as yf
import datetime
from PIL import Image
import time #format some variable
import requests
from PIL import Image
import bs4

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

f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")


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
    url = "https://www.worldometers.info/coronavirus/"
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
    url = "https://www.worldometers.info/coronavirus/country/"+name    
    html_data = get_html_data(url)
    #use bs4 to beutify our data
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_ ="content-inner").findAll("div", id="maincounter-wrap")
    all_data =""    
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
            st.sidebar.write(getWeather(fieldtext1))

## add the location
## add the percentage of recovering



