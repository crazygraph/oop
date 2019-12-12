import riskreturn as rr
import dataprep as dp 


def read(symbols,start_date,end_date):
	data 	= dp.getAllPriceData(symbols,start_date,end_date)
	prices 	= rr.getAllPricePerformance(symbols,data,start_date,end_date)
	return prices.to_dict(orient='index')
	