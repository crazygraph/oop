import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import relativedelta
import dataprep as dp

#symbol = ['GOOG']
#start_date = '2014-10-01'
#end_date = '2019-11-01'
#data = dp.getAllPriceData(symbol,start_date,end_date)

def getMonths(start_date, end_date):
	delta = relativedelta.relativedelta(datetime.strptime(end_date,'%Y-%m-%d'), datetime.strptime(start_date,'%Y-%m-%d'))
	months = delta.years*12 + delta.months
	return months

def getAnnualReturn(data,months):
    total_return = (data.iloc[-1]-data.iloc[0])/data.iloc[0]
    annualized_return = ((1 + total_return)**(12/months))
    return annualized_return * 100

def getAnnualVolatility(data):
    annualized_vol = data.pct_change().std() * np.sqrt(250)
    return annualized_vol * 100

def getSharpeRatio(annualized_return,annualized_vol):
    sharpe_ratio = (annualized_return - 0.01*100) / annualized_vol
    return sharpe_ratio

def getAllPricePerformance(symbols,data,start_date,end_date):
    price = pd.DataFrame(index=symbols,columns=['annual return', 'annual risk','sharpe ratio'])
    price['annual return'] = getAnnualReturn(data, getMonths(start_date,end_date))
    price['annual risk'] = getAnnualVolatility(data)
    price['sharpe ratio'] = getSharpeRatio(getAnnualReturn(data,getMonths(start_date,end_date)),getAnnualVolatility(data))
    price.index.name='symbol'
    return price.reset_index()