import intraday
import matplotlib.pyplot as plt
import pytz
import os
from datetime import datetime, timedelta, date

STOCKS = [ 'UVXY', '^GSPC', '^VIX', 'AMC', 'GME', 'AAPL', '^SPX', 'TSLA', '^DJI', 'SNP', 'GOOG', 'FB', 'SNOW', 'NFLX' ]
#STOCKS = [ 'UVXY' ]
DAYS_FILTERS = { "today" : 1, "lastweek" : 7, "lastmonth" : 30, "lastyear" : 365 }
#DAYS_FILTERS["weekday"] = datetime.today().weekday()+1
GROUP_ORDER = [ "today", "weekday", "lastweek", "lastmonth" ]

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
		start_date = end_date - timedelta(days=DAYS_FILTERS[timegroup])

		print("  Processing {:10} {} -> {}".format(timegroup+':', start_date, end_date))
		# Filter the results
		today_df = df[start_date:end_date]

		# Create the display canvas
		plt.figure(figsize = (50,30))
		plt.rcParams.update({'font.size': 50})

		plt.title('{} for {}'.format(timegroup, stock))
		figure = plt.plot(today_df['Open'].tolist() if timegroup != "today" else today_df['Open'], 'xkcd:crimson', linewidth=2.5)
		plt.savefig(intraday.get_imagefile(stock, timegroup, imagedir))
		plt.close()	
