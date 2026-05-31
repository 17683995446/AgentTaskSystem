"""
ScheduleResultDto - 调度结果DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleResultDto:
    success: bool
    task_id: str
    position: int
    message: str
