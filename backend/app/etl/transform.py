import pandas as pd

def prepare_prices_for_db(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['date'] = pd.to_datetime(df['date'])

        df.dropna(subset=['date', 'price'], inplace=True)

        df['price'] = pd.to_numeric(df['price'])
        df['market_cap'] = pd.to_numeric(df['market_cap'])
        df['volume'] = pd.to_numeric(df['volume'])

        # Remove duplicates, keeping the last occurrence for each date
        df = df.drop_duplicates()

        df.sort_values(by=['date'], inplace=True)

        df = df[["date", "price", "market_cap", "volume", "source"]]

        return df
    except Exception as e:
        raise ValueError(f"Error processing DataFrame: {e}")
