from abc import ABC, abstractmethod
from typing import Any


class ITaskValidator(ABC):

    @abstractmethod
    def validate_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def validate_params(self, params: list[dict]) -> tuple[bool, str]:
        pass

    @abstractmethod
    def validate_type_hint(self, type_hint: str) -> bool:
        pass
