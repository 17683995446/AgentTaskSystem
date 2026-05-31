"""
ISnapshot - 快照接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ISnapshot(ABC):
    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def load(self, key: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
