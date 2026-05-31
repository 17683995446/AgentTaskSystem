"""
ITaskSchedule - 任务调度接口
"""

from abc import ABC, abstractmethod
from .ScheduleRequestDto import ScheduleRequestDto
from .ScheduleResultDto import ScheduleResultDto


class ITaskSchedule(ABC):
    @abstractmethod
    def add_task(self, request: ScheduleRequestDto) -> ScheduleResultDto:
        pass

    @abstractmethod
    def get_next_task(self) -> ScheduleRequestDto:
        pass

    @abstractmethod
    def get_queue_size(self) -> int:
        pass
