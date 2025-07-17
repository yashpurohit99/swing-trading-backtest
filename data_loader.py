# swing_strategy_project/utils/data_loader.py

import yfinance as yf
import pandas as pd

def fetch_daily_data(symbol, start_date, end_date):
    full_symbol = symbol + ".NS" if not symbol.endswith(".NS") else symbol
    df = yf.download(full_symbol, start=start_date, end=end_date, progress=False)

    # Fix MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]  # Keep only required columns
    df.dropna(inplace=True)
    return df

def fetch_benchmark_data(start_date, end_date):
    nifty_symbol = "^NSEI"
    df = yf.download(nifty_symbol, start=start_date, end=end_date, progress=False)

    # Fix MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.dropna(inplace=True)
    return df
