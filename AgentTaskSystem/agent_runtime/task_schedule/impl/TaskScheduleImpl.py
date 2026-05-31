"""
TaskScheduleImpl - 任务调度实现
"""

import heapq
from ..interfaces.ITaskSchedule import ITaskSchedule
from ..interfaces.SchedulePriority import SchedulePriority
from ..interfaces.ScheduleRequestDto import ScheduleRequestDto
from ..interfaces.ScheduleResultDto import ScheduleResultDto
from AgentTaskSystem.common import MAX_QUEUE_SIZE


class TaskScheduleImpl(ITaskSchedule):
    def __init__(self):
        self._queue = []
        self._counter = 0

    def add_task(self, request: ScheduleRequestDto) -> ScheduleResultDto:
        if len(self._queue) >= MAX_QUEUE_SIZE:
            return ScheduleResultDto(
                success=False,
                task_id=request.task_id,
                position=-1,
                message="Queue is full"
            )
        self._counter += 1
        priority = -request.priority
        heapq.heappush(
            self._queue,
            (priority, self._counter, request)
        )
        return ScheduleResultDto(
            success=True,
            task_id=request.task_id,
            position=len(self._queue),
            message="Task added"
        )

    def get_next_task(self) -> ScheduleRequestDto:
        if not self._queue:
            return None
        _, _, request = heapq.heappop(self._queue)
        return request

    def get_queue_size(self) -> int:
        return len(self._queue)
