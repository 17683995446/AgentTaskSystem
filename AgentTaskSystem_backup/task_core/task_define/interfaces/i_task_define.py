from abc import ABC, abstractmethod
from typing import Optional
from .task_dto import TaskParamDto as TaskParam, TaskResultDto as TaskResult


class ITaskDefine(ABC):

    @abstractmethod
    def create_task(self, name: str, params: list[TaskParam]) -> TaskResult:
        pass

    @abstractmethod
    def validate_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def get_task_info(self, task_id: str) -> Optional[dict]:
        pass
