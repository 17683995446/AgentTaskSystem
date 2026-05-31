"""
ITaskValidator - 任务校验接口
"""

from abc import ABC, abstractmethod


class ITaskValidator(ABC):
    @abstractmethod
    def validate_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def validate_params(self, params: tuple) -> bool:
        pass
