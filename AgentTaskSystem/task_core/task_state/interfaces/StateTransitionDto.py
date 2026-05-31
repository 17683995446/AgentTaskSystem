"""
StateTransitionDto - 状态转换DTO
"""

from dataclasses import dataclass
from .TaskStateEnum import TaskStateEnum


@dataclass(frozen=True)
class StateTransitionDto:
    task_id: str
    from_state: TaskStateEnum
    to_state: TaskStateEnum
    transitioned_at: int
