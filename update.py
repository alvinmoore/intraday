import intraday

STOCKS = [ 'UVXY', '^GSPC', '^VIX', 'AMC', 'GME', 'AAPL', '^SPX', 'TSLA', '^DJI', 'SNP', 'GOOG', 'FB', 'SNOW', 'NFLX' ]

print("Current time:  {}".format(intraday.CURRENT_TIMESTAMP))

for stock in STOCKS:
	print("\nUpdating stock: '{}'".format(stock))
	df = intraday.update_ticker(stock)
	df.head()
	print("  Last update:  {}".format(intraday.get_lastrecordtimestamp(df)))
	
