from .base import DataSource

class YahooSource(DataSource):

    def __init__(self):
        super().__init__()

    def fetch_current_prices(self, symbols):
        pass

    def fetch_historical_prices(self, symbols, days):
        pass
