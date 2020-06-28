### Get intra day price for a given list of stock tickers
### For each ticker, the price data will be stored in the data/intra_day_price folder.

import requests
import pandas
import io

import shutil
import urllib.request as request
from contextlib import closing
import datetime
import os
import time


# Read stock price data from URL
def dataFromUrl(url):
	data_string = requests.get(url).content
	raw_data = pandas.read_csv(io.StringIO(data_string.decode('utf-8')), index_col=0)
	return raw_data


# Request stock price
def stockPriceIntraDay(ticker, folder):
	# Get data online
	interval = '1min'

	# You may use a different API key
	url = 'https://www.alphavantage.co/query?apikey=' + \
	      'ZMV8NPTG5H5JSZZ3' + \
	      '&function=TIME_SERIES_INTRADAY&symbol=' +  \
	      '{ticker}&interval={interval}&outputsize=full&datatype=csv'.format(
	      	ticker=ticker, interval=interval)

	# Get stock price
	intraday = dataFromUrl(url)

	# Append if history exists
	file = folder + '/' + ticker + '.csv'
	if os.path.exists(file):
		history = pandas.read_csv(file, index_col=0)
		intraday.append(history)

	# Inverse based on index
	intraday.sort_index(inplace=True)

	# Save to file
	intraday.to_csv(file)
	print('Intraday for [' + ticker + '] got.')


def getTickersPrice(tickers_list_file):
	write_folder = '../data/intra_day_price/'
	sep = '|'
	tickers_raw_data = pandas.read_csv(tickers_list_file, sep)

	tickers = tickers_raw_data['Symbol'].tolist()

	# Get stock price (intraday)
	for i, ticker in enumerate(tickers):
		try:
			time.sleep(1)

			print('Intraday', i, '/', len(tickers))
			stockPriceIntraDay(ticker, folder=write_folder)

			# Max frequency should be less than five requests per min
			# Only 500 requests can be made per day
			time.sleep(1)
		except:
			pass
	print('Intraday for all stocks got.')


if __name__ == "__main__":
	# getTickersPrice('../data/tickers/ticker_list_20200628.csv')
	getTickersPrice('../data/tickers/ticker_list_of_interests_test.csv')

	