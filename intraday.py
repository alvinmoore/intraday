import yfinance as yf
import pandas as pd
import os
import pytz
from datetime import datetime, date, timedelta

# there's a limit from yfinance to only get intraday data for the last 30 days
CURRENT_TIMESTAMP = datetime.now(pytz.timezone('US/Eastern'))
EARLIEST_TIMESTAMP = CURRENT_TIMESTAMP - timedelta(days=30)
DIRNAME = os.path.dirname(__file__)

def to_utc(d):
    return d.astimezone(pytz.UTC)

def df_to_utc(df):
    df.index = df.index.map(to_utc)
    return df

def get_stocksfile():
    return DIRNAME + '/config/stocks.csv'

def get_tickerfile(ticker):
    return DIRNAME + '/data/' + ticker.upper() + '.csv'

def get_imagedir(ticker, dirdate):
    return DIRNAME + '/images/' + dirdate.strftime("%Y-%m-%d") + '/' + ticker.upper() + '/'

def get_imagefile(ticker, imagename, imagedir):
    return imagedir + '/' + ticker.upper() + '-' + imagename + '.png'

def get_stocks():
    filename = get_stocksfile()
    try:
        return pd.read_csv(filename, parse_dates=True, index_col='Symbol')
    except FileNotFoundError:
        print("Symbols config file '{}' not found.\n".format(filename))
        # return empty data frame on error
        return []

def get_cache(ticker):
    filename = get_tickerfile(ticker)
    try:
        return pd.read_csv(filename, parse_dates=True, index_col='Datetime')
    except FileNotFoundError:
        print("Ticker cache file '{}' not found.\n".format(filename))
        # return empty data frame on error
        return pd.DataFrame()

def get_lastrecordtimestamp(df):
    if len(df) == 0:
        return EARLIEST_TIMESTAMP
    # return latest data as UTC
    return df.index.max()

def get_nextrecordtimestamp(df):
    latest_record = get_lastrecordtimestamp(df) + timedelta(minutes=1)
    return EARLIEST_TIMESTAMP if EARLIEST_TIMESTAMP > latest_record else latest_record

def update_ticker(ticker):
    old_df = get_cache(ticker)
    start_date = get_nextrecordtimestamp(old_df)

    # get new data
    t = yf.Ticker(ticker)

    if start_date > CURRENT_TIMESTAMP:
        print("   Ticker {}: {} > {}".format(ticker, start_date, CURRENT_TIMESTAMP))
 
    while start_date < CURRENT_TIMESTAMP:
        end_date_max = start_date + timedelta(minutes=7*60*24)
        # Don't search beyond now
        end_date = end_date_max if CURRENT_TIMESTAMP > end_date_max else CURRENT_TIMESTAMP
        print("   Ticker {}: {} -> {}".format(ticker, start_date, end_date))
        df = t.history(start=start_date, end=end_date, interval="1m", prepost=True)
        if not df.empty:
            # append new data
            old_df = pd.concat([old_df, df])
            # serialize to CSV
            old_df.to_csv(get_tickerfile(ticker))
        start_date = end_date + timedelta(days=1)
    return old_df

def get_ticker(ticker):
    df = get_cache(ticker)
    # return latest data as UTC
    return df_to_utc(df)

def get_tickers(type):
    dirname = os.path.dirname(__file__)
    with open(f'{dirname}/tickers/{type}.py', 'r') as f: 
        return ast.literal_eval(f.read())