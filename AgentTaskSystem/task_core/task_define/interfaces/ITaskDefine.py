"""
ITaskDefine - 任务定义接口
"""

from abc import ABC, abstractmethod


class ITaskDefine(ABC):
    @abstractmethod
    def create_task(self, task_data: dict):
        pass

    @abstractmethod
    def validate_task(self, task_id: str) -> bool:
        pass
