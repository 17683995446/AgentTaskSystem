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
from AgentTaskSystem.common.Logger import get_logger


class TaskStateImpl(ITaskState):
    def __init__(self):
        self._states = {}
        self._transitions = []
        self._snapshot = None
        self._logger = get_logger()
        self._logger.info("TaskState", "TaskStateImpl initialized")
        self._load_from_snapshot()

    def _get_snapshot(self):
        if not self._snapshot:
            provider = Provider()
            self._snapshot = provider.get("snapshot")
        return self._snapshot

    def _load_from_snapshot(self):
        self._logger.debug("TaskState", "_load_from_snapshot() called")
        snapshot = self._get_snapshot()
        if snapshot and snapshot.exists("task_state"):
            try:
                data = snapshot.load("task_state")
                self._states = data.get("states", {})
                self._transitions = data.get("transitions", [])
                self._logger.info("TaskState", f"Loaded {len(self._states)} states from snapshot")
            except Exception as e:
                self._logger.error("TaskState", f"Failed to load snapshot: {e}")
                self._states = {}
                self._transitions = []

    def _save_to_snapshot(self):
        self._logger.debug("TaskState", "_save_to_snapshot() called")
        snapshot = self._get_snapshot()
        if snapshot:
            try:
                data = {
                    "states": self._states,
                    "transitions": self._transitions
                }
                snapshot.save("task_state", data)
                self._logger.debug("TaskState", "Snapshot saved successfully")
            except Exception as e:
                self._logger.error("TaskState", f"Failed to save snapshot: {e}")

    def set_state(self, task_id: str, state: TaskStateEnum) -> StateTransitionDto:
        self._logger.info("TaskState", f"set_state() called: task_id={task_id}, state={state}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("TaskState", f"Invalid task_id: {task_id}")
            raise ValueError(f"Invalid task_id: {task_id}")
        if not isinstance(state, TaskStateEnum):
            self._logger.error("TaskState", f"Invalid state type: {type(state)}")
            raise ValueError(f"State must be TaskStateEnum, got {type(state)}")

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
        self._logger.info("TaskState", f"State transition: {from_state.value} -> {state.value}")
        return transition

    def get_state(self, task_id: str) -> TaskStateEnum:
        self._logger.debug("TaskState", f"get_state() called for {task_id}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("TaskState", f"Invalid task_id: {task_id}")
            return TaskStateEnum.PENDING
        state = self._states.get(task_id, TaskStateEnum.PENDING)
        self._logger.debug("TaskState", f"Task {task_id} state: {state.value}")
        return state

    def get_state_dto(self, task_id: str) -> TaskStateDto:
        self._logger.debug("TaskState", f"get_state_dto() called for {task_id}")
        return TaskStateDto(
            task_id=task_id,
            state=self.get_state(task_id),
            updated_at=get_current_timestamp()
        )

    def get_transitions(self, task_id: str) -> list:
        self._logger.debug("TaskState", f"get_transitions() called for {task_id}")
        return [t for t in self._transitions if t.task_id == task_id]
