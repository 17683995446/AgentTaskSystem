"""
TaskProgressDto - 任务进度DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskProgressDto:
    task_id: str
    progress: int
    message: str
