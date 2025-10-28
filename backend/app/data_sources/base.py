from abc import ABC, abstractmethod
from typing import List
import pandas as pd

class DataSource(ABC):

    @abstractmethod
    def fetch_current_prices(self, symbols: List[str]) -> List[dict]:
        pass

    @abstractmethod
    def fetch_historical_prices(self, symbol: str, days: int) -> pd.DataFrame:
        pass
