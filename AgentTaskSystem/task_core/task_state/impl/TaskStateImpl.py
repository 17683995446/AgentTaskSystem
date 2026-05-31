"""
TaskStateImpl - 任务状态实现
"""

from typing import Dict, Any
from ..interfaces.ITaskState import ITaskState
from ..interfaces.TaskStateEnum import TaskStateEnum
from ..interfaces.TaskStateDto import TaskStateDto
from ..interfaces.StateTransitionDto import StateTransitionDto
from AgentTaskSystem.common.utils import get_current_timestamp
from AgentTaskSystem.common.Provider import Provider


class TaskStateImpl(ITaskState):
    def __init__(self):
        self._states = {}
        self._transitions = []
        self._snapshot = None
        self._load_from_snapshot()

    def _get_snapshot(self):
        if not self._snapshot:
            provider = Provider()
            self._snapshot = provider.get("snapshot")
        return self._snapshot

    def _load_from_snapshot(self):
        snapshot = self._get_snapshot()
        if snapshot and snapshot.exists("task_state"):
            data = snapshot.load("task_state")
            self._states = data.get("states", {})
            self._transitions = data.get("transitions", [])

    def _save_to_snapshot(self):
        snapshot = self._get_snapshot()
        if snapshot:
            data = {
                "states": self._states,
                "transitions": self._transitions
            }
            snapshot.save("task_state", data)

    def set_state(self, task_id: str, state: TaskStateEnum) -> StateTransitionDto:
        from_state = self._states.get(task_id, TaskStateEnum.PENDING)
        self._states[task_id] = state
        transition = StateTransitionDto(
            task_id=task_id,
            from_state=from_state,
            to_state=state,
            transitioned_at=get_current_timestamp()
        )
        self._transitions.append(transition)
        self._save_to_snapshot()
        return transition

    def get_state(self, task_id: str) -> TaskStateEnum:
        return self._states.get(task_id, TaskStateEnum.PENDING)

    def get_state_dto(self, task_id: str) -> TaskStateDto:
        return TaskStateDto(
            task_id=task_id,
            state=self.get_state(task_id),
            updated_at=get_current_timestamp()
        )
