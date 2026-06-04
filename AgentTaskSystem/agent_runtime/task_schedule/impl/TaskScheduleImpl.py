"""
TaskScheduleImpl - 任务调度实现
"""

import heapq
from ..interfaces.ITaskSchedule import ITaskSchedule
from ..interfaces.SchedulePriority import SchedulePriority
from ..interfaces.ScheduleRequestDto import ScheduleRequestDto
from ..interfaces.ScheduleResultDto import ScheduleResultDto
from AgentTaskSystem.common import MAX_QUEUE_SIZE
from AgentTaskSystem.common.Logger import get_logger


class TaskScheduleImpl(ITaskSchedule):
    def __init__(self):
        self._queue = []
        self._counter = 0
        self._task_ids = set()
        self._logger = get_logger()
        self._logger.info("TaskSchedule", "TaskScheduleImpl initialized")

    def add_task(self, request: ScheduleRequestDto) -> ScheduleResultDto:
        self._logger.info("TaskSchedule", f"add_task() called: request={request}")
        if request is None:
            self._logger.error("TaskSchedule", "request is None")
            return ScheduleResultDto(success=False, task_id="", position=-1, message="request is None")
        if not isinstance(request, ScheduleRequestDto):
            self._logger.error("TaskSchedule", f"Invalid request type: {type(request)}")
            return ScheduleResultDto(success=False, task_id="", position=-1, message="Invalid request type")
        if not request.task_id:
            self._logger.error("TaskSchedule", "task_id is empty")
            return ScheduleResultDto(success=False, task_id="", position=-1, message="task_id is empty")

        if len(self._queue) >= MAX_QUEUE_SIZE:
            self._logger.error("TaskSchedule", f"Queue is full: {len(self._queue)}/{MAX_QUEUE_SIZE}")
            return ScheduleResultDto(
                success=False,
                task_id=request.task_id,
                position=-1,
                message="Queue is full"
            )

        if request.task_id in self._task_ids:
            self._logger.warn("TaskSchedule", f"Duplicate task_id: {request.task_id}")
            return ScheduleResultDto(
                success=False,
                task_id=request.task_id,
                position=-1,
                message="Duplicate task_id"
            )

        self._counter += 1
        priority = -request.priority
        heapq.heappush(
            self._queue,
            (priority, self._counter, request)
        )
        self._task_ids.add(request.task_id)
        position = len(self._queue)
        self._logger.info("TaskSchedule", f"Task added: {request.task_id} at position {position}")
        return ScheduleResultDto(
            success=True,
            task_id=request.task_id,
            position=position,
            message="Task added"
        )

    def get_next_task(self) -> ScheduleRequestDto:
        self._logger.info("TaskSchedule", "get_next_task() called")
        if not self._queue:
            self._logger.debug("TaskSchedule", "Queue is empty")
            return None
        _, _, request = heapq.heappop(self._queue)
        self._task_ids.discard(request.task_id)
        self._logger.info("TaskSchedule", f"Next task: {request.task_id}, queue_size={len(self._queue)}")
        return request

    def get_queue_size(self) -> int:
        size = len(self._queue)
        self._logger.debug("TaskSchedule", f"get_queue_size() = {size}")
        return size

    def has_task(self, task_id: str) -> bool:
        exists = task_id in self._task_ids
        self._logger.debug("TaskSchedule", f"has_task({task_id}) = {exists}")
        return exists

    def clear(self):
        self._logger.info("TaskSchedule", "clear() called")
        self._queue = []
        self._task_ids = set()
        self._counter = 0
