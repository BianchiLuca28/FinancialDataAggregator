from abc import ABC, abstractmethod
from typing import List
import pandas as pd

class DataSource(ABC):
    """
    Abstract base class for all data sources.

    This ensures all data source implementations (CoinGecko, Yahoo Finance)
    provide the same interface and return data in a consistent format.
    """

    def __init__(self, name: str):
        """
        Initialize the data source.

        Args:
            name: Name of the data source (e.g., 'coingecko', 'yahoo_finance')
        """
        self.name = name

    @abstractmethod
    def fetch_current_prices(self, symbols: List[str]) -> List[dict]:
        """
        Fetch current prices for the given symbols.

        Args:
            symbols: List of asset symbols/IDs
        """
        pass

    @abstractmethod
    def fetch_historical_prices(self, symbol: str, days: int) -> pd.DataFrame:
        """
        Fetch historical daily prices for a symbol.

        Args:
            symbol: Asset symbol/ID
            days: Number of days of historical data to fetch
        """
        pass
