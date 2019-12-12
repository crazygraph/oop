import pandas as pd
import numpy as np
import dataprep as dp
from pypfopt.efficient_frontier import EfficientFrontier 
from pypfopt import risk_models
from pypfopt import expected_returns
import json

#symbols = ['GOOG','AAPL','MSFT','AMZN']
#start_date = '2014-10-01'
#end_date = '2019-11-01'
#data = dp.getAllPriceData(symbols,start_date,end_date)

def getMuSigma(data):
    mu = expected_returns.mean_historical_return(data)
    Sigma = risk_models.sample_cov(data)
    return mu,Sigma

def getMaxSharpePortfolio(data):
    mu,Sigma = getMuSigma(data)
    ef = EfficientFrontier(mu, Sigma)
    raw_weights = ef.max_sharpe()
    weights = ef.clean_weights()
    performance = ef.portfolio_performance()
    return weights,performance

def getMinVolatilityPortfolio(data):
    mu,Sigma = getMuSigma(data)
    ef = EfficientFrontier(mu, Sigma)
    raw_weights = ef.min_volatility()
    weights = ef.clean_weights()
    performance = ef.portfolio_performance()
    return weights,performance

def getCumReturnFromMaxSharpe(data):
    returns = data.pct_change()
    weights,performance = getMaxSharpePortfolio(data)
    weights = np.array(list(weights.values()), dtype=float)
    returns['portfolio'] = returns.dot(weights)
    daily_cum_ret=(1+returns).cumprod()
    return daily_cum_ret

def getCumReturnFromMinVolatility(data):
    returns = data.pct_change()
    weights,performance = getMinVolatilityPortfolio(data)
    weights = np.array(list(weights.values()), dtype=float)
    returns['portfolio'] = returns.dot(weights)
    daily_cum_ret=(1+returns).cumprod()
    return daily_cum_ret