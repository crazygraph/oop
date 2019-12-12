import dataprep as dp 
import portfolio as prt 

def read(symbols,start_date,end_date,cum_ret=False):
	data 	= dp.getAllPriceData(symbols,start_date,end_date)
	weights,performance = prt.getMaxSharpePortfolio(data)
	weights2,performance2  = prt.getMinVolatilityPortfolio(data)
	cum_return_max = prt.getCumReturnFromMaxSharpe(data)
	cum_return_min = prt.getCumReturnFromMinVolatility(data)

	if cum_ret == True:
		result = {
        			'Maximum sharpe portfolio':{
        				'weights':weights,
        				'performance':dict(zip(['Expected annual return','Annual volatility','Sharpe Ratio'],list(performance)))
        			},
        			'Minimum volatility portfolio':{
        				'weights':weights2,
        				'performance':dict(zip(['Expected annual return','Annual volatility','Sharpe Ratio'],list(performance2)))
        			},
        			'Cumulative Return':{
        				'Maximum Sharpe': cum_return_max.to_dict(orient='index'),
        				'Minimum Volatility': cum_return_min.to_dict(orient='index')
        			}
        }

	else:
		result = {
					'Maximum sharpe portfolio':{
						'weights':weights,
						'performance':dict(zip(['Expected annual return','Annual volatility','Sharpe Ratio'],list(performance)))
					},
					'Minimum volatility portfolio':{
						'weights':weights2,
						'performance':dict(zip(['Expected annual return','Annual volatility','Sharpe Ratio'],list(performance2)))
					}
		}

	return result