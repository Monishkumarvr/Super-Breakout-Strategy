from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from time import sleep
import streamlit as st

st.title("Super Breakout Strategy")

url = "https://www.topstockresearch.com/rt/IndexAnalyser/Nifty50/Technicals"

url1 = "https://www.topstockresearch.com/rt/IndexAnalyser/NiftyNext50/Technicals"

browser = webdriver.Chrome(executable_path= "C:/Users/Lenovo/Downloads/chromedriver/chromedriver.exe")
browser.get(url)
sleep(2)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

table_tag = soup.find_all("tr")

tr = [j for i, j in enumerate(table_tag) if i not in [0, 1, 27, 53]]

stocks = []
for tr_tag in tr:
    try:
        td = tr_tag.find_all('td')
        stock = []
        for td_tag in td:
            text = td_tag.text
            stock.append(text)
        stocks.append(stock)
    except:
        continue
browser.close()

browser = webdriver.Chrome(executable_path= "C:/Users/Lenovo/Downloads/chromedriver/chromedriver.exe")
browser.get(url1)
sleep(2)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

table_tag1 = soup.find_all("tr")

tr1 = [j for i, j in enumerate(table_tag1) if i not in [0, 1, 27, 53]]

for tr_tag in tr1:
    try:
        td = tr_tag.find_all('td')
        stock = []
        for td_tag in td:
            text = td_tag.text
            stock.append(text)
        stocks.append(stock)
    except:
        continue
browser.close()

df = pd.DataFrame(stocks, columns = ['Name', 'Close', 'SMA 5', 'SMA 10', 'SMA 15', 'SMA 20', 'SMA 50', 'SMA 100', 'SMA 200'])

d_t = {'Name': str, 
       'Close': float,
       'SMA 5': float,
       'SMA 10': float,
       'SMA 15': float,
       'SMA 20': float,
       'SMA 50': float,
       'SMA 100': float,
       'SMA 200': float
       }

df = df.astype(d_t)

df['Close - SMA 200'] = df['Close'] - df['SMA 200']
df = df.sort_values('Close - SMA 200')
st.write(df)

df_1 = df[(df['Close - SMA 200'] > -20) & (df['Close - SMA 200'] <0) & (df['Close']>df['SMA 5']) & (df['Close']>df['SMA 10']) & (df['Close']>df['SMA 15']) & (df['Close']>df['SMA 20']) & (df['Close']>df['SMA 50']) & (df['Close']>df['SMA 100']) & (df['Close']<df['SMA 200'])]
df_1 = df_1.sort_values('Close - SMA 200')

st.write(df_1)
