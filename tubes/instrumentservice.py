import riskreturn as rr
import dataprep as dp 


def read(keyword=''):
	data 	= dp.instrumentSearch(keyword)
	return data.to_dict(orient='index')