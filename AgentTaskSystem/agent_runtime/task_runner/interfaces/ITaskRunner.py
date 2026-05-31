"""
ITaskRunner - 任务执行接口
"""

from abc import ABC, abstractmethod
from .ExecuteRequestDto import ExecuteRequestDto
from .ExecuteResultDto import ExecuteResultDto
from .TaskProgressDto import TaskProgressDto


class ITaskRunner(ABC):
    @abstractmethod
    def execute_task(self, request: ExecuteRequestDto) -> ExecuteResultDto:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def get_progress(self, task_id: str) -> TaskProgressDto:
        pass
