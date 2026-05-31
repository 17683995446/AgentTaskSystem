from typing import Optional, Any, Dict
from ..interfaces.i_task_runner import ITaskRunner


class TaskRunnerImpl(ITaskRunner):

    def __init__(self):
        self._running_tasks: Dict[str, bool] = {}
        self._results: Dict[str, Any] = {}
        self._progress: Dict[str, float] = {}

    def execute(self, task_id: str, params: Dict[str, Any]) -> bool:
        self._running_tasks[task_id] = True
        self._progress[task_id] = 0.0
        self._results[task_id] = None
        return True

    def get_result(self, task_id: str) -> Optional[Any]:
        return self._results.get(task_id)

    def is_running(self, task_id: str) -> bool:
        return self._running_tasks.get(task_id, False)

    def cancel(self, task_id: str) -> bool:
        if task_id in self._running_tasks:
            self._running_tasks[task_id] = False
            return True
        return False

    def get_progress(self, task_id: str) -> float:
        return self._progress.get(task_id, 0.0)
