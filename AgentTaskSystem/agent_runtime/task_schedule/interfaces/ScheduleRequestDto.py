"""
ScheduleRequestDto - 调度请求DTO
"""

from dataclasses import dataclass
from .SchedulePriority import SchedulePriority


@dataclass(frozen=True)
class ScheduleRequestDto:
    task_id: str
    priority: SchedulePriority
    scheduled_at: int
