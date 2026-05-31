"""
ITaskState - 任务状态接口
"""

from abc import ABC, abstractmethod
from .TaskStateEnum import TaskStateEnum
from .TaskStateDto import TaskStateDto
from .StateTransitionDto import StateTransitionDto


class ITaskState(ABC):
    @abstractmethod
    def set_state(self, task_id: str, state: TaskStateEnum) -> StateTransitionDto:
        pass

    @abstractmethod
    def get_state(self, task_id: str) -> TaskStateEnum:
        pass

    @abstractmethod
    def get_state_dto(self, task_id: str) -> TaskStateDto:
        pass
