from abc import ABC, abstractmethod
from typing import Any, Optional


class ISnapshot(ABC):

    @abstractmethod
    def save(self, key: str, data: Any) -> bool:
        pass

    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
