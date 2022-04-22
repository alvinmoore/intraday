import intraday

STOCKS = intraday.get_stocks().index.to_list()
#STOCKS = [ 'UVXY' ]

print("Current time:  {}".format(intraday.CURRENT_TIMESTAMP))

for stock in STOCKS:
	print("\nUpdating stock: '{}'".format(stock))
	df = intraday.update_ticker(stock)
	df.head()
	print("  Last update:  {}".format(intraday.get_lastrecordtimestamp(df)))
	
