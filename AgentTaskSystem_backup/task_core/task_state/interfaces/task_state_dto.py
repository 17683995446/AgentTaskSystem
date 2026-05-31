from dataclasses import dataclass
from typing import Optional
from AgentTaskSystem.task_core.task_state.interfaces.task_state_enum import TaskStateEnum


@dataclass(frozen=True)
class TaskStateDto:
    task_id: str
    state: TaskStateEnum
    updated_at: int


@dataclass(frozen=True)
class StateTransitionDto:
    task_id: str
    from_state: TaskStateEnum
    to_state: TaskStateEnum
    timestamp: int
    success: bool
