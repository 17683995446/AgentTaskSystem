from abc import ABC, abstractmethod
from typing import Optional
from AgentTaskSystem.task_core.task_state.interfaces.task_state_enum import TaskStateEnum


class ITaskState(ABC):

    @abstractmethod
    def get_state(self, task_id: str) -> Optional[TaskStateEnum]:
        pass

    @abstractmethod
    def set_state(self, task_id: str, state: TaskStateEnum) -> bool:
        pass

    @abstractmethod
    def is_valid_transition(
        self, task_id: str, new_state: TaskStateEnum
    ) -> bool:
        pass

    @abstractmethod
    def transition(self, task_id: str, new_state: TaskStateEnum) -> bool:
        pass
