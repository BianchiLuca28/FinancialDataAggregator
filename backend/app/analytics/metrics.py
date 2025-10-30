import pandas as pd

def calculate_daily_returns(df_pandas):
    """Calculate daily returns and moving averages using Pandas."""

    # Sort by symbol and date
    df = df_pandas.sort_values(['symbol', 'date']).copy()

    # Calculate previous price per symbol
    df['prev_price'] = df.groupby('symbol')['price'].shift(1)

    # Calculate daily return as percentage
    df['daily_return'] = ((df['price'] - df['prev_price']) / df['prev_price']) * 100

    # Calculate 7-day moving average
    df['ma_7d'] = df.groupby('symbol')['price'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )

    # Calculate 30-day moving average
    df['ma_30d'] = df.groupby('symbol')['price'].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean()
    )

    # Calculate 30-day volatility (std dev of returns)
    df['volatility_30d'] = df.groupby('symbol')['daily_return'].transform(
        lambda x: x.rolling(window=30, min_periods=1).std()
    )

    # Drop helper column
    df = df.drop('prev_price', axis=1)

    return df
