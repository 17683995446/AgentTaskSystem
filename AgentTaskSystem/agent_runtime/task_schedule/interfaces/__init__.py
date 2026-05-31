"""
TaskSchedule interfaces - 任务调度接口模块
"""

from .ITaskSchedule import ITaskSchedule
from .SchedulePriority import SchedulePriority
from .ScheduleRequestDto import ScheduleRequestDto
from .ScheduleResultDto import ScheduleResultDto

__all__ = [
    "ITaskSchedule",
    "SchedulePriority",
    "ScheduleRequestDto",
    "ScheduleResultDto"
]
