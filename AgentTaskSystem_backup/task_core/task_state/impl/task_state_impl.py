from typing import Optional, Dict
from ..interfaces.i_task_state import ITaskState
from ..interfaces.task_state_enum import TaskStateEnum


class TaskStateImpl(ITaskState):

    def __init__(self):
        self._states: Dict[str, TaskStateEnum] = {}
        self._transitions = self._build_transition_map()

    def _build_transition_map(self) -> Dict[TaskStateEnum, set]:
        return {
            TaskStateEnum.PENDING: {TaskStateEnum.RUNNING, TaskStateEnum.CANCELLED},
            TaskStateEnum.RUNNING: {TaskStateEnum.COMPLETED, TaskStateEnum.FAILED, TaskStateEnum.CANCELLED},
            TaskStateEnum.COMPLETED: set(),
            TaskStateEnum.FAILED: set(),
            TaskStateEnum.CANCELLED: set()
        }

    def get_state(self, task_id: str) -> Optional[TaskStateEnum]:
        return self._states.get(task_id)

    def set_state(self, task_id: str, state: TaskStateEnum) -> bool:
        if task_id not in self._states:
            self._states[task_id] = state
            return True
        return False

    def is_valid_transition(
        self, task_id: str, new_state: TaskStateEnum
    ) -> bool:
        current = self._states.get(task_id)
        if current is None:
            return new_state == TaskStateEnum.PENDING
        return new_state in self._transitions.get(current, set())

    def transition(self, task_id: str, new_state: TaskStateEnum) -> bool:
        if not self.is_valid_transition(task_id, new_state):
            return False
        self._states[task_id] = new_state
        return True
