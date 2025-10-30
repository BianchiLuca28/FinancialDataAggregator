from .coingecko import CoingeckoSource

cs = CoingeckoSource()

data = cs.fetch_historical_prices("bitcoin", 14)

print(data.head())
print(data.columns)
print(data.info())
print(data.size)

print(cs.fetch_current_prices(["bitcoin"]))
