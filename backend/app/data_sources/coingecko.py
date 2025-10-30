from .base import DataSource
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
        results = self.cg_api.get_price(ids=symbols,
                                        vs_currencies=os.getenv('DATASOURCE_CURRENCY'),
                                        include_market_cap=True,
                                        include_24hr_vol=True
                                    )

        data = []

        for coin, values in results.items():
            data.append({
                "symbol": coin,
                "date": pd.Timestamp.now().date(),
                "price": values.get(os.getenv('DATASOURCE_CURRENCY')),
                "market_cap": values.get(f"{os.getenv('DATASOURCE_CURRENCY')}_market_cap"),
                "volume": values.get(f"{os.getenv('DATASOURCE_CURRENCY')}_24h_vol"),
                "source": self.name
            })

        return pd.DataFrame(data)

    def fetch_historical_prices(self, symbol, days=7):
        api_result = self.cg_api.get_coin_market_chart_by_id(id=symbol, vs_currency=os.getenv('DATASOURCE_CURRENCY'), days=days)

        df_prices = pd.DataFrame(api_result['prices'], columns=["timestamp", "price"])
        df_market_caps = pd.DataFrame(api_result['market_caps'], columns=["timestamp", "market_cap"])
        df_volumes = pd.DataFrame(api_result['total_volumes'], columns=["timestamp", "volume"])

        df = df_prices.merge(df_market_caps, on="timestamp")
        df = df.merge(df_volumes, on="timestamp")

        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

        df["symbol"] = symbol

        df["source"] = self.name

        df = df[["symbol", "date", "price", "market_cap", "volume", "source"]]

        return df

    def fetch_market_coins(self):
        return self.cg_api.get_coins_markets()
