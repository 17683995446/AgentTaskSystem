"""
TaskInfoDto - 任务信息DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskInfoDto:
    task_id: str
    name: str
    created_at: int
