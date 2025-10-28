from coingecko import CoingeckoSource

cs = CoingeckoSource()

data = cs.fetch_historical_prices("bitcoin", 14)

print(data.head())
