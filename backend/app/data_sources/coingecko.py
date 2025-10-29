from base import DataSource
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

from pycoingecko import CoinGeckoAPI

class CoingeckoSource(DataSource):

    def __init__(self):
        super().__init__(name="coingecko")
        self.cg_api = CoinGeckoAPI(demo_api_key=os.getenv('KEY_COINDGECKO_API'))

    def fetch_current_prices(self, symbols):
        results = self.cg_api.get_price(ids=symbols, vs_currencies=os.getenv('DATASOURCE_CURRENCY'))
        return results

    def fetch_historical_prices(self, symbol, days=7):
        ohlc = self.cg_api.get_coin_ohlc_by_id(id=symbol, vs_currency=os.getenv('DATASOURCE_CURRENCY'), days=str(days))

        df = pd.DataFrame(ohlc)

        df.columns = ["date", "open", "high", "low", "close"]
        df["date"] = pd.to_datetime(df["date"], unit = "ms")
        df.set_index('date', inplace = True)

        return df
