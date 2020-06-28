import pandas
import matplotlib
import mplfinance
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc

matplotlib.style.use('ggplot')
# matplotlib.style.use('dark_background')

def stockPricePLot(ticker):
	# Load Data
	folder = '../data/intra_day_price/'
	file_name = folder + './' + ticker + '.csv'
	history = pandas.read_csv(file_name, parse_dates=True, index_col=0)

	# Data Manipulation
	close = history['close']
	print(close.head())
	close = close.reset_index()
	print(close.head())
	close['timestamp'] = close['timestamp'].map(matplotlib.dates.date2num)

	open_high_low_close = history[['open', 'high', 'low', 'close']].resample('1H').ohlc()
	print(open_high_low_close.head())
	open_high_low_close = open_high_low_close.reset_index()
	print(open_high_low_close.head())
	open_high_low_close['timestamp'] = open_high_low_close['timestamp'].map(matplotlib.dates.date2num)

	# Plot figures. 
	# Subplot 1: scatter plot
	subplot1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
	subplot1.xaxis_date()
	subplot1.plot(close['timestamp'], close['close'], 'b.')
	plt.title(ticker)
	# plt.show()

	# Subplot 2: candle stick plot.
	# subplot2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)
	# subplot2.xaxis_date()
	# mplfinance.candlestick_ohlc(ax=subplot2, quotes=open_high_low_close.values, width=0.01, colorup='g', colordown='r')
	## https://stackoverflow.com/questions/60599812/how-can-i-customize-mplfinance-plot
	print(history.keys())
	# history['Date'] = history['timestamp']
	history['Open'] = history['open']
	history['High'] = history['high']
	history['Low'] = history['low']
	history['Close'] = history['close']
	history['Volume'] = history['volume']

	subplot2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1, sharex=subplot1)
	# mplfinance.plot(history, type='candle', style='charles', title='', ylabel='', ylabel_lower='', volume=True, mav=(3,6,9), savefig='test-mplfinance.png')
	candlestick_ohlc(ax=subplot2, quotes=open_high_low_close.values, width=0.01, colorup='g', colordown='r')
	plt.show()


if __name__ == "__main__":
	stockPricePLot('NVDA')