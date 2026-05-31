"""
TaskStateDto - 任务状态DTO
"""

from dataclasses import dataclass
from .TaskStateEnum import TaskStateEnum


@dataclass(frozen=True)
class TaskStateDto:
    task_id: str
    state: TaskStateEnum
    updated_at: int
