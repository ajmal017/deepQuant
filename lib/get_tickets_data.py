import pandas
import io
import datetime
import shutil
import urllib.request as request

from contextlib import closing

url_stocks = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
url_others = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt'

# Get a list of ticker online
def getTickersData(url_stocks, out_file):
	with closing(request.urlopen(url_stocks)) as r:
		with open(out_file, 'wb') as f:
			shutil.copyfileobj(r, f)


# Generate a list of tickers from online resource
if __name__ == "__main__":
	url_stocks = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
	date = datetime.datetime.today().strftime('%Y%m%d')
	folder = '../data/tickers/'
	out_file =  folder + './ticker_list_' + date + '.csv'

	getTickersData(url_stocks, out_file)