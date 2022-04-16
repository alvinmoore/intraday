import intraday
import matplotlib.pyplot as plt
import pytz
import os
from datetime import datetime, timedelta, date

STOCKS = [ 'UVXY', '^GSPC', '^VIX', 'AMC', 'GME', 'AAPL', '^SPX', 'TSLA', '^DJI', 'SNP', 'GOOG', 'FB', 'SNOW', 'NFLX' ]
#STOCKS = [ 'UVXY' ]
DAYS_FILTERS = { "today" : 1, "lastweek" : 7, "lastmonth" : 30, "lastyear" : 365, "max" : 365 * 20 }
#DAYS_FILTERS["weekday"] = datetime.today().weekday()+1
GROUP_ORDER = [ "today", "weekday", "lastweek", "lastmonth", "lastyear", "max" ]

print("Exporting {} stocks".format(len(STOCKS)))


counter=0
for stock in STOCKS:
	counter += 1
	print("\nExporting stock #{}: '{}'".format(counter, stock))
	df = intraday.get_ticker(stock)
	lastrecorddate = intraday.get_lastrecordtimestamp(df)
	end_date = lastrecorddate + timedelta(days=1)
	DAYS_FILTERS["weekday"] = lastrecorddate.weekday()+1
	print("  {} -> {}".format(df.index.min().date(), df.index.max().date()))

	imagedir = intraday.get_imagedir(stock, lastrecorddate)
	os.makedirs(imagedir, exist_ok=True)

	# Process the current timegroup
	for timegroup in GROUP_ORDER:
		# Determine the date to start the filter
		filter_start = end_date - timedelta(days=DAYS_FILTERS[timegroup])

		# Filter the results
		today_df = df[filter_start:end_date]

		# Find the first date of the filter
		start_date = filter_start if filter_start > today_df.index.min() else today_df.index.min()

		print("  Processing {:10} {} -> {}".format(timegroup+':', start_date, end_date))
	
		# Create the display canvas
		plt.figure(figsize = (50,30))
		plt.rcParams.update({'font.size': 50})

		plt.title('{} {}: {} -> {}'.format(stock, timegroup, start_date.date(), end_date.date()))
		figure = plt.plot(today_df['Open'].tolist() if timegroup != "today" else today_df['Open'], 'xkcd:crimson', linewidth=2.5)
		plt.savefig(intraday.get_imagefile(stock, timegroup, imagedir))
		plt.close()	
