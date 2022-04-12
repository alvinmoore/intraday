import yfinance as yf
import pandas as pd
import os, ast
import pytz
from datetime import datetime, date, timedelta, timezone

# there's a limit from yfinance to only get intraday data for the last 30 days
CURRENT_DATE = pytz.UTC.localize(datetime.now())
START_DATE = CURRENT_DATE - timedelta(days=30)

def to_utc(d):
    return d.tz_convert(timezone.utc)

def df_to_utc(df):
    df.index = df.index.map(to_utc)
    
def get_tickerfile(ticker):
    dirname = os.path.dirname(__file__)
    return dirname + '/data/' + ticker + '.csv'

def get_cache(ticker):
    filename = get_tickerfile(ticker)
    try:
        return pd.read_csv(filename, parse_dates=True, index_col='Datetime')
    except FileNotFoundError:
        print("Ticker cache file '{}' not found.\n".format(filename))
        # return empty data frame on error
        return pd.DataFrame()

def get_lastday(df):
    if len(df) == 0:
        return START_DATE
    latest_record = df.index.max()
    return START_DATE if START_DATE > latest_record else latest_record

def update_ticker(ticker):
    old_df = get_cache(ticker)
    start_date = get_lastday(old_df) + timedelta(minutes=1)

    # get new data
    t = yf.Ticker(ticker)

    while start_date < CURRENT_DATE:
        end_date_max = start_date + timedelta(days=7)
        # Don't search beyond now
        end_date = end_date_max if CURRENT_DATE > end_date_max else CURRENT_DATE
        print("getting ticker {} from {} to {}".format(ticker, start_date, end_date))
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
    df_to_utc(df)
    return df

def get_tickers(type):
    dirname = os.path.dirname(__file__)
    with open(f'{dirname}/tickers/{type}.py', 'r') as f: 
        return ast.literal_eval(f.read())