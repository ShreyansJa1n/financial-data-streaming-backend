from abc import ABC, abstractmethod
from typing import Dict, Any


class ProviderInterface(ABC):

    @abstractmethod
    def fetch_raw_data(self, symbol: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def extract_price(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
