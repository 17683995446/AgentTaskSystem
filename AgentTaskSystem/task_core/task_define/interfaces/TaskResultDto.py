"""
TaskResultDto - 任务结果DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskResultDto:
    success: bool
    task_id: str
    message: str
