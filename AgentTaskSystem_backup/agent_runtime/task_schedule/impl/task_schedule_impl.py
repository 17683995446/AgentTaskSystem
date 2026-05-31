import heapq
from typing import Optional, List, Tuple
from ..interfaces.i_task_schedule import ITaskSchedule
from ..interfaces.schedule_priority import SchedulePriority


class TaskScheduleImpl(ITaskSchedule):
    DEFAULT_MAX_SIZE = 1000

    def __init__(self, max_size: int = DEFAULT_MAX_SIZE):
        self._max_size = max_size
        self._counter = 0
        self._queue: List[Tuple[int, int, str]] = []

    def enqueue(self, task_id: str, priority: SchedulePriority) -> bool:
        if self.is_full():
            return False
        self._counter += 1
        heapq.heappush(self._queue, (priority.value, self._counter, task_id))
        return True

    def dequeue(self) -> Optional[str]:
        if not self._queue:
            return None
        _, _, task_id = heapq.heappop(self._queue)
        return task_id

    def get_queue_size(self) -> int:
        return len(self._queue)

    def is_full(self) -> bool:
        return len(self._queue) >= self._max_size

    def clear_queue(self) -> None:
        self._queue.clear()
