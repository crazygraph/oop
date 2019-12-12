import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime
from dateutil import relativedelta
import requests
import json
from pandas.io.json import json_normalize
import sqlite3

cnx = sqlite3.connect('price.db', check_same_thread=False)

def url(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey=ZBTGX838US0G5RE2'
    return url

def checkSymbol(symbol):
    #url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+symbol+'&apikey=ZBTGX838US0G5RE2'
    #response = requests.get(url)
    #data = pd.DataFrame.from_dict(response.json()['bestMatches'])
    #return data['1. symbol']
    data = pd.read_sql('select * from symbol', cnx,index_col='index')
    if (data.empty):
        return 0
    else:
        if (data[data['symbol'] == symbol].empty):
            return 0 
        else:
            return 1

def instrumentSearch(keyword=''):
    data = pd.read_sql('select * from symbol', cnx,index_col='index')
    if (data.empty):
        return {'message':'table not found'}
    else:
        if (keyword == ''):
            return data
        else:
            if (data["symbol"].str.contains(keyword).empty):
                return {'message':'data not found'} 
            else:
                data = data[data["symbol"].str.contains(keyword,case=False) | data["name"].str.contains(keyword,case=False)]
                return data
                
def getPriceData(symbol):
    try:
        price = pd.read_sql('select * from '+symbol, cnx,index_col='index')
        return price
    except: 
        try:
            price = retrieveDataFromAPI(symbol)
            price.to_sql(name=symbol, con=cnx)
            return price
        except:
            return 'symbol tidak ditemukan'

def retrieveDataFromAPI(symbol):
    response = requests.get(url(symbol))
    try:
        timeseries = response.json()['Time Series (Daily)']
        data = pd.DataFrame.from_dict(timeseries, orient='index')
        data[symbol] = data['5. adjusted close'].astype(float)
        data = data.drop(columns=['1. open','2. high','3. low','4. close','5. adjusted close','6. volume','7. dividend amount','8. split coefficient'])
        return data
    except:
        return response.json()['Error Message']

def getAllPriceData(symbols,start_date,end_date):
    price = pd.DataFrame()
    for symbol in symbols:
        if(checkSymbol(symbol) == 1):
            price = pd.merge(price,getPriceData(symbol),how='outer',left_index=True,right_index=True)
        else:
            return 'symbol '+symbol+' not found'
    price = price.loc[start_date:end_date]
    return price